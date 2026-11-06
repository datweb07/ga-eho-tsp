from random import Random
from ...domain.objective import Route
from ...domain.operators import random_permutation


def initialize(dimension: int, population_size: int, rng: Random) -> list[Route]:
    """Khởi tạo random-only; cho phép trùng giá trị tour ở bài nhỏ."""
    return [random_permutation(dimension, rng) for _ in range(population_size)]
