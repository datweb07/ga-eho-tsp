"""Schema dùng chung cho GA và EHO; không import bất kỳ solver nào."""

from dataclasses import dataclass, field
from math import isfinite
from types import MappingProxyType
from typing import Any, Mapping

from .objective import Matrix, Route, route_length, validate_matrix


def integer(name: str, value: int, minimum: int = 1) -> None:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} phải là số nguyên >= {minimum}.")


def probability(name: str, value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value) or not 0 <= value <= 1:
        raise ValueError(f"{name} phải nằm trong [0, 1].")


@dataclass(frozen=True)
class TSPProblem:
    name: str
    distance_matrix: Matrix
    source: str = "user"
    coordinates: tuple[tuple[float, float], ...] | None = None
    known_optimum: float | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        try:
            matrix = tuple(tuple(row) for row in self.distance_matrix)
            validate_matrix(matrix)
        except (TypeError, OverflowError) as error:
            raise ValueError("Ma trận phải chứa các số hữu hạn.") from error
        object.__setattr__(self, "distance_matrix", matrix)
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
        if self.known_optimum is not None and (not isfinite(self.known_optimum) or self.known_optimum < 0):
            raise ValueError("Known optimum phải hữu hạn, không âm và có nguồn kiểm chứng.")
        if self.coordinates is not None:
            coords = tuple(tuple(point) for point in self.coordinates)
            if len(coords) != self.dimension or any(len(p) != 2 or not all(isfinite(v) for v in p) for p in coords):
                raise ValueError("Tọa độ phải có n cặp số hữu hạn.")
            object.__setattr__(self, "coordinates", coords)

    @property
    def dimension(self) -> int:
        return len(self.distance_matrix)

    def route_length(self, route: Route) -> float:
        return route_length(route, self.distance_matrix)


@dataclass(frozen=True, kw_only=True)
class RunConfigBase:
    seed: int = 42
    max_iterations: int = 250
    max_evaluations: int | None = None
    time_limit_seconds: float | None = None
    record_history_every: int = 1

    def __post_init__(self) -> None:
        integer("seed", self.seed, 0)
        integer("max_iterations", self.max_iterations)
        integer("record_history_every", self.record_history_every)
        if self.max_evaluations is not None:
            integer("max_evaluations", self.max_evaluations)
        if self.time_limit_seconds is not None and (isinstance(self.time_limit_seconds, bool)
                or not isinstance(self.time_limit_seconds, (int, float))
                or not isfinite(self.time_limit_seconds) or self.time_limit_seconds <= 0):
            raise ValueError("time_limit_seconds phải hữu hạn và > 0.")


@dataclass(frozen=True, kw_only=True)
class GAConfig(RunConfigBase):
    population_size: int = 80
    generations: int = 250
    selection_method: str = "tournament"
    tournament_size: int = 3
    crossover_method: str = "ox"
    crossover_rate: float = 0.9
    mutation_method: str = "inversion"
    mutation_rate: float = 0.15
    elite_count: int = 2
    initialization_method: str = "random"
    local_search_enabled: bool = False
    local_search_max_moves: int = 0
    nn_seed_fraction: float = 0.25
    stagnation_patience: int | None = None
    adaptive_mutation: bool = False
    adaptive_min_rate: float = 0.05
    adaptive_max_rate: float = 0.5
    adaptive_patience: int = 20
    local_search_max_probes: int = 20

    def __post_init__(self) -> None:
        super().__post_init__()
        integer("population_size", self.population_size, 4)
        integer("generations", self.generations)
        integer("tournament_size", self.tournament_size, 2)
        integer("elite_count", self.elite_count, 0)
        integer("local_search_max_moves", self.local_search_max_moves, 0)
        if self.tournament_size > self.population_size or self.elite_count >= self.population_size:
            raise ValueError("tournament_size <= population_size và elite_count < population_size.")
        if self.max_evaluations is not None and self.max_evaluations < self.population_size:
            raise ValueError("max_evaluations phải đủ đánh giá quần thể khởi tạo.")
        probability("crossover_rate", self.crossover_rate)
        probability("mutation_rate", self.mutation_rate)
        probability("nn_seed_fraction", self.nn_seed_fraction)
        probability("adaptive_min_rate", self.adaptive_min_rate)
        probability("adaptive_max_rate", self.adaptive_max_rate)
        integer("adaptive_patience", self.adaptive_patience)
        integer("local_search_max_probes", self.local_search_max_probes)
        if type(self.adaptive_mutation) is not bool or self.adaptive_min_rate > self.adaptive_max_rate:
            raise ValueError("Adaptive mutation cần bool, 0 <= min_rate <= max_rate <= 1.")
        if self.stagnation_patience is not None:
            integer("stagnation_patience", self.stagnation_patience)
        if not isinstance(self.selection_method, str) or self.selection_method not in {"tournament", "rank", "roulette_wheel"}:
            raise ValueError("Selection hỗ trợ tournament, rank, roulette_wheel.")
        if self.crossover_method not in ("ox", "pmx") or not isinstance(self.mutation_method, str) or self.mutation_method not in {"inversion", "swap", "insertion", "scramble"}:
            raise ValueError("Crossover: ox/pmx; mutation: inversion/swap/insertion/scramble.")
        if self.initialization_method not in ("random", "nearest_neighbor", "mixed"):
            raise ValueError("Initialization: random/nearest_neighbor/mixed.")
        if type(self.local_search_enabled) is not bool:
            raise ValueError("local_search_enabled phải là bool.")
        if self.local_search_enabled and self.local_search_max_moves < 1:
            raise ValueError("2-opt cần local_search_max_moves >= 1.")
        if not self.local_search_enabled and self.local_search_max_moves != 0:
            raise ValueError("Local search OFF yêu cầu local_search_max_moves=0.")


@dataclass(frozen=True, kw_only=True)
class EHOConfig(RunConfigBase):
    """Chỉ là schema cho giai đoạn EHO; chưa có thuật toán."""
    clan_count: int = 4
    elephants_per_clan: int = 20
    iterations: int = 250
    alpha: float = 0.7
    beta: float = 0.3
    separation_count_per_clan: int = 1
    initialization_method: str = "random"
    preserve_global_best: bool = True

    @property
    def population_size(self) -> int:
        return self.clan_count * self.elephants_per_clan

    def __post_init__(self) -> None:
        super().__post_init__()
        integer("clan_count", self.clan_count, 2)
        integer("elephants_per_clan", self.elephants_per_clan, 3)
        integer("iterations", self.iterations)
        integer("separation_count_per_clan", self.separation_count_per_clan)
        probability("alpha", self.alpha)
        probability("beta", self.beta)
        if self.separation_count_per_clan >= self.elephants_per_clan:
            raise ValueError("separation_count_per_clan phải nhỏ hơn kích thước clan.")
        if self.initialization_method != "random" or self.preserve_global_best is not True:
            raise ValueError("Baseline EHO dùng random và preserve_global_best=True.")
        if self.max_evaluations is not None and self.max_evaluations < self.population_size:
            raise ValueError("max_evaluations phải đủ khởi tạo EHO.")


@dataclass(frozen=True)
class IterationStat:
    iteration: int
    best_current: float
    best_so_far: float
    mean_fitness: float
    evaluations: int
    elapsed_seconds: float
    population_diversity: float | None = None


@dataclass(frozen=True)
class RunResult:
    algorithm: str
    problem_name: str
    best_route: Route
    best_distance: float
    iterations_completed: int
    evaluations: int
    elapsed_seconds: float
    seed: int
    history: tuple[IterationStat, ...]
    config_snapshot: dict[str, Any]
    stopping_reason: str
    is_valid: bool
    metadata: dict[str, Any] = field(default_factory=dict)
