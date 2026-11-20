"""Discrete elephant herding optimization for permutation TSP."""

from dataclasses import asdict
from math import fsum
from random import Random
from time import perf_counter

from ... import __version__
from ...domain.models import EHOConfig, IterationStat, RunResult, TSPProblem
from ...domain.objective import Route, validate_route
from ...domain.operators import random_permutation
from ...domain.protocols import ProgressCallback, StopRequested
from .clans import Clan
from .discrete_ops import move_toward_best, update_matriarch
from .separation import separate


def _preserve_global_best(
    clans: list[Clan],
    best_route: Route,
    best_distance: float,
) -> list[Clan]:
    """Đưa nghiệm tốt nhất vào clan đầu mà không loại matriarch của clan."""
    first = clans[0]
    if best_route in first.members:
        return clans

    leader_index = first.best_index()
    replacement_index = first.worst_indices(1, protected_indices=(leader_index,))[0]
    members = list(first.members)
    costs = list(first.costs)
    members[replacement_index] = best_route
    costs[replacement_index] = best_distance
    clans[0] = Clan(tuple(members), tuple(costs))
    return clans


def solve(
    problem: TSPProblem,
    config: EHOConfig,
    *,
    progress_callback: ProgressCallback | None = None,
    stop_requested: StopRequested | None = None,
) -> RunResult:
    """Tối ưu tour bằng cập nhật clan, medoid rời rạc và separation.

    Mỗi generation đọc clans hiện tại và tạo clans mới. Nếu dừng giữa
    generation, các candidate đã đánh giá vẫn có thể cải thiện archive,
    nhưng quần thể chưa hoàn tất không được commit.
    """
    if not isinstance(problem, TSPProblem):
        raise ValueError("EHO yêu cầu TSPProblem.")
    if not isinstance(config, EHOConfig):
        raise ValueError("EHO yêu cầu EHOConfig.")

    start = perf_counter()
    rng = Random(config.seed)
    clans: list[Clan] = []
    for _ in range(config.clan_count):
        members = tuple(
            random_permutation(problem.dimension, rng)
            for _ in range(config.elephants_per_clan)
        )
        costs = tuple(problem.route_length(route) for route in members)
        clans.append(Clan(members, costs))

    evaluations = config.population_size
    initial_candidates = [
        (clan.costs[index], clan.members[index])
        for clan in clans
        for index in range(clan.size)
    ]
    best_distance, best_route = min(initial_candidates, key=lambda item: item[0])

    history: list[IterationStat] = []
    completed = 0
    partial_iteration = False

    def record(iteration: int) -> None:
        costs = [cost for clan in clans for cost in clan.costs]
        stat = IterationStat(
            iteration=iteration,
            best_current=min(costs),
            best_so_far=best_distance,
            mean_fitness=fsum(costs) / len(costs),
            evaluations=evaluations,
            elapsed_seconds=perf_counter() - start,
            population_diversity=None,
        )
        history.append(stat)
        if progress_callback is not None:
            progress_callback(stat)

    def get_stop_reason() -> str | None:
        if stop_requested is not None and stop_requested():
            return "CANCELLED"
        if (config.time_limit_seconds is not None
                and perf_counter() - start >= config.time_limit_seconds):
            return "TIME_LIMIT"
        if config.max_evaluations is not None and evaluations >= config.max_evaluations:
            return "MAX_EVALUATIONS"
        return None

    record(0)
    stopping_reason = "MAX_ITERATIONS"
    iteration_limit = min(config.iterations, config.max_iterations)

    for iteration in range(1, iteration_limit + 1):
        stop_reason = get_stop_reason()
        if stop_reason is not None:
            stopping_reason = stop_reason
            break

        next_clans: list[Clan] = []
        partial_iteration = False

        for clan in clans:
            leader_index = clan.best_index()
            leader = clan.members[leader_index]
            center = clan.center()
            separated_indices = clan.worst_indices(
                config.separation_count_per_clan,
                protected_indices=(leader_index,),
            )
            separated_members = separate(
                clan.members,
                clan.costs,
                config.separation_count_per_clan,
                problem.dimension,
                rng,
                protected_indices=(leader_index,),
            )

            next_members: list[Route] = []
            next_costs: list[float] = []
            separated = set(separated_indices)

            for index, route in enumerate(clan.members):
                stop_reason = get_stop_reason()
                if stop_reason is not None:
                    stopping_reason = stop_reason
                    partial_iteration = True
                    break

                if index == leader_index:
                    candidate = update_matriarch(route, center, config.beta, rng)
                elif index in separated:
                    candidate = separated_members[index]
                else:
                    candidate = move_toward_best(route, leader, config.alpha, rng)

                cost = problem.route_length(candidate)
                evaluations += 1
                if cost < best_distance:
                    best_route, best_distance = candidate, cost
                next_members.append(candidate)
                next_costs.append(cost)

            if partial_iteration:
                break
            next_clans.append(Clan(tuple(next_members), tuple(next_costs)))

        if partial_iteration:
            break

        clans = next_clans
        if config.preserve_global_best:
            clans = _preserve_global_best(clans, best_route, best_distance)

        completed = iteration
        if iteration % config.record_history_every == 0:
            record(iteration)

    if (not history or history[-1].iteration != completed
            or history[-1].evaluations != evaluations):
        record(completed)

    validate_route(best_route, problem.dimension)
    return RunResult(
        algorithm="eho",
        problem_name=problem.name,
        best_route=best_route,
        best_distance=best_distance,
        iterations_completed=completed,
        evaluations=evaluations,
        elapsed_seconds=perf_counter() - start,
        seed=config.seed,
        history=tuple(history),
        config_snapshot=asdict(config),
        stopping_reason=stopping_reason,
        is_valid=True,
        metadata={
            "partial_iteration": partial_iteration,
            "version": __version__,
            "dataset_sha256": problem.metadata.get("sha256"),
            "initialization_atomic": True,
            "population_diversity": None,
            "clan_center": "hamming_medoid",
        },
    )
