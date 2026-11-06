from random import Random
from ...domain.objective import Route
from ...domain.operators import random_permutation
from ...domain.models import TSPProblem


def nearest_neighbor(problem: TSPProblem, start: int) -> Route:
    """Tham lam từ start, tie theo city nhỏ nhất; rotate để city 0 đứng đầu."""
    remaining = set(range(problem.dimension))
    remaining.remove(start)
    route = [start]
    while remaining:
        row = problem.distance_matrix[route[-1]]
        city = min(remaining, key=lambda candidate: (row[candidate], candidate))
        route.append(city)
        remaining.remove(city)
    zero = route.index(0)
    return tuple(route[zero:] + route[:zero])


def initialize(
    dimension: int, population_size: int, rng: Random, *,
    problem: TSPProblem | None = None, method: str = "random",
    nn_seed_fraction: float = 0.25,
) -> list[Route]:
    """Random mặc định; NN đa start hoặc mixed floor(P×fraction), không ép unique."""
    if method == "random":
        return [random_permutation(dimension, rng) for _ in range(population_size)]
    if method not in ("nearest_neighbor", "mixed") or problem is None:
        raise ValueError("Khởi tạo NN/mixed cần TSPProblem hợp lệ.")
    count = population_size if method == "nearest_neighbor" else int(population_size * nn_seed_fraction)
    routes: list[Route] = []
    while len(routes) < count:
        starts = rng.sample(range(dimension), dimension)
        for start in starts[:count-len(routes)]:
            routes.append(nearest_neighbor(problem, start))
    routes.extend(random_permutation(dimension, rng) for _ in range(population_size-count))
    return routes
