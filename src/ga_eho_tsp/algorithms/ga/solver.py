"""Vòng lặp GA; không GUI, I/O hoặc RNG toàn cục."""

from dataclasses import asdict
from math import fsum
from random import Random
from time import perf_counter

from ... import __version__
from ...domain.models import GAConfig, TSPProblem, IterationStat, RunResult
from ...domain.objective import validate_route
from ...domain.protocols import ProgressCallback, StopRequested
from .initialization import initialize
from .selection import prepare_selection
from .crossover import order_crossover, partially_mapped_crossover
from .monitoring import population_diversity, effective_mutation_rate
from .local_search import improve
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
    if config.initialization_method == "random":
        population = initialize(problem.dimension, config.population_size, rng)
    else:
        population = initialize(problem.dimension, config.population_size, rng, problem=problem,
                                method=config.initialization_method, nn_seed_fraction=config.nn_seed_fraction)
    costs = [problem.route_length(route) for route in population]
    evaluations = len(population)
    best_index = min(range(len(population)), key=lambda i: costs[i])
    best_route, best_distance = population[best_index], costs[best_index]
    history: list[IterationStat] = []
    completed = 0
    stagnation = 0
    mutation_rates: list[dict[str, object]] = []
    local_probes = 0
    local_moves = 0
    current_diversity = population_diversity(population) if config.adaptive_mutation else None
    crossover = order_crossover if config.crossover_method == "ox" else partially_mapped_crossover

    def record(iteration: int) -> None:
        stat = IterationStat(iteration, min(costs), best_distance,
                             fsum(c / len(costs) for c in costs), evaluations,
                             perf_counter()-start,
                             current_diversity if config.adaptive_mutation else population_diversity(population))
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

    def evaluate_candidate(route: tuple[int, ...]) -> float:
        nonlocal evaluations, best_route, best_distance
        cost = problem.route_length(route)
        evaluations += 1
        if cost < best_distance:
            best_route, best_distance = route, cost
        return cost

    record(0)
    reason = "MAX_ITERATIONS"
    partial = False
    for iteration in range(1, min(config.generations, config.max_iterations)+1):
        stopped = should_stop()
        if stopped:
            reason = stopped
            break
        next_population, next_costs = select_elites(population, costs, config.elite_count)
        selector = prepare_selection(population, costs, config.selection_method, config.tournament_size)
        previous_best = best_distance
        rate = effective_mutation_rate(config, stagnation, current_diversity or 0.0)
        if config.adaptive_mutation:
            mutation_rates.append({"iteration": iteration, "rate": rate, "completed": False})
        while len(next_population) < config.population_size:
            stopped = should_stop()
            if stopped:
                break
            first, second = selector.pick(rng), selector.pick(rng)
            children = crossover(first, second, rng) if rng.random() < config.crossover_rate else (first, second)
            for child in children:
                if len(next_population) == config.population_size:
                    break
                stopped = should_stop()
                if stopped:
                    break
                child = mutate(child, rate, rng, config.mutation_method)
                cost = evaluate_candidate(child)
                if config.local_search_enabled:
                    improved = improve(child, cost, evaluate=evaluate_candidate, should_stop=should_stop,
                                       max_moves=config.local_search_max_moves,
                                       max_probes=config.local_search_max_probes)
                    child, cost = improved.route, improved.cost
                    local_probes += improved.probes
                    local_moves += improved.accepted_moves
                    stopped = improved.stopping_reason
                next_population.append(child)
                next_costs.append(cost)
                if stopped:
                    break
            if stopped:
                break
        if stopped and len(next_population) < config.population_size:
            reason, partial = stopped, True
            break
        population, costs = next_population, next_costs
        completed = iteration
        stagnation = 0 if best_distance < previous_best else stagnation + 1
        if config.adaptive_mutation:
            mutation_rates[-1]["completed"] = True
            current_diversity = population_diversity(population)
        if iteration % config.record_history_every == 0:
            record(iteration)
        if config.stagnation_patience is not None and stagnation >= config.stagnation_patience:
            reason = "STAGNATION"
            break
    # Luôn ghi trạng thái cuối; partial dùng population đã commit, archive gồm mọi evaluation.
    if history[-1].iteration != completed or history[-1].evaluations != evaluations:
        record(completed)
    validate_route(best_route, problem.dimension)
    return RunResult("GA+2-opt" if config.local_search_enabled else "ga", problem.name, best_route, best_distance, completed,
                     evaluations, perf_counter()-start, config.seed, tuple(history),
                     asdict(config), reason, True,
                     {"partial_iteration": partial, "version": __version__,
                      "stagnation_iterations": stagnation,
                      "adaptive_mutation": config.adaptive_mutation,
                      "effective_mutation_rates": mutation_rates,
                      "local_search_full_evaluations": local_probes,
                      "local_search_accepted_moves": local_moves,
                      "dataset_sha256": problem.metadata.get("sha256"),
                      "initialization_atomic": True})
