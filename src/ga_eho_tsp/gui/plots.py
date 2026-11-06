"""Matplotlib presentation; không gọi solver hoặc sửa route core."""

from collections.abc import Sequence
from math import cos, sin, tau

from matplotlib.figure import Figure

from ..domain.models import IterationStat, RunResult, TSPProblem

SCHEMATIC = "Sơ đồ minh họa, không phải vị trí địa lý"


def draw_route(figure: Figure, problem: TSPProblem, result: RunResult | None = None) -> None:
    figure.clear()
    ax = figure.add_subplot(111)
    points = problem.coordinates
    if points is None:
        points = tuple((cos(tau * i / problem.dimension), sin(tau * i / problem.dimension))
                       for i in range(problem.dimension))
    ax.scatter([p[0] for p in points], [p[1] for p in points], s=45, color="#2b658c", zorder=3)
    for i, (x, y) in enumerate(points):
        ax.annotate(str(i + 1), (x, y), xytext=(5, 6), textcoords="offset points", fontsize=8)
    ax.scatter(*points[0], s=120, facecolors="none", edgecolors="#cb6527", linewidths=2,
               label="Bắt đầu/kết thúc: 1", zorder=4)
    if result is not None:
        tour = (*result.best_route, result.best_route[0])
        ax.plot([points[i][0] for i in tour], [points[i][1] for i in tour], color="#357c9c", linewidth=1.2)
        title = f"{problem.name} | {result.algorithm} | chi phí {result.best_distance:g}"
    else:
        title = f"{problem.name} | {problem.dimension} thành phố | chưa chạy"
    ax.set_title(title, fontsize=10, pad=18)
    ax.legend(loc="lower left", fontsize=8)
    ax.set_aspect("equal", adjustable="datalim")
    ax.margins(.18)
    ax.set_axis_off()
    figure.text(.5, .025, SCHEMATIC if problem.coordinates is None else "Tọa độ do dataset cung cấp",
                ha="center", fontsize=9, color="#8b4513")
    figure.subplots_adjust(left=.08, right=.94, top=.88, bottom=.12)


def draw_history(figure: Figure, history: Sequence[IterationStat]) -> None:
    figure.clear()
    ax, diversity = figure.subplots(2, 1, sharex=True, gridspec_kw={"height_ratios": [3, 1]})
    if history:
        x = [s.evaluations for s in history]
        for field, label in (("best_so_far", "Best toàn lịch sử"), ("best_current", "Best quần thể"),
                             ("mean_fitness", "Trung bình quần thể")):
            ax.step(x, [getattr(s, field) for s in history], where="post", label=label, linewidth=1.3)
        available = [s for s in history if s.population_diversity is not None]
        if available:
            diversity.step([s.evaluations for s in available], [s.population_diversity for s in available],
                           where="post", color="#47816b")
        ax.legend(fontsize=8)
    ax.set(title="Hội tụ từ snapshot thực của solver", ylabel="Chi phí (đơn vị ma trận)")
    diversity.set(xlabel="Số lần đánh giá hàm mục tiêu (evaluations)", ylabel="Diversity", ylim=(-.05, 1.05))
    for panel in (ax, diversity):
        panel.grid(alpha=.2)
    figure.subplots_adjust(left=.18, right=.97, top=.90, bottom=.13, hspace=.18)
