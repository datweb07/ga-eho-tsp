"""Điều phối solver bằng thread/queue, hoàn toàn không import Tk."""

from dataclasses import dataclass
from pathlib import Path
from queue import Empty, Queue
from threading import Event, Thread
from time import perf_counter
import traceback
from typing import Any

from ..algorithms.ga import solve
from ..domain.models import EHOConfig, GAConfig, IterationStat, TSPProblem
from ..domain.protocols import Solver


@dataclass(frozen=True)
class AlgorithmEntry:
    """Điểm đăng ký solver thật; None biểu thị chưa triển khai."""

    label: str
    config_type: type[GAConfig] | type[EHOConfig]
    solver: Solver[Any] | None


ALGORITHMS = {
    "ga": AlgorithmEntry("Genetic Algorithm (GA)", GAConfig, solve),
    "eho": AlgorithmEntry("EHO — Đang phát triển, nhóm EHO sẽ bổ sung", EHOConfig, None),
}


def bundled_datasets() -> list[Path]:
    """Tìm data cạnh repo/package, độc lập cwd; wheel không kèm data dùng Duyệt."""
    root = Path(__file__).resolve().parents[3]
    return sorted((root / "data").glob("*.txt"))


class RunController:
    """Một job tại một thời điểm; chỉ main thread gọi start/drain/cancel.

    Progress để hiển thị được throttle, history đầy đủ vẫn do solver giữ.
    Queue terminal được drain sau khi thread thoát để không cho Run chồng.
    """

    def __init__(self) -> None:
        self.events: Queue[tuple[str, Any]] = Queue()
        self.stop_event = Event()
        self.thread: Thread | None = None
        self.active = False

    def start(self, algorithm: str, problem: TSPProblem, config: GAConfig | EHOConfig) -> None:
        if self.active:
            raise ValueError("Đang có tác vụ; hãy chờ kết thúc trước khi chạy tiếp.")
        entry = ALGORITHMS[algorithm]
        if entry.solver is None:
            raise ValueError("EHO đang phát triển — chưa có solver để chạy.")
        if not isinstance(config, entry.config_type):
            raise ValueError("Schema cấu hình không khớp thuật toán.")
        self.stop_event.clear()
        self.active = True
        self.thread = Thread(target=self._run, args=(entry, problem, config), daemon=False,
                             name="tsp-solver")
        try:
            self.thread.start()
        except RuntimeError:
            self.active = False
            raise

    def _run(self, entry: AlgorithmEntry, problem: TSPProblem, config: Any) -> None:
        last_sent = float("-inf")

        def progress(stat: IterationStat) -> None:
            nonlocal last_sent
            now = perf_counter()
            if now - last_sent >= 0.15:
                self.events.put(("progress", stat))
                last_sent = now

        try:
            result = entry.solver(problem, config, progress_callback=progress,
                                  stop_requested=self.stop_event.is_set)
        except Exception as error:
            # Hiện lỗi thật trên UI; traceback lưu trong tab Chi tiết.
            self.events.put(("error", (str(error), traceback.format_exc())))
        else:
            self.events.put(("result", result))

    def cancel(self) -> None:
        self.stop_event.set()

    def drain(self) -> list[tuple[str, Any]]:
        items = []
        while True:
            try:
                item = self.events.get_nowait()
            except Empty:
                break
            if item[0] in ("result", "error"):
                if self.thread is not None and self.thread.is_alive():
                    self.events.put(item)
                    break
                self.active = False
            items.append(item)
        return items
