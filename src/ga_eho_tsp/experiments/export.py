"""Xuất report nhỏ từ số đo benchmark; không hard-code counters của preset."""

from pathlib import Path
from typing import Any


def write_summary_markdown(summaries: list[dict[str, Any]], path: Path) -> None:
    lines = ["| Variant | Dataset | Valid / failed | Distance mean ± std | Min / median / max | Runtime mean / median (s) | Evaluations min / max |",
             "|---|---|---:|---:|---:|---:|---:|"]
    for row in summaries:
        if not row["successful_runs"]:
            lines.append(f"| {row['variant']} | {row['dataset']} | 0 / {row['failed_runs']} | — | — | — | — |")
            continue
        deviation = f"{row['distance_std']:.2f}" if row['distance_std'] is not None else "—"
        lines.append(
            f"| {row['variant']} | {row['dataset']} | {row['successful_runs']} / {row['failed_runs']} "
            f"| {row['distance_mean']:.2f} ± {deviation} "
            f"| {row['distance_min']:g} / {row['distance_median']:g} / {row['distance_max']:g} "
            f"| {row['runtime_seconds_mean']:.6f} / {row['runtime_seconds_median']:.6f} "
            f"| {row['evaluations_min']:g} / {row['evaluations_max']:g} |")
    path.write_text("\n".join(lines)+"\n", encoding="utf-8")
