# Đề tài 6: Ứng dụng thuật toán Genetic Algorithm và Elephant Herding Optimization cho bài toán người du lịch (Traveling Salesman Problem - TSP)

Nhóm 4 sinh viên năm 3, kế hoạch 8 tuần. **Trương Thành Đạt** phụ trách 100% GA, shared TSP domain, kiến trúc và nghiệm thu; ba thành viên còn lại phụ trách EHO. GA P0 hiện chạy headless và có kiểm thử. **EHO: planned / not implemented**; chỉ có schema EHOConfig dùng chung. GUI mới Tkinter + ttk + Matplotlib triển khai ở giai đoạn tích hợp sau.

Đặc tả đóng băng thực có trong workspace: [GUIDELINES.md](GUIDELINES.md) (tiêu đề FINAL.MD, V1.0); không có file `final.md`. Không sửa nội dung đặc tả khi triển khai.

## Cài đặt và chạy (Python 3.11+)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e '.[dev]'
python -m ga_eho_tsp.cli validate --dataset data/legacy/06Cities-1248.txt
python -m ga_eho_tsp.cli solve --algorithm ga --dataset data/legacy/15Cities-1194.txt --seed 42 --json outputs/runs/ga.json
python -m pytest -q
python -m ga_eho_tsp.cli benchmark --config experiments/configs/baseline.json
```

Core/CLI không cần NumPy, NetworkX, Matplotlib hay display. Không cần activate nếu dùng trực tiếp `.\.venv\Scripts\python.exe`. Cài editable một lần để package import được từ root hoặc cwd khác. `requirements-dev.txt` khóa dependency test của môi trường đã kiểm tra; extra legacy chỉ cần khi chạy script audit legacy.

GA hỗ trợ tournament (mặc định), rank, roulette_wheel; OX; inversion (mặc định), swap, insertion, scramble; random initialization, elitism, global best, seed, history, evaluations, cooperative cancel/time/evaluation/iteration caps. Các flag ví dụ:

```powershell
python -m ga_eho_tsp.cli solve --algorithm ga --dataset data/legacy/26Cities-937.txt --population-size 81 --generations 100 --max-iterations 100 --selection-method rank --mutation-method swap --mutation-rate 0.15 --max-evaluations 8000
python benchmark_all.py --config experiments/configs/baseline.json
python -m ga_eho_tsp.cli --help
```

Core route tuple 0-based, start 0, không khép vòng. CLI tour đóng vòng; JSON best_route vẫn là core route. Ma trận whitespace n×n, n≥3, đối xứng, hữu hạn, không âm, diagonal=0. Hậu tố tên dataset chỉ là hint, không tự coi optimum. Xem [data/README.md](data/README.md).

Chưa có PMX, TSPLIB loader, local search, adaptive mutation, GUI mới hoặc EHO solver. `--algorithm eho` báo chưa triển khai, không fallback. Hai giới hạn `generations`/`max_iterations` cùng tồn tại; chạy min hai giá trị. Cancel/time kiểm tra sau bước khởi tạo atomic và trước từng offspring; xem hợp đồng để hiểu trạng thái partial.

## Tài liệu và bằng chứng

- [Audit và lỗi legacy](docs/audit_legacy.md), [kiến trúc/API bàn giao](docs/architecture.md), [GA và toán tử](docs/algorithm_ga.md).
- [Kiểm thử, runtime và benchmark thực](docs/experiments.md); raw CSV/summary nhỏ được chọn ở `experiments/reports/`, full JSON/history ở `outputs/` bị gitignore.
- [Legacy được bảo toàn và attribution](legacy/README.md). Code, Demo, notebooks cũ chuyển vào legacy; Demo.py/visualize_run.py tại root đã archive, chưa có launcher GUI mới.

Nguồn tham chiếu ban đầu: [ThienNguyen3001/Travelling-Salesman-Genetic-AI-Final](https://github.com/ThienNguyen3001/Travelling-Salesman-Genetic-AI-Final). Chưa thấy LICENSE trong bản local/upstream root đã xem; quyền phân phối code/dataset kế thừa chưa được xác minh. Cần leader làm rõ với tác giả; không gán license của nhóm lên phần kế thừa. Phần GA chính thức được viết lại và cần nhóm review, hiểu và giải thích trước khi nộp. Sách seminar *Swarm Intelligence Algorithms: A Tutorial* là nguồn dự kiến cho EHO, chưa được đọc/triển khai trong giai đoạn này.
