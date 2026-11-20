"""Kiểm thử tính tái lập (reproducibility) và độc lập RNG cho Discrete EHO."""

from pathlib import Path
import random
import pytest

from ga_eho_tsp.algorithms.eho import solve
from ga_eho_tsp.data.matrix_loader import load_matrix
from ga_eho_tsp.domain.models import EHOConfig, RunResult

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


def _numeric_history(result: RunResult) -> list[tuple]:
    return [
        (
            stat.iteration,
            stat.best_current,
            stat.best_so_far,
            stat.mean_fitness,
            stat.evaluations,
            stat.population_diversity,
        )
        for stat in result.history
    ]


@pytest.mark.parametrize("filename", ["06Cities-1248.txt", "15Cities-1194.txt", "48Cities-33523.txt"])
def test_same_seed_produces_identical_results_and_history(filename):
    problem = load_matrix(DATA_DIR / filename)
    config = EHOConfig(
        clan_count=3,
        elephants_per_clan=8,
        iterations=10,
        max_iterations=10,
        alpha=0.7,
        beta=0.3,
        separation_count_per_clan=1,
        seed=42,
    )
    first = solve(problem, config)
    second = solve(problem, config)

    assert first.best_route == second.best_route
    assert first.best_distance == second.best_distance
    assert first.evaluations == second.evaluations
    assert first.iterations_completed == second.iterations_completed
    assert first.stopping_reason == second.stopping_reason
    assert first.seed == second.seed
    assert first.config_snapshot == second.config_snapshot
    assert first.metadata == second.metadata
    assert _numeric_history(first) == _numeric_history(second)


def test_eho_is_independent_of_global_random_state():
    problem = load_matrix(DATA_DIR / "15Cities-1194.txt")
    config = EHOConfig(
        clan_count=2,
        elephants_per_clan=6,
        iterations=8,
        max_iterations=8,
        seed=2026,
    )

    random.seed(9999)
    global_before = random.getstate()
    first = solve(problem, config)
    global_after = random.getstate()

    # Solver không được chạm vào trạng thái RNG toàn cục
    assert global_before == global_after

    # Thay đổi RNG toàn cục giữa hai lần chạy không ảnh hưởng kết quả EHO
    random.seed(123456)
    _ = [random.random() for _ in range(100)]
    second = solve(problem, config)

    assert first.best_route == second.best_route
    assert first.best_distance == second.best_distance
    assert first.evaluations == second.evaluations
    assert _numeric_history(first) == _numeric_history(second)


def test_different_seeds_produce_distinct_trajectories():
    problem = load_matrix(DATA_DIR / "15Cities-1194.txt")
    histories = []
    routes = set()
    for seed in (1, 2, 42, 99):
        config = EHOConfig(
            clan_count=2,
            elephants_per_clan=8,
            iterations=10,
            max_iterations=10,
            seed=seed,
        )
        res = solve(problem, config)
        histories.append(_numeric_history(res))
        routes.add(res.best_route)

    assert len(routes) > 1
    assert len({tuple(h) for h in histories}) > 1


def test_reproducibility_under_partial_iteration_budget():
    problem = load_matrix(DATA_DIR / "15Cities-1194.txt")
    config = EHOConfig(
        clan_count=2,
        elephants_per_clan=10,
        iterations=15,
        max_iterations=15,
        max_evaluations=50,
        seed=77,
    )
    first = solve(problem, config)
    second = solve(problem, config)

    assert first.metadata["partial_iteration"] is True
    assert first.best_route == second.best_route
    assert first.best_distance == second.best_distance
    assert first.evaluations == second.evaluations == 50
    assert first.iterations_completed == second.iterations_completed
    assert _numeric_history(first) == _numeric_history(second)


@pytest.mark.parametrize("filename", ALL_DATASETS)
def test_reproducibility_smoke_across_all_datasets(filename):
    problem = load_matrix(DATA_DIR / filename)
    config = EHOConfig(
        clan_count=2,
        elephants_per_clan=5,
        iterations=4,
        max_iterations=4,
        seed=42,
    )
    first = solve(problem, config)
    second = solve(problem, config)

    assert first.best_route == second.best_route
    assert first.best_distance == second.best_distance
    assert first.evaluations == second.evaluations
    assert _numeric_history(first) == _numeric_history(second)
