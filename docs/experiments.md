# Kiểm thử và số liệu thực — GA P0

Ngày thực hiện: 05/11/2026. Python 3.11.9, Windows-10-10.0.26300-SP0, package 0.1.0. HEAD lúc đo `5d81c76a315cdb7e7753d65aa9b68e503f42d795`, working tree dirty: code mới chưa commit. SHA256 từng file package đã đo ở `experiments/reports/implementation_sha256.json`; checksum dataset nằm trong raw CSV và data/README.md. Không có EHO solver hoặc benchmark EHO.

## Lệnh thực sự đã chạy

Các lệnh `python` bên dưới được thực thi bằng `.venv/Scripts/python.exe` trong repo này.

| Lệnh | Kết quả thực |
|---|---|
| `python --version`; `python -m pip list` | Python 3.11.9; xác định dependency legacy, chưa có pytest lúc bắt đầu |
| `python -m pip install -e '.[dev]' --no-build-isolation` | FAIL: môi trường ban đầu thiếu bdist_wheel |
| `python -m pip install -e '.[dev]'` trong sandbox | FAIL: getaddrinfo/PyPI không truy cập được |
| Cùng lệnh cài đặt sau cấp quyền network | PASS: editable package + pytest 8.3.5 và dependencies được cài |
| `python -m pytest -q` lần đầu | 98 passed in 0.80s |
| Sau thêm edge cases/evaluation/cancel/failure logs | 104 passed in 0.82s |
| `python -m pytest -q` cuối cùng | **105 passed in 0.78s**, 0 fail, 0 skip; log `experiments/reports/pytest.txt` |
| `python -m compileall -q src/ga_eho_tsp` | PASS tại bước 104 tests |
| `python -m pip check` | No broken requirements found |
| `python -m ga_eho_tsp.cli validate --dataset data/legacy/06Cities-1248.txt` | PASS: dimension=6, symmetric=True, diagonal=0, finite=True |
| `python -m ga_eho_tsp.cli solve --algorithm ga --dataset data/legacy/15Cities-1194.txt --seed 42 --json outputs/runs/ga-15-42.json` | PASS: kết quả bên dưới |
| `python -m ga_eho_tsp.cli benchmark --config experiments/configs/baseline.json` | PASS: 35 run, 0 failed, tất cả route/cost kiểm tra độc lập hợp lệ |
| `python experiments/scripts/audit_legacy.py` | PASS: tái hiện các lỗi legacy, lưu JSON; cần extra legacy |
| `python -m cProfile -o outputs/ga-48.prof -m ga_eho_tsp.cli solve --dataset data/legacy/48Cities-33523.txt --seed 42` | PASS: distance=38410, 19580 evaluations; profile có overhead |
| `python experiments/scripts/summarize_ga.py` | PASS: kiểm tra checksum 7 matrix, 35 raw rows valid; sinh bảng/manifest, giữ report nhỏ |

Baseline chạy trước archive (import fail, benchmark cũ, headless visualization) đã ghi riêng ở audit_legacy.md. Không chạy GUI tương tác, không thực thi notebook end-to-end, không chạy EHO. Test failure logging dùng lỗi được tiêm **chỉ trong test** để chứng minh không bỏ run lỗi; benchmark 35 run thực không có lỗi tiêm.

## Phạm vi tests

- Domain: objective/cạnh cuối/đảo route/không sửa input, n nhỏ, jagged/non-numeric/negative/NaN/inf/asymmetric/nonzero diagonal, bool/float city/sai start/closed/duplicate/missing route, floating tolerance và integer symmetry chính xác, off-diagonal zero, loader lỗi.
- 7 dataset: dimension 3/4/6/15/26/42/48 và sample cost/checksum metadata. Exhaustive enumeration của 2!/3!/5! tail permutations xác nhận optimum 6/189/1248 cho ba bài nhỏ; không hard-code route trong solver.
- GA operators: nhiều seed trên 3/4/6/15/26/42/48, parent bất biến, OX ví dụ cụ thể, inversion n=3, rates 0/1, selection ties/minimization, elites không sửa score/chọn lặp index 0.
- Solver: population lẻ P=9, chính xác số evaluations, global best khi final population xấu hơn (controlled test), history monotonic, RNG global không đổi, reproducibility bỏ qua elapsed, cancel trước/sau callback/giữa generation, partial budget chính xác, time limit, max_iterations, zero-cost mọi selection×mutation.
- Integration: CLI subprocess headless, JSON round trip, validate và lỗi tiếng Việt, EHO chưa triển khai báo rõ, benchmark CSV/JSON/summary 5 seed và lưu run FAILED, schema/protocol EHO độc lập không import EHO/GUI.

## Một run CLI thực

```text
distance=1225
tour=0 → 1 → 14 → 13 → 12 → 11 → 10 → 9 → 7 → 6 → 5 → 8 → 4 → 3 → 2 → 0
seed=42; iterations=250; evaluations=19580; runtime=0.235404s; status=MAX_ITERATIONS
```

Đây là lần chạy cuối; lần trước cùng seed/config cũng distance=1225 nhưng runtime=0.238810s. Runtime không thuộc cam kết deterministic. Report nhỏ `example_ga15_seed42.json` giữ route/core/config/counters, bỏ history chỉ ở bản tóm tắt; full JSON với history ở outputs/runs/ga-15-42.json.

## Benchmark GA nhiều seed

Config thực: `experiments/configs/baseline.json`. Seeds `[11,23,37,53,71]`, population 80, generations/max_iterations 250, tournament k3, OX 0.9, inversion 0.15, elites 2, random-only, local search OFF. Full run evaluations = 80 + 250×78 = **19580** ở mọi run. Không callback/render trong benchmark, thời gian chỉ solver, không loader/export/validation ngoài solver.

| Dataset | Runs hợp lệ | Distance mean ± sample std | Min / median / max | Runtime mean (s) | Evaluations/run |
|---|---:|---:|---:|---:|---:|
| 03Cities-6 | 5 | 6.00 ± 0.00 | 6 / 6 / 6 | 0.146244 | 19580 |
| 04Cities-189 | 5 | 189.00 ± 0.00 | 189 / 189 / 189 | 0.157096 | 19580 |
| 06Cities-1248 | 5 | 1248.00 ± 0.00 | 1248 / 1248 / 1248 | 0.174855 | 19580 |
| 15Cities-1194 | 5 | 1200.20 ± 13.86 | 1194 / 1194 / 1225 | 0.236574 | 19580 |
| 26Cities-937 | 5 | 977.20 ± 18.27 | 960 / 972 / 998 | 0.303020 | 19580 |
| 42Cities-699 | 5 | 781.00 ± 23.29 | 741 / 788 / 802 | 0.404949 | 19580 |
| 48Cities-33523 | 5 | 37969.80 ± 1056.48 | 36578 / 38225 / 39314 | 0.460955 | 19580 |

Raw thật: `experiments/reports/ga_p0_raw.csv`. Summary machine-readable có đầy đủ mean/std/median/min/max cả distance và runtime, counts failed/success ở `ga_p0_summary.json`. Bảng tạo tự động `ga_p0_table.md`. Full structured JSON từng seed có route/history/config/environment/run_id tại `outputs/benchmarks/ga-p0/` (gitignore). Lần chạy benchmark đầu cũng 35 valid và cùng distance, runtime khác; bảng ở đây là lần cuối, không chọn seed có lợi để tính trung bình. Khi rerun cùng output_dir các file sẽ bị ghi đè; đổi output_dir để bảo tồn nhiều đợt đo.

Known optimum/gap để trống trong registry/raw, chưa xác minh provenance và từng phần tử từ upstream. Không suy luận optimum 42 chỉ vì route tuần tự có cost=699. Benchmark **chỉ GA**, không gọi là so sánh GA–EHO. Legacy cũ khác operator/budget/seed, nên không so runtime để tuyên bố speedup. Các run có result hợp lệ khi chạm time/evaluation budget vẫn lưu stopping_reason; lỗi solver/validation được lưu FAILED và error, không bỏ khỏi raw. Dataset/config lỗi trước run làm fail-fast với thông báo CLI, chưa có ExperimentRecord riêng cho lỗi nạp dataset.

## Profiling và đề xuất có số liệu

Profile cuối trên 48 city seed42: 7.043.058 function calls, tổng dưới profiler 1.837s, solver 1.717s. Cumulative (có lồng nhau, **không cộng trực tiếp**) objective wrapper ~0.714s, OX ~0.702s, validate_route ~0.291s, selection ~0.178s. Bản text đầy đủ: `experiments/reports/profile_ga48.txt`. Đây là run **bật profiler**, không thay thế runtime benchmark không profiler (~0.461s trung bình 5 seed trên cùng máy).

Ưu tiên tối ưu tiếp theo nếu leader cần: đo microbenchmark OX để giảm duyệt/index modulo/lặp len trên tail; giữ output deterministic và permutation tests. Objective validation có chi phí nhưng chưa bỏ khỏi đường mặc định; nếu đề xuất fast path nội bộ, cần invariant/test chứng minh và thống nhất objective counting trước. Rank hiện sort mỗi lần chọn parent: profile riêng trước ablation lớn, có thể chuẩn bị ranking một lần/generation. Chưa làm tối ưu này, chưa đổi NumPy, chưa tuyên bố “đã tối ưu” hoặc nhanh hơn legacy. Default 48 city dưới một giây trung bình trong batch này đủ smoke headless, không chứng minh GUI responsive.

## Giới hạn và việc kế tiếp

P0 GA có kiểm thử, không đồng nghĩa toàn bộ P0 dự án đã xong. Chưa test clean install trên máy thứ hai, Tkinter UI/cancel bằng nút, ảnh render bằng mắt, TSPLIB semantics, EHO, PMX, formal type/lint check hoặc ablation operators nhiều seed. Chưa có xác nhận quyền sử dụng code/dataset bằng văn bản. Chưa tạo PR/commit.

Thứ tự task: (1) leader review API/ownership và provenance/permission; (2) ba thành viên EHO triển khai riêng khi nhận lệnh, giữ common contract + tests; (3) GA P1 PMX/ablation và profile có trước/sau; (4) GUI Tkinter worker/queue và benchmark liên thuật toán theo evaluation budget sau khi EHO pass tests. Không bắt đầu các giai đoạn đó trong lần này.
