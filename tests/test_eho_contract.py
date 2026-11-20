"""Kiểm thử hợp đồng (shared contract) và tính đúng đắn cho Discrete EHO."""

from dataclasses import asdict, fields
import json
from pathlib import Path
from random import Random
import sys
import pytest

import ga_eho_tsp.algorithms.eho.solver as eho_solver_module
from ga_eho_tsp.algorithms.eho import solve
from ga_eho_tsp.algorithms.eho.clans import Clan
from ga_eho_tsp.algorithms.eho.discrete_ops import (
    hamming_distance,
    move_toward_best,
    update_matriarch,
)
from ga_eho_tsp.algorithms.eho.separation import separate
from ga_eho_tsp.algorithms.eho.solver import _preserve_global_best
from ga_eho_tsp.data.matrix_loader import load_matrix
from ga_eho_tsp.domain.models import EHOConfig, IterationStat, RunResult, TSPProblem
from ga_eho_tsp.domain.objective import validate_route
from ga_eho_tsp.domain.operators import random_permutation
from ga_eho_tsp.domain.protocols import Solver

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
ALL_DATASETS = (
    "03Cities-6.txt",
    "04Cities-189.txt",
    "06Cities-1248.txt",
    "15Cities-1194.txt",
    "26Cities-937.txt",
    "42Cities-699.txt",
    "48Cities-33523.txt",
)


# ---------------------------------------------------------------------------
# 1. Clan structure, invariants, tie-break & Hamming medoid
# ---------------------------------------------------------------------------


def test_clan_invariants_and_validation():
    members = ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 2, 1))
    costs = (10.0, 20.0, 15.0)
    clan = Clan(members, costs)
    assert clan.size == 3
    assert clan.dimension == 4
    assert clan.best_index() == 0
    assert clan.worst_indices(1) == (1,)

    with pytest.raises(ValueError):
        Clan((), ())
    with pytest.raises(ValueError):
        Clan(members, (10.0, 20.0))
    with pytest.raises(ValueError):
        Clan(((0, 1, 2), (1, 0, 2)), (1.0, 2.0))
    with pytest.raises(ValueError):
        Clan(((0, 1, 2),), (-1.0,))
    with pytest.raises(ValueError):
        Clan(((0, 1, 2),), (float("nan"),))
    with pytest.raises(ValueError):
        Clan(((0, 1, 2),), (float("inf"),))
    with pytest.raises(ValueError):
        Clan(((0, 1, 2),), (True,))  # type: ignore[arg-type]


def test_clan_best_worst_tie_break_and_protection():
    members = (
        (0, 1, 2, 3),
        (0, 1, 3, 2),
        (0, 2, 1, 3),
        (0, 3, 2, 1),
    )
    # Hòa hoàn toàn chi phí: best ưu tiên index nhỏ (0), worst ưu tiên index nhỏ (0, 1...)
    clan = Clan(members, (50.0, 50.0, 50.0, 50.0))
    assert clan.best_index() == 0
    assert clan.worst_indices(2) == (0, 1)
    assert clan.worst_indices(2, protected_indices=(0,)) == (1, 2)

    with pytest.raises(ValueError):
        clan.worst_indices(4, protected_indices=(0,))
    with pytest.raises(ValueError):
        clan.worst_indices(-1)
    with pytest.raises(ValueError):
        clan.worst_indices(1, protected_indices=(99,))


def test_clan_medoid_matches_manual_calculation_and_tie_break():
    # Kiểm chứng khớp tính tay trên bộ 4 route (6 thành phố)
    members = (
        (0, 1, 2, 3, 4, 5),  # sum Hamming = 0 + 5 + 4 + 2 = 11
        (0, 2, 1, 4, 5, 3),  # sum Hamming = 5 + 0 + 2 + 3 = 10
        (0, 2, 1, 3, 5, 4),  # sum Hamming = 4 + 2 + 0 + 2 = 8
        (0, 2, 1, 3, 4, 5),  # sum Hamming = 2 + 3 + 2 + 0 = 7 -> medoid
    )
    clan = Clan(members, (100.0, 300.0, 250.0, 200.0))
    assert clan.center_index() == 3
    assert clan.center() == members[3]

    # Khi tổng Hamming bằng nhau, ưu tiên cost thấp hơn rồi index nhỏ hơn
    symmetric_members = (
        (0, 1, 2, 3),  # khoảng cách tới 2 route kia = 2 + 2 = 4
        (0, 2, 3, 1),  # khoảng cách tới 2 route kia = 3 + 3 = 6
        (0, 3, 1, 2),  # khoảng cách tới 2 route kia = 3 + 3 = 6
    )
    # 2 route cuối cùng sum=6; thử 2 route bằng tổng Hamming:
    two_members = ((0, 1, 2, 3), (0, 2, 1, 3))
    clan_cost_tie = Clan(two_members, (20.0, 10.0))
    assert clan_cost_tie.center_index() == 1
    clan_idx_tie = Clan(two_members, (10.0, 10.0))
    assert clan_idx_tie.center_index() == 0
    assert symmetric_members[0] in Clan(symmetric_members, (1.0, 2.0, 3.0)).members


# ---------------------------------------------------------------------------
# 2. Route validity, Objective consistency & Shared Contract across all 7 datasets
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("filename", ALL_DATASETS)
def test_eho_route_validity_and_objective_consistency_all_datasets(filename):
    problem = load_matrix(DATA_DIR / filename)
    config = EHOConfig(
        clan_count=2,
        elephants_per_clan=6,
        iterations=5,
        max_iterations=5,
        alpha=0.7,
        beta=0.3,
        separation_count_per_clan=1,
        seed=42,
    )
    result = solve(problem, config)

    assert isinstance(result, RunResult)
    assert result.algorithm == "eho"
    assert result.problem_name == problem.name
    assert result.is_valid is True
    assert result.stopping_reason == "MAX_ITERATIONS"
    assert result.iterations_completed == 5

    # Route validity: độ dài n, bắt đầu từ 0, hoán vị 0..n-1
    validate_route(result.best_route, problem.dimension)
    assert len(result.best_route) == problem.dimension
    assert result.best_route[0] == 0
    assert sorted(result.best_route) == list(range(problem.dimension))

    # Objective consistency: khớp tính lại độc lập
    recomputed = problem.route_length(result.best_route)
    assert result.best_distance == pytest.approx(recomputed)
    assert result.history[-1].best_so_far == pytest.approx(recomputed)


def test_eho_shared_contract_protocol_serialization_and_no_gui_imports():
    solver: Solver[EHOConfig] = solve
    problem = TSPProblem("triangle", ((0, 1, 2), (1, 0, 3), (2, 3, 0)))
    config = EHOConfig(clan_count=2, elephants_per_clan=4, iterations=2, max_iterations=2, seed=7)
    result = solver(problem, config)

    expected_fields = {
        "algorithm",
        "problem_name",
        "best_route",
        "best_distance",
        "iterations_completed",
        "evaluations",
        "elapsed_seconds",
        "seed",
        "history",
        "config_snapshot",
        "stopping_reason",
        "is_valid",
        "metadata",
    }
    assert {field.name for field in fields(RunResult)} == expected_fields
    record = json.loads(json.dumps(asdict(result)))
    assert record["algorithm"] == "eho"
    assert record["best_route"][0] == 0 and len(record["best_route"]) == 3
    assert record["best_distance"] == pytest.approx(6.0)
    assert result.metadata["clan_center"] == "hamming_medoid"
    assert result.metadata["initialization_atomic"] is True
    assert result.metadata["partial_iteration"] is False
    assert "tkinter" not in sys.modules and "matplotlib.pyplot" not in sys.modules


def test_solve_rejects_invalid_problem_or_config():
    problem = TSPProblem("triangle", ((0, 1, 2), (1, 0, 3), (2, 3, 0)))
    with pytest.raises(ValueError):
        solve("not-a-problem", EHOConfig())  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        solve(problem, "not-a-config")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# 3. Evaluation counting & operator delegation
# ---------------------------------------------------------------------------


def test_evaluation_counting_matches_actual_route_length_calls(monkeypatch):
    problem = load_matrix(DATA_DIR / "15Cities-1194.txt")
    call_count = 0
    original_route_length = TSPProblem.route_length

    def spy_route_length(self, route):
        nonlocal call_count
        call_count += 1
        return original_route_length(self, route)

    monkeypatch.setattr(TSPProblem, "route_length", spy_route_length)

    config = EHOConfig(
        clan_count=3,
        elephants_per_clan=5,
        iterations=4,
        max_iterations=4,
        separation_count_per_clan=1,
        seed=11,
    )
    result = solve(problem, config)

    pop_size = config.clan_count * config.elephants_per_clan
    expected_evals = pop_size * (1 + config.iterations)
    assert result.evaluations == expected_evals
    assert call_count == expected_evals
    assert result.history[0].evaluations == pop_size
    assert result.history[-1].evaluations == expected_evals


def test_solver_delegates_to_public_eho_operators(monkeypatch):
    problem = load_matrix(DATA_DIR / "06Cities-1248.txt")
    counts = {"move": 0, "matriarch": 0, "separate": 0}

    orig_move = eho_solver_module.move_toward_best
    orig_matriarch = eho_solver_module.update_matriarch
    orig_separate = eho_solver_module.separate

    def spy_move(*args, **kwargs):
        counts["move"] += 1
        return orig_move(*args, **kwargs)

    def spy_matriarch(*args, **kwargs):
        counts["matriarch"] += 1
        return orig_matriarch(*args, **kwargs)

    def spy_separate(*args, **kwargs):
        counts["separate"] += 1
        return orig_separate(*args, **kwargs)

    monkeypatch.setattr(eho_solver_module, "move_toward_best", spy_move)
    monkeypatch.setattr(eho_solver_module, "update_matriarch", spy_matriarch)
    monkeypatch.setattr(eho_solver_module, "separate", spy_separate)

    config = EHOConfig(
        clan_count=2,
        elephants_per_clan=5,
        iterations=3,
        max_iterations=3,
        separation_count_per_clan=1,
        seed=5,
    )
    solve(problem, config)

    # 3 iterations x 2 clans: mỗi clan có 1 matriarch, 1 separation, 3 common
    assert counts["matriarch"] == 3 * 2
    assert counts["separate"] == 3 * 2
    assert counts["move"] == 3 * 2 * 3


# ---------------------------------------------------------------------------
# 4. Budget compliance, iteration caps & Stop conditions
# ---------------------------------------------------------------------------


def test_budget_compliance_max_evaluations_50_on_15_cities(monkeypatch):
    problem = load_matrix(DATA_DIR / "15Cities-1194.txt")
    call_count = 0
    original_route_length = TSPProblem.route_length

    def spy_route_length(self, route):
        nonlocal call_count
        call_count += 1
        return original_route_length(self, route)

    monkeypatch.setattr(TSPProblem, "route_length", spy_route_length)

    # pop_size = 2 * 10 = 20 <= 50; init=20, iter1=40, iter2 dừng giữa chừng ở 50
    config = EHOConfig(
        clan_count=2,
        elephants_per_clan=10,
        iterations=20,
        max_iterations=20,
        max_evaluations=50,
        seed=42,
    )
    result = solve(problem, config)

    assert result.evaluations <= 50
    assert result.evaluations == 50
    assert call_count == 50
    assert result.stopping_reason == "MAX_EVALUATIONS"
    assert result.iterations_completed == 1
    assert result.metadata["partial_iteration"] is True
    assert result.history[-1].evaluations == 50
    validate_route(result.best_route, problem.dimension)
    assert result.best_distance == pytest.approx(original_route_length(problem, result.best_route))


def test_budget_exact_boundary_commits_cleanly():
    problem = load_matrix(DATA_DIR / "06Cities-1248.txt")
    config = EHOConfig(
        clan_count=2,
        elephants_per_clan=5,
        iterations=10,
        max_iterations=10,
        max_evaluations=20,  # init 10 + 1 full iteration 10
        seed=3,
    )
    result = solve(problem, config)
    assert result.evaluations == 20
    assert result.iterations_completed == 1
    assert result.stopping_reason == "MAX_EVALUATIONS"
    assert result.metadata["partial_iteration"] is False


def test_min_of_iterations_and_max_iterations_is_respected():
    problem = load_matrix(DATA_DIR / "04Cities-189.txt")
    config = EHOConfig(
        clan_count=2,
        elephants_per_clan=4,
        iterations=50,
        max_iterations=3,
        seed=1,
    )
    result = solve(problem, config)
    assert result.iterations_completed == 3
    assert result.stopping_reason == "MAX_ITERATIONS"
    assert result.evaluations == 8 * (1 + 3)


def test_stop_requested_immediate_and_mid_generation():
    problem = load_matrix(DATA_DIR / "15Cities-1194.txt")
    config = EHOConfig(
        clan_count=2,
        elephants_per_clan=5,
        iterations=20,
        max_iterations=20,
        seed=42,
    )

    # Hủy ngay sau khởi tạo
    res_immediate = solve(problem, config, stop_requested=lambda: True)
    assert res_immediate.stopping_reason == "CANCELLED"
    assert res_immediate.iterations_completed == 0
    assert res_immediate.evaluations == config.population_size
    assert res_immediate.is_valid is True
    validate_route(res_immediate.best_route, problem.dimension)

    # Hủy giữa generation 1 (sau vài lần kiểm tra stop_requested)
    checks = 0

    def cancel_midway() -> bool:
        nonlocal checks
        checks += 1
        return checks >= 5

    res_mid = solve(problem, config, stop_requested=cancel_midway)
    assert res_mid.stopping_reason == "CANCELLED"
    assert res_mid.iterations_completed == 0
    assert res_mid.metadata["partial_iteration"] is True
    assert config.population_size < res_mid.evaluations < 2 * config.population_size
    assert res_mid.is_valid is True
    validate_route(res_mid.best_route, problem.dimension)


def test_time_limit_stops_early_with_valid_result():
    problem = load_matrix(DATA_DIR / "26Cities-937.txt")
    config = EHOConfig(
        clan_count=4,
        elephants_per_clan=15,
        iterations=500,
        max_iterations=500,
        time_limit_seconds=1e-9,
        seed=42,
    )
    result = solve(problem, config)
    assert result.stopping_reason == "TIME_LIMIT"
    assert result.iterations_completed < config.iterations
    assert result.is_valid is True
    validate_route(result.best_route, problem.dimension)
    assert result.best_distance == pytest.approx(problem.route_length(result.best_route))


def test_progress_callback_receives_frozen_stats_and_propagates_errors():
    problem = load_matrix(DATA_DIR / "06Cities-1248.txt")
    config = EHOConfig(
        clan_count=2,
        elephants_per_clan=4,
        iterations=4,
        max_iterations=4,
        record_history_every=2,
        seed=9,
    )
    received: list[IterationStat] = []
    result = solve(problem, config, progress_callback=received.append)

    assert tuple(received) == result.history
    assert all(isinstance(stat, IterationStat) for stat in received)

    def failing_callback(_stat: IterationStat) -> None:
        raise RuntimeError("callback boom")

    with pytest.raises(RuntimeError, match="callback boom"):
        solve(problem, config, progress_callback=failing_callback)


# ---------------------------------------------------------------------------
# 5. History invariants & Global best preservation
# ---------------------------------------------------------------------------


def test_history_invariants_and_monotonic_best_so_far():
    problem = load_matrix(DATA_DIR / "15Cities-1194.txt")
    config = EHOConfig(
        clan_count=3,
        elephants_per_clan=8,
        iterations=15,
        max_iterations=15,
        record_history_every=3,
        seed=123,
    )
    result = solve(problem, config)

    assert len(result.history) >= 2
    assert result.history[0].iteration == 0
    assert result.history[0].evaluations == config.population_size
    assert result.history[-1].iteration == result.iterations_completed
    assert result.history[-1].evaluations == result.evaluations
    assert result.history[-1].best_so_far == pytest.approx(result.best_distance)

    for prev, curr in zip(result.history, result.history[1:]):
        assert curr.best_so_far <= prev.best_so_far + 1e-12
        assert curr.evaluations >= prev.evaluations
        assert curr.iteration >= prev.iteration

    for stat in result.history:
        assert stat.best_so_far <= stat.best_current + 1e-12
        assert stat.best_current <= stat.mean_fitness + 1e-12
        assert stat.population_diversity is None


def test_preserve_global_best_helper_and_end_to_end():
    # Kiểm thử trực tiếp helper _preserve_global_best
    clan0 = Clan(((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 2, 1)), (100.0, 200.0, 150.0))
    clan1 = Clan(((0, 1, 3, 2), (0, 2, 3, 1), (0, 3, 1, 2)), (120.0, 220.0, 160.0))
    archive_route = (0, 1, 3, 2)
    archive_cost = 50.0

    updated = _preserve_global_best([clan0, clan1], archive_route, archive_cost)
    # Bảo toàn leader cũ của clan0 (index 0) và thay worst (index 1) bằng archive_route
    assert updated[0].members[0] == (0, 1, 2, 3)
    assert updated[0].members[1] == archive_route
    assert updated[0].costs[1] == archive_cost

    # Kiểm thử end-to-end với beta=1.0 (matriarch bị kéo mạnh về medoid) và separation lớn:
    # best_so_far vẫn phải được bảo toàn, không bao giờ tăng.
    problem = load_matrix(DATA_DIR / "15Cities-1194.txt")
    config = EHOConfig(
        clan_count=2,
        elephants_per_clan=6,
        iterations=12,
        max_iterations=12,
        alpha=0.2,
        beta=1.0,
        separation_count_per_clan=4,
        preserve_global_best=True,
        seed=77,
    )
    result = solve(problem, config)
    best_values = [stat.best_so_far for stat in result.history]
    assert best_values == sorted(best_values, reverse=True)
    assert result.best_distance == pytest.approx(problem.route_length(result.best_route))


# ---------------------------------------------------------------------------
# 6. Parent immutability across all EHO operators
# ---------------------------------------------------------------------------


def test_parent_immutability_across_all_eho_operators():
    n = 15
    rng = Random(42)
    clan_list = [list(random_permutation(n, rng)) for _ in range(6)]
    costs_list = [float(i * 10 + 5) for i in range(6)]

    clan_snapshot = [route.copy() for route in clan_list]
    costs_snapshot = costs_list.copy()

    _ = hamming_distance(clan_list[0], clan_list[1])
    _ = move_toward_best(clan_list[0], clan_list[1], 0.7, Random(1))
    _ = update_matriarch(clan_list[1], clan_list[2], 0.3, Random(2))
    _ = separate(clan_list, costs_list, 2, n, Random(3), protected_indices=(0,))

    clan_obj = Clan(clan_list, costs_list)
    _ = clan_obj.best_index()
    _ = clan_obj.worst_indices(2, protected_indices=(0,))
    _ = clan_obj.center_index()
    _ = clan_obj.center()

    assert clan_list == clan_snapshot
    assert costs_list == costs_snapshot
