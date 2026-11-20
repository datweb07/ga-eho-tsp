"""Cấu trúc clan và phép tính medoid cho Discrete EHO trên TSP."""

from collections.abc import Sequence
from dataclasses import dataclass
from math import isfinite

from ...domain.objective import Route, validate_route
from .discrete_ops import hamming_distance


@dataclass(frozen=True)
class Clan:
    """Một clan bất biến với route và chi phí được ghép theo cùng index."""

    members: tuple[Route, ...]
    costs: tuple[float, ...]

    def __post_init__(self) -> None:
        if (not isinstance(self.members, Sequence)
                or isinstance(self.members, (str, bytes))):
            raise ValueError("members phải là danh sách route hợp lệ.")
        if (not isinstance(self.costs, Sequence)
                or isinstance(self.costs, (str, bytes))):
            raise ValueError("costs phải là danh sách chi phí hợp lệ.")

        try:
            members = tuple(tuple(route) for route in self.members)
        except TypeError as error:
            raise ValueError("Mỗi member phải là một route hợp lệ.") from error
        costs = tuple(self.costs)

        if not members:
            raise ValueError("Clan không được rỗng.")
        if len(costs) != len(members):
            raise ValueError("Số route và số chi phí trong clan phải bằng nhau.")

        dimension = len(members[0])
        for route in members:
            validate_route(route, dimension)
        normalized_costs: list[float] = []
        for cost in costs:
            if isinstance(cost, bool) or not isinstance(cost, (int, float)):
                raise ValueError("Mọi chi phí trong clan phải hữu hạn và không âm.")
            try:
                numeric_cost = float(cost)
            except OverflowError as error:
                raise ValueError("Mọi chi phí trong clan phải hữu hạn và không âm.") from error
            if not isfinite(numeric_cost) or numeric_cost < 0:
                raise ValueError("Mọi chi phí trong clan phải hữu hạn và không âm.")
            normalized_costs.append(numeric_cost)

        object.__setattr__(self, "members", members)
        object.__setattr__(self, "costs", tuple(normalized_costs))

    @property
    def size(self) -> int:
        """Số voi trong clan."""
        return len(self.members)

    @property
    def dimension(self) -> int:
        """Số thành phố của mỗi route."""
        return len(self.members[0])

    def best_index(self) -> int:
        """Trả index của route tốt nhất; hòa chi phí ưu tiên index nhỏ."""
        return min(range(self.size), key=lambda index: (self.costs[index], index))

    def worst_indices(
        self,
        count: int = 1,
        *,
        protected_indices: Sequence[int] = (),
    ) -> tuple[int, ...]:
        """Chọn `count` route tệ nhất, bỏ qua index được bảo vệ.

        Chi phí cao hơn được chọn trước; khi hòa, index nhỏ hơn được chọn
        trước để giữ kết quả xác định.
        """
        if type(count) is not int or count < 0:
            raise ValueError("count phải là số nguyên không âm.")
        if (not isinstance(protected_indices, Sequence)
                or isinstance(protected_indices, (str, bytes))):
            raise ValueError("protected_indices phải là dãy index.")

        protected: set[int] = set()
        for index in protected_indices:
            if type(index) is not int or not 0 <= index < self.size:
                raise ValueError("Index được bảo vệ phải thuộc phạm vi clan.")
            protected.add(index)

        eligible = [index for index in range(self.size) if index not in protected]
        if count > len(eligible):
            raise ValueError("count vượt số member không được bảo vệ.")
        return tuple(sorted(eligible, key=lambda index: (-self.costs[index], index))[:count])

    def center_index(self) -> int:
        """Trả index medoid theo tổng Hamming distance trong clan.

        Khi tổng khoảng cách bằng nhau, ưu tiên chi phí TSP thấp hơn rồi
        index nhỏ hơn. Khoảng cách tính trên các vị trí sau city 0.
        """
        distance_totals = [0] * self.size
        for first in range(self.size):
            for second in range(first + 1, self.size):
                distance = hamming_distance(self.members[first], self.members[second])
                distance_totals[first] += distance
                distance_totals[second] += distance

        return min(
            range(self.size),
            key=lambda index: (distance_totals[index], self.costs[index], index),
        )

    def center(self) -> Route:
        """Trả route medoid của clan."""
        return self.members[self.center_index()]
