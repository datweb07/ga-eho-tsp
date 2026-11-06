from random import Random
from ...domain.objective import Route


def mutate(route: Route, rate: float, rng: Random, method: str = "inversion") -> Route:
    """Một xác suất/cá thể; đảo đoạn gồm cả hai đầu, không sửa parent."""
    if method not in {"inversion", "swap", "insertion", "scramble"}:
        raise ValueError("Mutation không được hỗ trợ.")
    if rng.random() >= rate:
        return tuple(route)
    result = list(route)
    i, j = rng.sample(range(1, len(route)), 2)
    if method == "swap":
        result[i], result[j] = result[j], result[i]
    elif method == "insertion":
        result.insert(j, result.pop(i))
    else:
        i, j = sorted((i, j))
        segment = result[i:j+1]
        if method == "inversion":
            segment.reverse()
        else:
            rng.shuffle(segment)
        result[i:j+1] = segment
    return tuple(result)
