# Đề tài 6: Ứng dụng thuật toán Genetic Algorithm và Elephant Herding Optimization cho bài toán người du lịch (Traveling Salesman Problem - TSP)

**GA P1/P2 đã nghiệm thu để bàn giao. EHO chưa được triển khai; GUI chưa có.** Trương Thành Đạt là leader, phụ trách GA và hợp đồng dùng chung; ba thành viên còn lại phát triển D-EHO độc lập ở giai đoạn sau. Package Python 3.11+, version0.2.0. Đặc tả đóng băng ở [GUIDELINES.md](GUIDELINES.md), không sửa trong lần cleanup này.

## Cài đặt trên Windows

Chạy từ root repository, ưu tiên đường dẫn ngắn như `D:\ga-eho-tsp`:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pip check
```

`requirements.txt` cài editable package bằng `-e .`, Matplotlib, Jupyter Notebook, ipykernel và nbclient. Core GA/CLI dùng stdlib; không cài package này từ PyPI. Không cần cài riêng NumPy vì notebook không import trực tiếp. Tkinter là phần GUI dự kiến sau này, đi cùng Python Windows; Linux có thể cần package hệ thống `python3-tk`, không dùng `pip install tkinter`.

Nếu PowerShell không activate được, dùng trực tiếp `.\.venv\Scripts\python.exe` thay `python`. Nếu Windows báo lỗi đường dẫn quá dài khi cài JupyterLab, chuyển project/venv sang đường dẫn ngắn rồi cài lại; quy trình này đã được kiểm chứng với một venv QA sạch độc lập.

## CLI và benchmark

```powershell
python -m ga_eho_tsp.cli validate --dataset data/legacy/06Cities-1248.txt
python -m ga_eho_tsp.cli solve --algorithm ga --dataset data/legacy/15Cities-1194.txt --seed 42
python -m ga_eho_tsp.cli solve --algorithm ga --dataset data/legacy/48Cities-33523.txt --crossover-method pmx --initialization-method mixed --max-evaluations 6000 --seed 42
python -m ga_eho_tsp.cli benchmark --config examples/ga_benchmark.json
```

Default: random initialization, tournament k3, OX rate0.9, inversion rate0.15, population80, elitism2, generations/max_iterations250, seed42. Có rank/roulette, PMX, NN/mixed, swap/insertion/scramble, diversity, opt-in stagnation/adaptive và bounded2-opt. 2-opt OFF mặc định, bật bằng `--local-search-enabled --local-search-max-moves 1 --local-search-max-probes 10`; label `GA+2-opt`, mọi probe tính vào evaluations. Adaptive bật bằng `--adaptive-mutation`. Không bảo đảm các biến thể tốt hơn control.

Đường dẫn trong benchmark JSON được resolve **tương đối với file config**. Chỉ giữ [một config mẫu](examples/ga_benchmark.json):7dataset×5seed, mỗi run6000evaluations. Benchmark sinh CSV/JSON/Markdown vào ignored `outputs/`; thư mục này không được gửi trong bản bàn giao và sẽ được tạo khi người dùng chạy. Chọn output_dir khác để giữ một đợt đo mới thay vì ghi đè.

Core route tuple 0-based, khóa0 đầu tiên, không gắn0 cuối; CLI đóng vòng để hiển thị. Chi phí là đơn vị của ma trận, không mặc định km. Hai iteration caps chạy theo min; để chạy hơn250 thế hệ phải tăng cả generations và max_iterations. Hậu tố tên file là hint, không phải optimum đã xác minh.

## Ba notebook thí nghiệm

```powershell
jupyter notebook
```

Mở notebook, chọn kernel `.venv` đã cài rồi **Restart Kernel & Run All**. Trong VS Code: **Select Kernel → Python Environments → .venv**. Nếu `ModuleNotFoundError: ga_eho_tsp`, kiểm tra interpreter và chạy lại `python -m pip install -r requirements.txt` bằng chính interpreter đó; không chỉnh sys.path. Có thể mở Jupyter từ root hoặc `Experiment/`.

| Notebook | Nội dung Quick Mode | Runs | Run All thực đo tại root |
|---|---|---:|---:|
| [Experiment 1-2](Experiment/Experiment%201-2.ipynb) | Operators OFAT, sensitivity, hội tụ, diversity |80|6.742s|
| [Experiment 3](Experiment/Experiment%203.ipynb) | Phân bố/độ ổn định, best-observed, kiểm chứng nhỏ |30|3.999s|
| [Experiment 4](Experiment/Experiment%204.ipynb) |15/26/42/48city, NN/PMX/adaptive/2-opt, accounting |120|9.063s|

Quick dùng seeds `[11,23,37,53,71]`, có evaluation/time/run caps. Full Mode25seeds là opt-in, chưa chạy nghiệm thu phiên này. Notebook giữ bảng và biểu đồ thực, không có vòng chạy đến target hoặc giả định optimum từ filename. Thời gian trên chỉ là lần đo tại máy nghiệm thu, có thể khác khi chạy lại.

## Cấu trúc và bàn giao EHO

```text
src/ga_eho_tsp/
  domain/          # TSPProblem, configs, RunResult, objective, protocols
  data/            # matrix loader và registry
  algorithms/ga/   # GA P1/P2 độc lập
  experiments/     # benchmark.py, export.py dùng thật
  cli.py
data/legacy/       # 7 ma trận giữ nguyên checksum
Experiment/        # đúng 3 notebook mới
examples/          # đúng 1 JSON benchmark mẫu
docs/              # kiến trúc, GA, thí nghiệm, attribution
```

Team EHO dùng `domain.models`, `domain.objective`, `domain.protocols`, `domain.operators` và loader chung; không sửa GA/objective để thích nghi với EHO. `EHOConfig` chỉ là schema, CLI `--algorithm eho` báo chưa triển khai. Xem [contract bàn giao](docs/architecture.md), [thuật toán GA](docs/algorithm_ga.md), [số đo và gates](docs/experiments.md), [nguồn và backup](docs/source_attribution.md), [dataset](data/README.md).

**Đã chạy166regression tests trước khi xóa tests theo chỉ thị leader. Repo cuối không còn automated pytest regression suite; đây là thay đổi có chủ đích so với cây đích trong GUIDELINES và là rủi ro khi phát triển EHO.** Code tests, kết quả cũ và thay đổi chưa commit đã được backup ngoài repository. Không chạy `pytest` để nghiệm thu bản bàn giao này; kết quả xác minh phiên release và notebook được trình bày trong docs/experiments.md. Team nên thống nhất cách khôi phục regression suite khi bắt đầu phát triển EHO.

Optimum/licensing/provenance của7dataset chưa xác minh đầy đủ; không có TSPLIB loader, EHO hoặc GUI. Không khẳng định heuristic tối ưu toàn cục hay tốc độ tốt hơn trên mọi máy. Nguồn tham chiếu ban đầu: [ThienNguyen3001/Travelling-Salesman-Genetic-AI-Final](https://github.com/ThienNguyen3001/Travelling-Salesman-Genetic-AI-Final); không tự gán license cho nội dung kế thừa.
