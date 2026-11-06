"""Progress chỉ nhận snapshot; callback không can thiệp quần thể."""

from collections.abc import Callable
from typing import Protocol, TypeVar

from .models import GAConfig, EHOConfig, IterationStat, RunResult, TSPProblem

ProgressCallback = Callable[[IterationStat], None]
StopRequested = Callable[[], bool]
Config = TypeVar("Config", GAConfig, EHOConfig, contravariant=True)


class Solver(Protocol[Config]):
    def __call__(self, problem: TSPProblem, config: Config, *,
                 progress_callback: ProgressCallback | None = None,
                 stop_requested: StopRequested | None = None) -> RunResult: ...
