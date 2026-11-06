"""Phép cơ bản trên hoán vị dùng chung; không có policy solver."""

from random import Random
from .objective import Route


def random_permutation(dimension: int, rng: Random) -> Route:
    """Khóa city 0, shuffle phần đuôi bằng RNG được tiêm vào."""
    if type(dimension) is not int or dimension < 3:
        raise ValueError("Số thành phố phải là số nguyên >= 3.")
    tail = list(range(1, dimension))
    rng.shuffle(tail)
    return (0, *tail)
