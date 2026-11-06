from random import Random
from ...domain.objective import Route


def select_parent(population: list[Route], costs: list[float], rng: Random,
                  method: str = "tournament", tournament_size: int = 3) -> Route:
    """Chọn một bố/mẹ, có hoàn lại giữa các lần gọi; không sửa costs."""
    if method == "tournament":
        indices = rng.sample(range(len(population)), tournament_size)
        return population[min(indices, key=lambda i: costs[i])]
    if method == "rank":
        indices = sorted(range(len(population)), key=lambda i: costs[i])
        return population[rng.choices(indices, weights=range(len(indices), 0, -1), k=1)[0]]
    if method == "roulette_wheel":
        # Scale trước khi cộng để tránh overflow; ties => chọn đều.
        maximum = max(costs)
        weights = [1.0 if maximum == 0 else 1.0 - cost / maximum for cost in costs]
        if not any(weights):
            return rng.choice(population)
        return rng.choices(population, weights=weights, k=1)[0]
    raise ValueError("Selection không được hỗ trợ.")
