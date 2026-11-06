"""Một cửa sổ Tk/ttk; tất cả thao tác widget/canvas nằm trên main thread."""

from dataclasses import asdict
import json
from pathlib import Path
import sys
from time import perf_counter
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from ..data.matrix_loader import load_matrix
from ..domain.models import GAConfig, IterationStat, RunResult, TSPProblem
from .controller import ALGORITHMS, RunController, bundled_datasets
from .controls import ConfigForm, preset_config
from .export import export_history, export_json
from .plots import SCHEMATIC, draw_history, draw_route


class Application:
    """Giữ snapshot problem/config của run, không chạm nội bộ GA."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.controller = RunController()
        self.problem: TSPProblem | None = None
        self.run_problem: TSPProblem | None = None
        self.result: RunResult | None = None
        self.closing = False
        self.live_history: list[IterationStat] = []
        self.started = 0.0
        self.last_live_plot = 0.0
        self.algorithm_keys = list(ALGORITHMS)
        self.dataset_paths = {p.name: p for p in bundled_datasets()}
        root.title("Đề tài 6 · GA–EHO–TSP | Genetic Algorithm")
        root.geometry("1240x720")
        root.minsize(1180, 640)
        root.protocol("WM_DELETE_WINDOW", self.request_close)
        style = ttk.Style(root)
        style.configure("Title.TLabel", font=("Segoe UI", 15, "bold"))
        style.configure("Action.TButton", padding=(12, 6))
        frame = ttk.Frame(root, padding=12)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Genetic Algorithm · Traveling Salesman Problem", style="Title.TLabel").pack(anchor="w")
        ttk.Label(frame, text="Đề tài 6 · GA hiện có · EHO đang phát triển · chi phí theo ma trận dữ liệu").pack(anchor="w", pady=(0, 8))
        panes = ttk.Panedwindow(frame, orient="horizontal")
        panes.pack(fill="both", expand=True)
        left, right = ttk.Frame(panes, width=410), ttk.Frame(panes)
        panes.add(left, weight=0)
        panes.add(right, weight=1)
        self._build_inputs(left)
        self._build_results(right)
        self.poll_id = root.after(100, self._poll)
        if self.dataset_paths:
            name = "15Cities-1194.txt" if "15Cities-1194.txt" in self.dataset_paths else next(iter(self.dataset_paths))
            self.dataset_var.set(name)
            self.select_dataset()
        else:
            self.dataset_info.set("Không tìm thấy data/ cạnh package. Hãy Duyệt file ma trận .txt.")
        self._update_actions()

    def _build_inputs(self, parent: ttk.Frame) -> None:
        dataset = ttk.LabelFrame(parent, text="1. Dataset TSP", padding=8)
        dataset.pack(fill="x", padx=(0, 10))
        self.dataset_var = tk.StringVar()
        self.dataset_box = ttk.Combobox(dataset, textvariable=self.dataset_var, values=list(self.dataset_paths), state="readonly")
        self.dataset_box.pack(side="top", fill="x")
        self.dataset_box.bind("<<ComboboxSelected>>", lambda event: self.select_dataset())
        self.browse_button = ttk.Button(dataset, text="Duyệt file .txt…", command=self.browse_dataset)
        self.browse_button.pack(anchor="w", pady=4)
        self.dataset_info = tk.StringVar()
        ttk.Label(dataset, textvariable=self.dataset_info, wraplength=390).pack(fill="x")
        self.algorithm_var = tk.StringVar(value=ALGORITHMS["ga"].label)
        self.algorithm_box = ttk.Combobox(parent, textvariable=self.algorithm_var,
                                         values=[a.label for a in ALGORITHMS.values()], state="readonly")
        self.algorithm_box.pack(fill="x", padx=(0, 10), pady=6)
        self.algorithm_box.bind("<<ComboboxSelected>>", lambda event: self._update_actions())
        presets = ttk.Frame(parent)
        presets.pack(fill="x", padx=(0, 10))
        self.preset_var = tk.StringVar(value="Mặc định")
        self.preset_box = ttk.Combobox(presets, textvariable=self.preset_var, state="readonly",
                                      values=("Demo nhanh", "Mặc định", "Giới hạn evaluations"), width=24)
        self.preset_box.pack(side="left", fill="x", expand=True)
        self.preset_box.bind("<<ComboboxSelected>>", lambda event: self.apply_preset())
        self.reset_button = ttk.Button(presets, text="Reset default", command=self.reset_defaults)
        self.reset_button.pack(side="left", padx=4)
        self.form = ConfigForm(parent)
        self.form.pack(fill="both", expand=True, padx=(0, 10), pady=6)
        self.variant = tk.StringVar(value="GA thuần · adaptive/2-opt OFF mặc định")
        ttk.Label(parent, textvariable=self.variant, wraplength=390, foreground="#8b4513").pack(fill="x")
        self.form.variables["local_search_enabled"].trace_add("write", lambda *args: self._variant_changed())
        self.form.variables["adaptive_mutation"].trace_add("write", lambda *args: self._variant_changed())

    def _build_results(self, parent: ttk.Frame) -> None:
        actions = ttk.Frame(parent)
        actions.pack(fill="x")
        self.run_button = ttk.Button(actions, text="Chạy GA", style="Action.TButton", command=self.start_run)
        self.run_button.pack(side="left")
        self.stop_button = ttk.Button(actions, text="Dừng", style="Action.TButton", command=self.stop_run)
        self.stop_button.pack(side="left", padx=6)
        self.export_buttons = []
        for label, kind in (("Lưu JSON", "json"), ("CSV history", "csv"), ("PNG tuyến", "route"), ("PNG hội tụ", "history")):
            button = ttk.Button(actions, text=label, command=lambda k=kind: self.save(k))
            button.pack(side="left", padx=2)
            self.export_buttons.append(button)
        self.status = tk.StringVar(value="Sẵn sàng")
        self.metrics = tk.StringVar(value="Chưa có kết quả. Chọn dataset và cấu hình rồi Chạy GA.")
        ttk.Label(parent, textvariable=self.status, foreground="#225c78").pack(anchor="w", pady=(8, 2))
        ttk.Label(parent, textvariable=self.metrics, wraplength=750).pack(anchor="w", pady=(0, 4))
        self.tabs = ttk.Notebook(parent)
        self.tabs.pack(fill="both", expand=True)
        route_tab, history_tab, detail_tab = (ttk.Frame(self.tabs) for _ in range(3))
        for tab, label in ((route_tab, "Tuyến đường"), (history_tab, "Hội tụ"), (detail_tab, "Chi tiết")):
            self.tabs.add(tab, text=label)
        self.layout_note = tk.StringVar(value=SCHEMATIC)
        ttk.Label(route_tab, textvariable=self.layout_note, foreground="#8b4513").pack(anchor="center")
        self.route_figure = Figure(figsize=(6, 4), dpi=90)
        self.history_figure = Figure(figsize=(6, 4), dpi=90)
        self.route_canvas = FigureCanvasTkAgg(self.route_figure, master=route_tab)
        self.history_canvas = FigureCanvasTkAgg(self.history_figure, master=history_tab)
        for canvas in (self.route_canvas, self.history_canvas):
            canvas.get_tk_widget().pack(fill="both", expand=True)
        draw_history(self.history_figure, [])
        self.details = scrolledtext.ScrolledText(detail_tab, wrap="none", font=("Consolas", 10), width=65, height=15)
        self.details.pack(fill="both", expand=True)
        self.details.configure(state="disabled")
        self.tour_text = tk.StringVar(value="Tour 1-based khép vòng sẽ xuất hiện sau khi chạy.")
        ttk.Label(parent, textvariable=self.tour_text, wraplength=760).pack(fill="x", pady=(6, 0))

    def _variant_changed(self) -> None:
        local = self.form.variables["local_search_enabled"].get()
        adaptive = self.form.variables["adaptive_mutation"].get()
        self.variant.set(("GA + 2-opt (biến thể thực nghiệm)" if local else "GA thuần, không local search")
                         + (" · adaptive ON" if adaptive else " · adaptive OFF"))

    def _algorithm(self) -> str:
        return self.algorithm_keys[self.algorithm_box.current()]

    def _update_actions(self) -> None:
        busy = self.controller.active or self.closing
        available = ALGORITHMS[self._algorithm()].solver is not None
        for widget in (self.dataset_box, self.algorithm_box, self.preset_box):
            widget.configure(state="disabled" if busy else "readonly")
        for widget in (self.browse_button, self.reset_button):
            widget.configure(state="disabled" if busy else "normal")
        self.form.set_enabled(not busy and available)
        self.run_button.configure(state="normal" if not busy and available and self.problem is not None else "disabled")
        self.stop_button.configure(state="normal" if self.controller.active and not self.closing else "disabled")
        for widget in self.export_buttons:
            widget.configure(state="normal" if self.result is not None and not busy else "disabled")
        if not available and not busy:
            self.status.set("EHO đang phát triển — nhóm EHO sẽ bổ sung; chưa thể chạy.")
        elif not busy and self.status.get().startswith("EHO"):
            self.status.set("Sẵn sàng")

    def _error(self, title: str, error: Exception | str) -> None:
        self.status.set(f"Lỗi: {error}")
        messagebox.showerror(title, str(error), parent=self.root)

    def select_dataset(self, path: str | Path | None = None) -> None:
        if self.controller.active or self.closing:
            return
        path = path or self.dataset_paths.get(self.dataset_var.get())
        self.problem = None
        try:
            if path is None:
                raise ValueError("Chưa chọn file ma trận .txt.")
            self.problem = load_matrix(path)
        except (ValueError, OSError) as error:
            self.dataset_info.set(str(error))
            self._error("Dữ liệu không hợp lệ", error)
        else:
            p = self.problem
            self.dataset_info.set(f"{p.name} · n={p.dimension} · vuông/đối xứng/finite/chéo 0: hợp lệ\nNguồn: {p.source}")
            self.status.set("Sẵn sàng")
            # Kết quả cũ không được gắn lên dataset mới.
            self.result = None
            self.run_problem = None
            self.layout_note.set(SCHEMATIC if p.coordinates is None else "Tọa độ do dataset cung cấp")
            self.tour_text.set("Chưa có tour cho dataset vừa chọn.")
            self.metrics.set("Chưa chạy dataset này.")
            draw_route(self.route_figure, p)
            draw_history(self.history_figure, [])
            self._set_details({"dataset": p.name, "source": p.source, "metadata": dict(p.metadata)})
            self.route_canvas.draw_idle()
            self.history_canvas.draw_idle()
        self._update_actions()

    def browse_dataset(self) -> None:
        path = filedialog.askopenfilename(parent=self.root, title="Chọn ma trận khoảng cách whitespace",
                                          filetypes=[("Ma trận khoảng cách", "*.txt")])
        if path:
            name = str(Path(path).resolve())
            self.dataset_paths[name] = Path(path)
            self.dataset_box.configure(values=list(self.dataset_paths))
            self.dataset_var.set(name)
            self.select_dataset(path)

    def apply_preset(self) -> None:
        if not self.controller.active:
            self.form.set_config(preset_config(self.preset_var.get()))

    def reset_defaults(self) -> None:
        self.preset_var.set("Mặc định")
        self.apply_preset()

    def start_run(self) -> None:
        if self.controller.active or self.closing:
            return
        try:
            algorithm = self._algorithm()
            if ALGORITHMS[algorithm].solver is None:
                raise ValueError("EHO chưa triển khai.")
            if self.problem is None:
                raise ValueError("Hãy chọn dataset hợp lệ trước khi chạy.")
            config = self.form.config()
            self.run_problem = self.problem
            self.controller.start(algorithm, self.run_problem, config)
        except (ValueError, RuntimeError) as error:
            self._error("Không thể chạy", error)
            return
        self.result = None
        self.live_history = []
        self.started = perf_counter()
        self.status.set("Đang chạy · " + self.variant.get())
        self.metrics.set(f"seed={config.seed}; đang khởi tạo quần thể…")
        self.tour_text.set("Đang tìm tour…")
        self._set_details({"dataset": self.run_problem.name, "source": self.run_problem.source,
                           "config_thuc_chay": asdict(config)})
        draw_route(self.route_figure, self.run_problem)
        draw_history(self.history_figure, [])
        self.route_canvas.draw_idle()
        self.history_canvas.draw_idle()
        self._update_actions()

    def stop_run(self) -> None:
        if self.controller.active:
            self.controller.cancel()
            self.status.set("Đã yêu cầu dừng · đang chờ solver trả best đã tìm được…")
            self.stop_button.configure(state="disabled")

    def _poll(self) -> None:
        for kind, payload in self.controller.drain():
            if kind == "progress":
                self.live_history.append(payload)
                self.metrics.set(f"seed={self.form.variables['seed'].get()} · thế hệ={payload.iteration} · evaluations={payload.evaluations} · best={payload.best_so_far:g} · runtime={payload.elapsed_seconds:.2f}s")
                if self.tabs.index(self.tabs.select()) == 1 and perf_counter() - self.last_live_plot >= .3:
                    draw_history(self.history_figure, self.live_history[-1000:])
                    self.history_canvas.draw_idle()
                    self.last_live_plot = perf_counter()
            elif kind == "result":
                self.show_result(payload)
            elif kind == "error":
                self.status.set(f"Lỗi solver: {payload[0]}")
                self._set_details({"error": payload[0], "traceback": payload[1]})
                if not self.closing:
                    messagebox.showerror("Lỗi solver", payload[0], parent=self.root)
                self._update_actions()
        if self.closing and not self.controller.active:
            self._destroy()
            return
        if self.controller.active:
            self.root.title(f"GA–EHO–TSP · Đang chạy {perf_counter() - self.started:.1f}s")
        self.poll_id = self.root.after(100, self._poll)

    def show_result(self, result: RunResult) -> None:
        self.result = result
        p = self.run_problem
        assert p is not None
        self.layout_note.set(SCHEMATIC if p.coordinates is None else "Tọa độ do dataset cung cấp")
        status = "Đã hủy" if result.stopping_reason == "CANCELLED" else "Hoàn thành"
        self.status.set(f"{status} · {result.stopping_reason} · {result.algorithm}")
        self.root.title("Đề tài 6 · GA–EHO–TSP | Genetic Algorithm")
        self.metrics.set(f"{p.name} · n={p.dimension} · distance={result.best_distance:g}\nseed={result.seed} · iterations={result.iterations_completed} · evaluations={result.evaluations} · runtime solver={result.elapsed_seconds:.6f}s")
        self.tour_text.set("Tour 1-based: " + " → ".join(str(i + 1) for i in (*result.best_route, 0)))
        draw_route(self.route_figure, p, result)
        draw_history(self.history_figure, result.history)
        self.route_canvas.draw_idle()
        self.history_canvas.draw_idle()
        detail = asdict(result)
        detail["dataset_source"] = p.source
        detail["dimension"] = p.dimension
        detail["note"] = "History hiển thị tối đa 200 snapshot cuối; JSON/CSV xuất đầy đủ. Chi phí theo ma trận, không mặc định km."
        detail["history"] = detail["history"][-200:]
        if p.known_optimum is not None and p.known_optimum > 0:
            detail["relative_gap_percent"] = 100 * (result.best_distance - p.known_optimum) / p.known_optimum
        self._set_details(detail)
        self._update_actions()

    def _set_details(self, values: dict) -> None:
        self.details.configure(state="normal")
        self.details.delete("1.0", "end")
        self.details.insert("1.0", json.dumps(values, ensure_ascii=False, indent=2))
        self.details.configure(state="disabled")

    def save(self, kind: str) -> None:
        if self.result is None or self.controller.active:
            return
        extension = ".json" if kind == "json" else ".csv" if kind == "csv" else ".png"
        path = filedialog.asksaveasfilename(parent=self.root, title="Lưu kết quả GA", defaultextension=extension,
                                           initialfile=f"{self.result.problem_name}-{self.result.seed}-{kind}{extension}",
                                           filetypes=[(extension, "*" + extension)], confirmoverwrite=True)
        if not path:
            return
        try:
            if kind == "json":
                export_json(self.result, path)
            elif kind == "csv":
                export_history(self.result, path)
            else:
                figure = self.route_figure if kind == "route" else self.history_figure
                figure.savefig(path, dpi=150, bbox_inches="tight")
        except (ValueError, OSError) as error:
            self._error("Không lưu được kết quả", error)
        else:
            self.status.set(f"Đã lưu {path} · {self.result.stopping_reason}")

    def request_close(self) -> None:
        if self.closing:
            return
        if self.controller.active:
            if not messagebox.askyesno("Đóng cửa sổ", "Solver đang chạy. Yêu cầu dừng và đóng sau khi worker kết thúc?", parent=self.root):
                return
            self.closing = True
            self.controller.cancel()
            self.status.set("Đang dừng worker trước khi đóng…")
            self._update_actions()
        else:
            self._destroy()

    def _destroy(self) -> None:
        self.root.after_cancel(self.poll_id)
        for canvas in (self.route_canvas, self.history_canvas):
            # Hủy draw_idle pending trước khi hủy Tcl interpreter.
            idle = canvas._idle_draw_id
            if idle:
                canvas.get_tk_widget().after_cancel(idle)
                canvas._idle_draw_id = None
        self.root.destroy()


def main() -> int:
    try:
        root = tk.Tk()
    except tk.TclError as error:
        print(f"Không mở được GUI Tkinter/display: {error}", file=sys.stderr)
        return 1
    Application(root)
    root.mainloop()
    return 0
