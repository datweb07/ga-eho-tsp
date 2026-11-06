"""Bounded 2-opt: đánh giá FULL objective mỗi probe, không dùng delta ẩn."""

from collections.abc import Callable
from dataclasses import dataclass

from ...domain.objective import Route


@dataclass(frozen=True)
class LocalSearchResult:
    route: Route
    cost: float
    probes: int
    accepted_moves: int
    stopping_reason: str | None


def improve(
    route: Route, cost: float, *, evaluate: Callable[[Route], float],
    should_stop: Callable[[], str | None], max_moves: int, max_probes: int,
) -> LocalSearchResult:
    """First improvement theo i,j tăng dần; restart sau move, giữ 0 và parent."""
    probes, moves = 0, 0
    stopped = None
    while moves < max_moves and probes < max_probes:
        improved = False
        for left in range(1, len(route)-1):
            for right in range(left+1, len(route)):
                stopped = should_stop()
                if stopped or probes >= max_probes:
                    return LocalSearchResult(route, cost, probes, moves, stopped)
                candidate = route[:left] + route[left:right+1][::-1] + route[right+1:]
                candidate_cost = evaluate(candidate)
                probes += 1
                if candidate_cost < cost:
                    route, cost = candidate, candidate_cost
                    moves += 1
                    improved = True
                    break
            if improved:
                break
        if not improved:
            break
    return LocalSearchResult(route, cost, probes, moves, stopped)
