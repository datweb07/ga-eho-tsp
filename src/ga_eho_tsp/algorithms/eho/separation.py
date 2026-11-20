"""Toán tử tách đàn (Separating Operator - Formula 12.4 rời rạc) cho Discrete EHO."""

from collections.abc import Sequence
from math import isfinite
from random import Random

from ...domain.objective import Route, validate_route
from ...domain.operators import random_permutation


def _validate_inputs(
    clan: Sequence[Route],
    costs: Sequence[float],
    separation_count: int,
    n: int,
    protected_indices: Sequence[int],
) -> int:
    if not isinstance(clan, Sequence) or isinstance(clan, (str, bytes)):
        raise ValueError("clan phải là danh sách các route hợp lệ.")
    if not isinstance(costs, Sequence) or isinstance(costs, (str, bytes)):
        raise ValueError("costs phải là danh sách chi phí hợp lệ.")
    clan_size = len(clan)
    if clan_size == 0:
        raise ValueError("clan không được rỗng.")
    if len(costs) != clan_size:
        raise ValueError("Độ dài clan và costs phải bằng nhau.")
    if type(n) is not int or n < 3:
        raise ValueError("Số thành phố n phải là số nguyên >= 3.")
    if type(separation_count) is not int or separation_count < 0 or separation_count > clan_size:
        raise ValueError(f"separation_count phải là số nguyên trong đoạn [0, {clan_size}].")
    if (not isinstance(protected_indices, Sequence)
            or isinstance(protected_indices, (str, bytes))):
        raise ValueError("protected_indices phải là dãy index.")

    protected: set[int] = set()
    for index in protected_indices:
        if type(index) is not int or not 0 <= index < clan_size:
            raise ValueError("Index được bảo vệ phải thuộc phạm vi clan.")
        protected.add(index)
    if separation_count > clan_size - len(protected):
        raise ValueError("separation_count vượt số member không được bảo vệ.")

    for route in clan:
        validate_route(route, n)
    for cost in costs:
        if isinstance(cost, bool) or not isinstance(cost, (int, float)) or not isfinite(cost) or cost < 0:
            raise ValueError("Mọi giá trị trong costs phải là số hữu hạn không âm.")
    return clan_size


def separate(
    clan: Sequence[Route],
    costs: Sequence[float],
    separation_count: int,
    n: int,
    rng: Random,
    *,
    protected_indices: Sequence[int] = (),
) -> list[Route]:
    """Thay các index tệ nhất theo `costs` bằng random routes mới.

    - Không sửa đổi `clan` và `costs` tại chỗ (parent immutability).
    - Giữ nguyên kích thước clan và đảm bảo mọi route trả về đều là hoán vị hợp lệ bắt đầu từ city 0.
    - Khi hòa cost, tie-break xác định theo chỉ số nhỏ hơn trước để đảm bảo reproducibility.
    - Có thể bảo vệ index matriarch; `costs` có thể là xếp hạng của clan cha để
      giữ vai trò đã chọn ổn định trong generation kế tiếp.
    """
    clan_size = _validate_inputs(clan, costs, separation_count, n, protected_indices)
    new_clan: list[Route] = [tuple(route) for route in clan]

    if separation_count == 0:
        return new_clan

    protected = set(protected_indices)
    eligible = [index for index in range(clan_size) if index not in protected]
    worst_indices = sorted(eligible, key=lambda i: (-costs[i], i))[:separation_count]
    for idx in worst_indices:
        new_clan[idx] = random_permutation(n, rng)

    return new_clan
