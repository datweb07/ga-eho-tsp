"""Form GAConfig: defaults từ schema, parse có tên field, không sửa config ngầm."""

from dataclasses import asdict, replace
import tkinter as tk
from tkinter import ttk

from ..domain.models import GAConfig

CHOICES = {
    "selection_method": ("tournament", "rank", "roulette_wheel"),
    "crossover_method": ("ox", "pmx"),
    "mutation_method": ("inversion", "swap", "insertion", "scramble"),
    "initialization_method": ("random", "nearest_neighbor", "mixed"),
}
OPTIONAL_INTS = {"max_evaluations", "stagnation_patience"}
ADVANCED = {
    "stagnation_patience", "adaptive_mutation", "adaptive_min_rate", "adaptive_max_rate",
    "adaptive_patience", "local_search_enabled", "local_search_max_moves",
    "local_search_max_probes", "time_limit_seconds", "record_history_every",
}
HELP = {
    "population_size": "Số tour trong quần thể, >= 4; budget phải đủ quần thể đầu.",
    "generations": "Số thế hệ; thực chạy tối đa min(generations, max_iterations).",
    "max_iterations": "Cap thứ hai; muốn vượt 250 phải tăng cả hai cap.",
    "seed": "Seed nguyên >= 0. Cùng input/config/seed cho cùng numeric history.",
    "max_evaluations": "Tổng full objective calls, gồm probes 2-opt. Trống = không giới hạn.",
    "elite_count": "Số cá thể giữ lại, 0 <= elite_count < population_size.",
    "tournament_size": "Số ứng viên mỗi lần tournament, từ 2 đến population_size.",
    "mutation_rate": "Xác suất đột biến trên CẢ tour, trong [0, 1].",
    "crossover_rate": "Xác suất lai cặp bố mẹ, trong [0, 1].",
    "initialization_method": "random là baseline; NN/mixed là heuristic khởi tạo tùy chọn.",
    "nn_seed_fraction": "Tỷ lệ NN trong mixed, [0,1]; không ép các tour unique.",
    "local_search_enabled": "Bật sẽ chạy GA + 2-opt (biến thể thực nghiệm), không phải baseline.",
    "local_search_max_moves": "OFF phải là 0; ON cần >=1 accepted moves/offspring.",
    "local_search_max_probes": "Giới hạn full objective probes cho mỗi offspring, >=1.",
    "stagnation_patience": "Dừng sau k full generations không cải thiện. Trống = OFF.",
    "time_limit_seconds": "Trống = không giới hạn. Cooperative; khởi tạo quần thể là atomic.",
    "record_history_every": "Lưu mỗi k thế hệ, luôn có snapshot đầu/cuối.",
    "adaptive_mutation": "Thích nghi theo stagnation/diversity; OFF mặc định.",
    "adaptive_min_rate": "Cận dưới xác suất adaptive [0,1], <= max_rate.",
    "adaptive_max_rate": "Cận trên xác suất adaptive [0,1].",
    "adaptive_patience": "Số vòng để tăng áp lực adaptive, >=1.",
    "selection_method": "tournament/rank/roulette_wheel; minimize tour cost.",
    "crossover_method": "OX hoặc PMX, luôn giữ hoán vị và city 0.",
    "mutation_method": "inversion/swap/insertion/scramble; chỉ tác động tail.",
}


def preset_config(name: str) -> GAConfig:
    """Preset luôn bắt đầu từ schema thật; mọi field được phản ánh lại form."""
    default = GAConfig()
    if name == "Demo nhanh":
        return replace(default, population_size=40, generations=60, max_iterations=60)
    if name == "Giới hạn evaluations":
        return replace(default, generations=2000, max_iterations=2000, max_evaluations=6000,
                       record_history_every=5)
    return default


def parse_config(values: dict[str, str | bool]) -> GAConfig:
    defaults = asdict(GAConfig())
    parsed = {}
    for name, default in defaults.items():
        value = values[name]
        try:
            if type(default) is bool:
                if type(value) is not bool:
                    raise ValueError("cần giá trị bật/tắt")
                parsed[name] = value
            elif name in CHOICES:
                parsed[name] = str(value).strip().lower()
            elif name in OPTIONAL_INTS or name == "time_limit_seconds":
                text = str(value).strip()
                parsed[name] = None if not text else (float(text) if name == "time_limit_seconds" else int(text))
            else:
                parsed[name] = type(default)(str(value).strip())
        except (TypeError, ValueError) as error:
            expected = "số thực" if isinstance(default, float) or name == "time_limit_seconds" else "số nguyên"
            raise ValueError(f"{name}: cần {expected} hợp lệ. {HELP.get(name, '')}") from error
    return GAConfig(**parsed)


class ConfigForm(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.variables: dict[str, tk.Variable] = {}
        self.widgets: list[tk.Widget] = []
        self.help_text = tk.StringVar(value="Chọn trường để xem ý nghĩa. Trống ở các cap tùy chọn = OFF.")
        tabs = ttk.Notebook(self)
        tabs.pack(fill="both", expand=True)
        for advanced, title in ((False, "Cơ bản"), (True, "Nâng cao")):
            page = ttk.Frame(tabs)
            tabs.add(page, text=title)
            canvas = tk.Canvas(page, highlightthickness=0, width=390)
            scroll = ttk.Scrollbar(page, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scroll.set)
            scroll.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            body = ttk.Frame(canvas, padding=6)
            window = canvas.create_window((0, 0), window=body, anchor="nw")
            body.bind("<Configure>", lambda event, c=canvas: c.configure(scrollregion=c.bbox("all")))
            canvas.bind("<Configure>", lambda event, c=canvas, w=window: c.itemconfigure(w, width=event.width))
            body.columnconfigure(1, weight=1)
            row = 0
            for name, default in asdict(GAConfig()).items():
                if (name in ADVANCED) != advanced:
                    continue
                ttk.Label(body, text=name).grid(row=row, column=0, sticky="w", pady=4, padx=(0, 8))
                var = tk.BooleanVar(value=default) if type(default) is bool else tk.StringVar(
                    value="" if default is None else str(default))
                self.variables[name] = var
                if name in CHOICES:
                    widget = ttk.Combobox(body, textvariable=var, values=CHOICES[name], state="readonly", width=18)
                elif type(default) is bool:
                    widget = ttk.Checkbutton(body, text="Bật", variable=var)
                else:
                    widget = ttk.Entry(body, textvariable=var, width=19)
                widget.grid(row=row, column=1, sticky="ew", pady=3)
                widget.bind("<FocusIn>", lambda event, n=name: self.help_text.set(HELP.get(n, n)))
                # Cuộn cả khi chuột ở entry/label; không bind_all sang biểu đồ.
                for child in (widget, body.grid_slaves(row=row, column=0)[0]):
                    child.bind("<MouseWheel>", lambda event, c=canvas: c.yview_scroll(-int(event.delta / 120), "units"))
                self.widgets.append(widget)
                row += 1
        ttk.Label(self, textvariable=self.help_text, wraplength=390, foreground="#35516d").pack(fill="x", pady=6)

    def config(self) -> GAConfig:
        return parse_config({name: var.get() for name, var in self.variables.items()})

    def set_config(self, config: GAConfig) -> None:
        for name, value in asdict(config).items():
            self.variables[name].set("" if value is None else value)

    def set_enabled(self, enabled: bool) -> None:
        for widget in self.widgets:
            if isinstance(widget, ttk.Combobox):
                widget.configure(state="readonly" if enabled else "disabled")
            else:
                widget.configure(state="normal" if enabled else "disabled")
