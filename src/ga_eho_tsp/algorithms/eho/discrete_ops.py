"""Toán tử cập nhật đàn rời rạc cho Discrete EHO (D-EHO) trên hoán vị TSP."""

from collections.abc import Sequence
from math import floor, isfinite
from random import Random

from ...domain.objective import Route, validate_route


def _validate_strength(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise ValueError(f"{name} phải là số thực hữu hạn trong [0, 1].")
    if not (0.0 <= value <= 1.0):
        raise ValueError(f"{name} phải nằm trong đoạn [0, 1].")
    return float(value)


def _validate_pair(first: Route, second: Route) -> int:
    if (
        not isinstance(first, Sequence)
        or isinstance(first, (str, bytes))
        or not isinstance(second, Sequence)
        or isinstance(second, (str, bytes))
    ):
        raise ValueError("Route phải là dãy số nguyên hợp lệ.")
    n = len(first)
    if n < 3:
        raise ValueError("Route phải có ít nhất 3 thành phố.")
    if len(second) != n:
        raise ValueError("Hai route phải có cùng số thành phố.")
    validate_route(first, n)
    validate_route(second, n)
    return n


def hamming_distance(a: Route, b: Route) -> int:
    """Số vị trí khác nhau trên đoạn đuôi (index 1..n-1) giữa hai route hợp lệ."""
    n = _validate_pair(a, b)
    return sum(1 for i in range(1, n) if a[i] != b[i])


def _guided_swap(source: Route, target: Route, strength: float, rng: Random) -> Route:
    """Dịch chuyển `source` về phía `target` bằng tối đa k phép swap có định hướng.

    Độ phức tạp O(n) nhờ bảng vị trí `pos`. Không chạm city 0 và không sửa input.
    Biên:
      - strength == 0.0 hoặc source == target -> trả về bản sao của source.
      - strength == 1.0 -> trả về bản sao của target.
      - 0 < strength < 1 -> k = floor(strength * r * HammingDistance(source, target)),
        thực hiện tối đa k bước swap ngẫu nhiên trên các vị trí sai khác.
    """
    n = _validate_pair(source, target)
    if strength == 0.0:
        return tuple(source)
    if strength == 1.0:
        return tuple(target)

    diff = [i for i in range(1, n) if source[i] != target[i]]
    if not diff:
        return tuple(source)

    steps = floor(strength * rng.random() * len(diff))
    if steps <= 0:
        return tuple(source)

    result = list(source)
    pos = [0] * n
    for idx, city in enumerate(result):
        pos[city] = idx

    rng.shuffle(diff)
    swaps_done = 0
    for i in diff:
        if swaps_done >= steps:
            break
        desired_city = target[i]
        current_city = result[i]
        if current_city == desired_city:
            continue
        j = pos[desired_city]
        result[i], result[j] = desired_city, current_city
        pos[desired_city] = i
        pos[current_city] = j
        swaps_done += 1

    return tuple(result)


def move_toward_best(
    current: Route,
    pbest: Route,
    alpha: float,
    rng: Random,
) -> Route:
    """Formula 12.1 (rời rạc): dịch chuyển voi `current` hướng về matriarch `pbest` với hệ số alpha."""
    strength = _validate_strength("alpha", alpha)
    return _guided_swap(current, pbest, strength, rng)


def update_matriarch(
    matriarch: Route,
    clan_center: Route,
    beta: float,
    rng: Random,
) -> Route:
    """Formula 12.2 (rời rạc): cập nhật matriarch hướng về tâm đàn (medoid) `clan_center` với hệ số beta."""
    strength = _validate_strength("beta", beta)
    return _guided_swap(matriarch, clan_center, strength, rng)
