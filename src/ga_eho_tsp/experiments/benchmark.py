"""Benchmark GA nhiều seed và ablation; không đọc trạng thái nội bộ solver."""

import csv
import hashlib
import json
import platform
import re
import statistics
import subprocess
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any
from uuid import uuid4

from .. import __version__
from ..algorithms.ga import solve
from ..data.matrix_loader import load_matrix
from ..domain.models import GAConfig
from .export import write_summary_markdown


def environment_metadata() -> dict[str, Any]:
    try:
        commit_process = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
        dirty_process = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=False)
        commit = commit_process.stdout.strip() or None
        dirty = bool(dirty_process.stdout.strip()) if dirty_process.returncode == 0 else None
    except OSError:
        commit, dirty = None, None
    package = Path(__file__).resolve().parents[1]
    hashes = {str(path.relative_to(package)).replace('\\', '/'):
              hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(package.rglob('*.py'))}
    return {"python": platform.python_version(), "platform": platform.platform(),
            "version": __version__, "commit": commit, "working_tree_dirty": dirty,
            "source_sha256": hashes}


def summarize(rows: list[dict[str, Any]], dataset: str, variant: str, runs: int) -> dict[str, Any]:
    successful = [row for row in rows if row['valid']]
    summary = {"dataset": dataset, "variant": variant, "runs": runs,
               "successful_runs": len(successful), "failed_runs": runs-len(successful)}
    for metric in ("distance", "runtime_seconds", "evaluations", "relative_gap_percent"):
        values = [row[metric] for row in successful if row[metric] is not None]
        for name, function in (("mean", statistics.mean), ("std", statistics.stdev),
                               ("median", statistics.median), ("min", min), ("max", max)):
            summary[f"{metric}_{name}"] = (function(values) if values and (name != "std" or len(values)>1) else None)
    return summary


def benchmark(config_path: str | Path) -> dict[str, Any]:
    """Paths tương đối với config; variants chỉ override GAConfig, không Cartesian grid."""
    config_path = Path(config_path).resolve()
    spec = json.loads(config_path.read_text(encoding="utf-8"))
    if spec.get("algorithm", "ga") != "ga":
        raise ValueError("EHO planned / not implemented.")
    seeds = spec["seeds"]
    if (not isinstance(seeds, list) or len(seeds) < 5
            or any(type(seed) is not int or seed < 0 for seed in seeds)
            or len(set(seeds)) != len(seeds)):
        raise ValueError("Benchmark cần ít nhất 5 seed nguyên không âm khác nhau.")
    config = GAConfig(**spec.get("ga", {}))
    variants = spec.get("variants", [{"name": "baseline", "ga": {}}])
    names = [variant['name'] for variant in variants]
    if not names or any(not isinstance(name, str) or not re.fullmatch(r'[a-zA-Z0-9_-]+', name) for name in names) or len(set(names)) != len(names):
        raise ValueError("Tên variant phải duy nhất và chỉ chứa chữ, số, _ hoặc -.")
    configured = [(variant['name'], replace(config, **variant.get('ga', {}))) for variant in variants]
    # Validate toàn bộ dataset trước run, fail-fast thay vì mất nửa batch vì file sau sai.
    problems = [load_matrix(config_path.parent / dataset) for dataset in spec['datasets']]
    if not problems or len({p.name for p in problems}) != len(problems):
        raise ValueError("Benchmark cần dataset không rỗng, tên dataset không trùng.")
    output = config_path.parent / spec["output_dir"]
    output.mkdir(parents=True, exist_ok=True)
    environment = environment_metadata()
    rows, summaries = [], []
    failures = 0
    for variant, variant_config in configured:
        run_dir = output / variant if 'variants' in spec else output
        run_dir.mkdir(parents=True, exist_ok=True)
        for problem in problems:
            group = []
            for seed in seeds:
                run_id = uuid4().hex
                run_config = replace(variant_config, seed=seed)
                record = {"run_id": run_id, "dataset": problem.name, "variant": variant,
                          "algorithm": "ga", "seed": seed, "distance": None, "best_route": None,
                          "runtime_seconds": None, "evaluations": None, "status": "FAILED",
                          "valid": False, "sha256": problem.metadata["sha256"],
                          "known_optimum": problem.known_optimum, "relative_gap_percent": None,
                          "config": json.dumps(asdict(run_config), sort_keys=True),
                          "version": __version__, "commit": environment['commit'], "error": ""}
                try:
                    result = solve(problem, run_config)
                    if not result.is_valid or problem.route_length(result.best_route) != result.best_distance:
                        raise ValueError("Solver trả chi phí/route không hợp lệ.")
                except (ValueError, RuntimeError) as error:
                    record["error"] = str(error)
                    failures += 1
                    structured = {"run": record, "environment": environment}
                else:
                    record.update(algorithm=result.algorithm, distance=result.best_distance,
                                  best_route=json.dumps(result.best_route), runtime_seconds=result.elapsed_seconds,
                                  evaluations=result.evaluations, status=result.stopping_reason, valid=True)
                    if problem.known_optimum is not None and problem.known_optimum > 0:
                        record['relative_gap_percent'] = 100*(result.best_distance-problem.known_optimum)/problem.known_optimum
                    structured = {"run_id": run_id, "variant": variant, "result": asdict(result), "environment": environment}
                rows.append(record)
                group.append(record)
                (run_dir / f"{problem.name}-{seed}.json").write_text(
                    json.dumps(structured, indent=2, allow_nan=False), encoding="utf-8")
            summaries.append(summarize(group, problem.name, variant, len(seeds)))
    with (output / "raw.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = {"environment": environment, "summary": summaries, "failed_runs": failures, "total_runs": len(rows)}
    (output / "summary.json").write_text(json.dumps(report, indent=2, allow_nan=False), encoding="utf-8")
    write_summary_markdown(summaries, output / "summary.md")
    return report
