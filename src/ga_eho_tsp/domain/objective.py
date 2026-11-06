"""Objective duy nhất cho symmetric TSP."""

from collections.abc import Sequence
from math import fsum, isfinite

Route = tuple[int, ...]
Matrix = tuple[tuple[float, ...], ...]


def validate_route(route: Sequence[int], dimension: int) -> None:
    """Từ chối route đóng vòng, sai kiểu, thiếu hoặc trùng city."""
    if (not isinstance(route, Sequence) or isinstance(route, (str, bytes))
            or len(route) != dimension or not route or route[0] != 0
            or any(type(city) is not int for city in route)
            or set(route) != set(range(dimension))):
        raise ValueError("Route phải là hoán vị 0..n-1, bắt đầu bằng 0, không khép vòng.")


def validate_matrix(matrix: Matrix) -> None:
    """Kiểm tra nguyên chính xác; số thực dùng abs tolerance 1e-9."""
    n = len(matrix)
    if n < 3 or any(len(row) != n for row in matrix):
        raise ValueError("Ma trận phải vuông với ít nhất 3 thành phố.")
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not isfinite(x) or x < 0 for row in matrix for x in row):
        raise ValueError("Khoảng cách phải hữu hạn và không âm.")
    for i in range(n):
        if matrix[i][i] != 0:
            raise ValueError("Đường chéo ma trận phải bằng 0.")
        for j in range(i):
            a, b = matrix[i][j], matrix[j][i]
            equal = a == b if isinstance(a, int) and isinstance(b, int) else abs(a-b) <= 1e-9
            if not equal:
                raise ValueError("Ma trận phải đối xứng (sai số tuyệt đối 1e-9 cho số thực).")


def route_length(route: Sequence[int], matrix: Matrix) -> float:
    """Tính từng cạnh và cạnh cuối về 0 đúng một lần; không sửa input."""
    validate_route(route, len(matrix))
    try:
        total = fsum(matrix[route[i]][route[(i+1) % len(route)]] for i in range(len(route)))
    except OverflowError as error:
        raise ValueError("Tổng khoảng cách vượt miền số hữu hạn.") from error
    if not isfinite(total):
        raise ValueError("Tổng khoảng cách vượt miền số hữu hạn.")
    return total
