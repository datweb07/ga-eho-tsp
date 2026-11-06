from random import Random
from ...domain.objective import Route


def order_crossover(parent1: Route, parent2: Route, rng: Random) -> tuple[Route, Route]:
    """OX hai điểm trên tail; fill vòng từ sau đoạn cắt; parent bất biến."""
    a, b = parent1[1:], parent2[1:]
    left, right = sorted(rng.sample(range(len(a)), 2))
    right += 1

    def child(first: Route, second: Route) -> Route:
        result = [-1] * len(first)
        result[left:right] = first[left:right]
        used = set(first[left:right])
        values = [second[(right+i) % len(second)] for i in range(len(second))
                  if second[(right+i) % len(second)] not in used]
        positions = [(right+i) % len(first) for i in range(len(first))
                     if result[(right+i) % len(first)] == -1]
        for position, value in zip(positions, values):
            result[position] = value
        return (0, *result)

    return child(a, b), child(b, a)
