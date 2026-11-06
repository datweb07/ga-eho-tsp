"""Lưu report nhỏ từ output thật, không chạy lại hoặc sửa số liệu."""

import csv
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    output = ROOT / "outputs/benchmarks/ga-p0"
    reports = ROOT / "experiments/reports"
    for name in ("raw.csv", "summary.json"):
        shutil.copyfile(output / name, reports / f"ga_p0_{name}")
    report = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    rows = list(csv.DictReader((output / "raw.csv").open(encoding="utf-8")))
    table = ["| Dataset | Runs hợp lệ | Distance mean ± std | Min / median / max | Runtime mean (s) | Evaluations/run |",
             "|---|---:|---:|---:|---:|---:|"]
    for item in report["summary"]:
        costs = f"{item['distance_mean']:.2f} ± {item['distance_std']:.2f}"
        spread = f"{item['distance_min']:g} / {item['distance_median']:g} / {item['distance_max']:g}"
        table.append(f"| {item['dataset']} | {item['successful_runs']} | {costs} | {spread} | {item['runtime_seconds_mean']:.6f} | 19580 |")
    (reports / "ga_p0_table.md").write_text("\n".join(table)+"\n", encoding="utf-8")
    manifest = {str(p.relative_to(ROOT)).replace('\\','/'): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted((ROOT/"src/ga_eho_tsp").rglob('*.py'))}
    (reports / "implementation_sha256.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    baseline = json.loads((reports/"legacy_baseline.json").read_text(encoding="utf-8"))
    datasets = ["# Dữ liệu legacy", "", "Ma trận explicit whitespace, không header, city 0-based ở core.",
                "Nguồn trực tiếp: bộ code nhóm đưa vào workspace, tham chiếu ThienNguyen3001/Travelling-Salesman-Genetic-AI-Final.",
                "Các file được chuyển nguyên byte từ data/ sang data/legacy/. Chưa xác minh quyền phân phối hoặc ánh xạ từng file với nguồn dataset gốc.",
                "Hậu tố tên chỉ là hint; registry known_optimum=None. Xem docs/audit_legacy.md về nguồn/giấy phép và kiểm chứng exhaustive 3/4/6 city.", "",
                "Tất cả 7 file đã qua dimension, square, symmetry, diagonal=0, finite, nonnegative checks.", "",
                "| File | n | Cost route (0,1,…,n−1) | SHA256 |", "|---|---:|---:|---|"]
    for item in baseline['datasets']:
        name = item['file'].replace('\\','/').split('/')[-1]
        assert hashlib.sha256((ROOT/'data/legacy'/name).read_bytes()).hexdigest() == item['sha256']
        datasets.append(f"| {name} | {item['dimension']} | {item['sample_cost']} | `{item['sha256']}` |")
    (ROOT/'data/README.md').write_text('\n'.join(datasets)+'\n', encoding='utf-8')
    assert len(rows) == 35 and all(row['valid'] == 'True' for row in rows)
    print('\n'.join(table))


if __name__ == '__main__':
    main()
