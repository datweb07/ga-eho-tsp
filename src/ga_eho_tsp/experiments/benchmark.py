"""Benchmark GA nhiều seed; chưa có EHO để so sánh liên thuật toán."""

import csv
import json
import platform
import statistics
import subprocess
from dataclasses import asdict, replace
from pathlib import Path
from uuid import uuid4

from .. import __version__
from ..algorithms.ga import solve
from ..data.matrix_loader import load_matrix
from ..domain.models import GAConfig


def benchmark(config_path: str | Path) -> dict[str, object]:
    """Đường dẫn dataset/output tương đối với thư mục chứa config."""
    config_path = Path(config_path).resolve()
    spec = json.loads(config_path.read_text(encoding="utf-8"))
    if spec.get("algorithm", "ga") != "ga":
        raise ValueError("EHO planned / not implemented.")
    seeds = spec["seeds"]
    if len(seeds) < 5 or len(set(seeds)) != len(seeds):
        raise ValueError("Benchmark chính cần ít nhất 5 seed khác nhau.")
    config = GAConfig(**spec.get("ga", {}))
    output = config_path.parent / spec["output_dir"]
    output.mkdir(parents=True, exist_ok=True)
    commit_process = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
    dirty_process = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=False)
    environment = {"python": platform.python_version(), "platform": platform.platform(),
                   "version": __version__, "commit": commit_process.stdout.strip(),
                   "working_tree_dirty": bool(dirty_process.stdout.strip())}
    rows, summaries = [], []
    failures = 0
    for dataset in spec["datasets"]:
        problem = load_matrix(config_path.parent / dataset)
        group = []
        for seed in seeds:
            run_id = uuid4().hex
            record = {"run_id": run_id, "dataset": problem.name, "algorithm": "ga", "seed": seed,
                      "distance": None, "runtime_seconds": None,
                      "evaluations": None, "status": "FAILED",
                      "valid": False, "sha256": problem.metadata["sha256"],
                      "known_optimum": problem.known_optimum, "relative_gap_percent": None,
                      "config": json.dumps(asdict(replace(config, seed=seed)), sort_keys=True),
                      "environment": json.dumps(environment, sort_keys=True), "error": ""}
            try:
                result = solve(problem, replace(config, seed=seed))
                # Independent check excluded from solver evaluations/runtime.
                valid = problem.route_length(result.best_route) == result.best_distance
                if not valid or not result.is_valid:
                    raise ValueError("Solver trả chi phí/route không hợp lệ.")
            except (ValueError, RuntimeError) as error:
                record["error"] = str(error)
                failures += 1
                rows.append(record)
                (output / f"{problem.name}-{seed}.json").write_text(
                    json.dumps(record, indent=2), encoding="utf-8")
                continue
            record.update(distance=result.best_distance, runtime_seconds=result.elapsed_seconds,
                          evaluations=result.evaluations, status=result.stopping_reason, valid=True)
            (output / f"{problem.name}-{seed}.json").write_text(json.dumps(
                {"run_id": run_id, "result": asdict(result), "environment": environment}, indent=2), encoding="utf-8")
            rows.append(record)
            group.append(record)
        summary = {"dataset": problem.name, "runs": len(seeds), "successful_runs": len(group),
                   "failed_runs": len(seeds)-len(group)}
        for metric in ("distance", "runtime_seconds"):
            values = [row[metric] for row in group]
            for name, function in (("mean", statistics.mean), ("std", statistics.stdev),
                                   ("median", statistics.median), ("min", min), ("max", max)):
                summary[f"{metric}_{name}"] = (function(values) if values and (name != "std" or len(values)>1) else None)
        summaries.append(summary)
    if not rows:
        raise ValueError("Benchmark cần ít nhất một dataset.")
    with (output / "raw.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = {"environment": environment, "summary": summaries, "failed_runs": failures}
    (output / "summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
