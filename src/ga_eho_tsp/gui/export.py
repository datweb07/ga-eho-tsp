"""Xuất snapshot RunResult; caller chọn đường dẫn và xác nhận overwrite."""

import csv
from dataclasses import asdict, fields
import json
from pathlib import Path

from ..domain.models import IterationStat, RunResult


def export_json(result: RunResult, path: str | Path) -> None:
    Path(path).write_text(json.dumps(asdict(result), ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")


def export_history(result: RunResult, path: str | Path) -> None:
    with Path(path).open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=[field.name for field in fields(IterationStat)])
        writer.writeheader()
        writer.writerows(asdict(stat) for stat in result.history)
