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
        values = [city for city in second[right:] + second[:right] if city not in used]
        positions = list(range(right, len(first))) + list(range(left))
        for position, value in zip(positions, values):
            result[position] = value
        return (0, *result)

    return child(a, b), child(b, a)


def partially_mapped_crossover(
    parent1: Route, parent2: Route, rng: Random
) -> tuple[Route, Route]:
    """PMX trên tail: giữ segment, giải collision bằng chuỗi ánh xạ A→B."""
    first, second = parent1[1:], parent2[1:]
    left, right = sorted(rng.sample(range(len(first)), 2))
    right += 1

    def child(kept: Route, donor: Route) -> Route:
        result = list(donor)
        result[left:right] = kept[left:right]
        mapping = dict(zip(kept[left:right], donor[left:right]))
        for index in (*range(left), *range(right, len(kept))):
            city = donor[index]
            while city in mapping:
                city = mapping[city]
            result[index] = city
        return (0, *result)

    return child(first, second), child(second, first)
