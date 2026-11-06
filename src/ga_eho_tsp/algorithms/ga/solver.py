"""Vòng lặp GA; không GUI, I/O hoặc RNG toàn cục."""

from dataclasses import asdict
from math import fsum
from random import Random
from time import perf_counter

from ...domain.models import GAConfig, TSPProblem, IterationStat, RunResult
from ...domain.objective import validate_route
from ...domain.protocols import ProgressCallback, StopRequested
from .initialization import initialize
from .selection import select_parent
from .crossover import order_crossover
from .mutation import mutate
from .survivor import select_elites


def solve(problem: TSPProblem, config: GAConfig, *,
          progress_callback: ProgressCallback | None = None,
          stop_requested: StopRequested | None = None) -> RunResult:
    """Trả best toàn lịch sử; interruption giữ candidate đã đánh giá, không vượt budget."""
    if not isinstance(config, GAConfig):
        raise ValueError("GA yêu cầu GAConfig.")
    start = perf_counter()
    rng = Random(config.seed)
    population = initialize(problem.dimension, config.population_size, rng)
    costs = [problem.route_length(route) for route in population]
    evaluations = len(population)
    best_index = min(range(len(population)), key=lambda i: costs[i])
    best_route, best_distance = population[best_index], costs[best_index]
    history: list[IterationStat] = []
    completed = 0

    def record(iteration: int) -> None:
        stat = IterationStat(iteration, min(costs), best_distance,
                             fsum(c / len(costs) for c in costs), evaluations,
                             perf_counter()-start)
        history.append(stat)
        if progress_callback is not None:
            progress_callback(stat)

    def should_stop() -> str | None:
        if stop_requested is not None and stop_requested():
            return "CANCELLED"
        if config.time_limit_seconds is not None and perf_counter()-start >= config.time_limit_seconds:
            return "TIME_LIMIT"
        if config.max_evaluations is not None and evaluations >= config.max_evaluations:
            return "MAX_EVALUATIONS"
        return None

    record(0)
    reason = "MAX_ITERATIONS"
    partial = False
    for iteration in range(1, min(config.generations, config.max_iterations)+1):
        stopped = should_stop()
        if stopped:
            reason = stopped
            break
        next_population, next_costs = select_elites(population, costs, config.elite_count)
        while len(next_population) < config.population_size:
            stopped = should_stop()
            if stopped:
                break
            first = select_parent(population, costs, rng, config.selection_method, config.tournament_size)
            second = select_parent(population, costs, rng, config.selection_method, config.tournament_size)
            children = order_crossover(first, second, rng) if rng.random() < config.crossover_rate else (first, second)
            for child in children:
                if len(next_population) == config.population_size:
                    break
                stopped = should_stop()
                if stopped:
                    break
                child = mutate(child, config.mutation_rate, rng, config.mutation_method)
                cost = problem.route_length(child)
                evaluations += 1
                next_population.append(child)
                next_costs.append(cost)
                if cost < best_distance:
                    best_route, best_distance = child, cost
            if stopped:
                break
        if stopped and len(next_population) < config.population_size:
            reason, partial = stopped, True
            break
        population, costs = next_population, next_costs
        completed = iteration
        if iteration % config.record_history_every == 0:
            record(iteration)
    # Luôn ghi trạng thái cuối; partial dùng population đã commit, archive gồm mọi evaluation.
    if history[-1].iteration != completed or history[-1].evaluations != evaluations:
        record(completed)
    validate_route(best_route, problem.dimension)
    return RunResult("ga", problem.name, best_route, best_distance, completed,
                     evaluations, perf_counter()-start, config.seed, tuple(history),
                     asdict(config), reason, True,
                     {"partial_iteration": partial, "version": "0.1.0",
                      "dataset_sha256": problem.metadata.get("sha256"),
                      "initialization_atomic": True})
