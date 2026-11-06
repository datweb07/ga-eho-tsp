"""Selection minimization; chuẩn bị distribution một lần mỗi generation."""

from dataclasses import dataclass
from itertools import accumulate
from random import Random

from ...domain.objective import Route


@dataclass
class PreparedSelection:
    population: list[Route]
    costs: list[float]
    method: str
    tournament_size: int
    indices: list[int]
    cumulative_weights: list[float] | None

    def pick(self, rng: Random) -> Route:
        """Chỉ RNG thay đổi; population/costs/distribution không bị sửa."""
        if self.method == "tournament":
            indices = rng.sample(range(len(self.population)), self.tournament_size)
            return self.population[min(indices, key=lambda index: self.costs[index])]
        if self.cumulative_weights is None:
            return rng.choice(self.population)
        index = rng.choices(self.indices, cum_weights=self.cumulative_weights, k=1)[0]
        return self.population[index]


def prepare_selection(
    population: list[Route], costs: list[float], method: str = "tournament",
    tournament_size: int = 3,
) -> PreparedSelection:
    """Inputs hợp lệ và giữ nguyên đến hết generation; không dùng RNG lúc prepare."""
    indices = list(range(len(population)))
    cumulative = None
    if method == "rank":
        indices.sort(key=lambda index: costs[index])
        cumulative = list(accumulate(range(len(indices), 0, -1)))
    elif method == "roulette_wheel":
        maximum = max(costs)
        weights = [1.0 if maximum == 0 else 1.0-cost/maximum for cost in costs]
        if any(weights):
            cumulative = list(accumulate(weights))
    elif method != "tournament":
        raise ValueError("Selection không được hỗ trợ.")
    return PreparedSelection(population, costs, method, tournament_size, indices, cumulative)


def select_parent(
    population: list[Route], costs: list[float], rng: Random,
    method: str = "tournament", tournament_size: int = 3,
) -> Route:
    """API một lần chọn tương thích P0; solver dùng prepare_selection mỗi generation."""
    return prepare_selection(population, costs, method, tournament_size).pick(rng)
