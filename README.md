# GA-EHO-TSP

**Genetic Algorithm and Elephant Herding Optimization for the Traveling Salesman Problem**

## Overview

This repository contains a university Artificial Intelligence course project focused on solving the **Traveling Salesman Problem (TSP)** using two metaheuristic optimization algorithms:

- **Genetic Algorithm (GA)**
- **Elephant Herding Optimization (EHO)**

The project aims to implement, visualize, and experimentally evaluate both algorithms across different TSP instances.

## Project Objectives

The primary objectives of this project are:

1. Implement the Genetic Algorithm for solving TSP.
2. Implement Elephant Herding Optimization for solving TSP.
3. Develop an interactive application for visualizing TSP solutions.
4. Evaluate solution quality, convergence behavior, and computational performance.
5. Conduct experiments using multiple TSP benchmark datasets.

## Technologies

**Programming Language**

- Python

**Planned Libraries**

- NumPy
- Matplotlib
- Tkinter

Additional dependencies will be documented as development progresses.

## Cách chạy

Thực hiện các lệnh dưới đây từ thư mục gốc repository, với **Python 3.11 trở lên**.

### 1. Tạo môi trường và cài thư viện

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
```

Nếu không activate được trong PowerShell, dùng `.\.venv\Scripts\python.exe` thay cho `python` trong các lệnh tiếp theo. Đặt project ở đường dẫn ngắn nếu Windows báo lỗi đường dẫn quá dài khi cài Jupyter.

### 2. Chạy giao diện GA

```powershell
python -m ga_eho_tsp.gui
# hoặc, từ root repository:
python Demo.py
```

Hai lệnh mở cùng form **Tkinter + ttk + Matplotlib**. Chọn dataset, preset hoặc chỉnh tham số rồi bấm **Chạy GA**; **Dừng** trả best đã tìm được. Xem các tab Tuyến đường, Hội tụ, Chi tiết và lưu JSON/CSV/PNG. Sơ đồ tròn của các ma trận chỉ minh họa, không phải vị trí địa lý. EHO đang phát triển, chưa thể chạy. Xem [hướng dẫn GUI](docs/gui_guide.md) và [bàn giao EHO](docs/eho_handoff.md).

### 3. Kiểm tra dữ liệu và chạy GA bằng CLI

```powershell
python -m ga_eho_tsp.cli validate --dataset data/06Cities-1248.txt
python -m ga_eho_tsp.cli solve --algorithm ga --dataset data/15Cities-1194.txt --seed 42 --json outputs/ga.json
```

Kết quả hiển thị distance, tour đóng vòng, seed, iterations, evaluations, runtime và stopping reason. File JSON giữ route 0-based không gắn lại city 0 ở cuối. Hiện chỉ có solver GA; EHO chưa triển khai.

Ví dụ chọn PMX và mixed initialization, giới hạn 6.000 evaluations:

```powershell
python -m ga_eho_tsp.cli solve --algorithm ga --dataset data/48Cities-33523.txt --seed 42 --crossover-method pmx --initialization-method mixed --max-evaluations 6000 --json outputs/ga-pmx.json
```

### 4. Chạy benchmark

```powershell
python -m ga_eho_tsp.cli benchmark --config examples/ga_benchmark.json
```

Config mẫu chạy 7 ma trận × 5 seed, mỗi run tối đa 6.000 evaluations. CSV, JSON và summary được tạo tại `outputs/benchmarks/ga-example/`. Chạy lại cùng output_dir sẽ ghi đè kết quả; sửa output_dir nếu muốn giữ nhiều đợt đo. Đường dẫn dataset trong config được tính tương đối với vị trí file JSON.

### 5. Chạy notebook

```powershell
jupyter notebook
```

Mở ba notebook trong `Experiment/`, chọn kernel `.venv` đã cài thư viện, rồi **Restart Kernel & Run All**. Trong VS Code: **Select Kernel → Python Environments → .venv**. Có thể mở Jupyter từ root hoặc `Experiment/`. Giữ `MODE = 'QUICK'` cho lần đầu; Full Mode là tùy chọn chạy nhiều seed hơn.

Nếu notebook báo không import được `ga_eho_tsp`, kiểm tra đúng kernel và chạy lại `python -m pip install -r requirements.txt` bằng interpreter đó; không chỉnh sys.path.

## Kiểm tra sau khi chạy

### 1. Kiểm tra môi trường và cả 7 ma trận

```powershell
python -m pip check
Get-ChildItem data -Filter *.txt | ForEach-Object {
    python -m ga_eho_tsp.cli validate --dataset $_.FullName
    if ($LASTEXITCODE -ne 0) { throw "Dữ liệu không hợp lệ: $($_.Name)" }
}
```

Mong đợi `No broken requirements found` và cả 7 ma trận hợp lệ.

### 2. Đối chiếu kết quả GA độc lập

Sau khi chạy ví dụ tạo `outputs/ga.json` ở trên:

```powershell
python -c "import json; from ga_eho_tsp.data.matrix_loader import load_matrix; p=load_matrix('data/15Cities-1194.txt'); r=json.load(open('outputs/ga.json', encoding='utf-8')); assert r['is_valid']; assert r['best_distance']==p.route_length(r['best_route']); h=r['history']; assert all(b['best_so_far']<=a['best_so_far'] for a,b in zip(h,h[1:])); assert h[-1]['evaluations']==r['evaluations']; print('PASS: route, distance, history và evaluations')"
```

Chạy lại cùng dataset, seed và cấu hình phải cho cùng route, distance và numeric history; runtime có thể khác. Không coi số trong tên dataset là optimum đã xác minh.

### 3. Kiểm tra benchmark và notebook

```powershell
python -c "import json; r=json.load(open('outputs/benchmarks/ga-example/summary.json', encoding='utf-8')); assert r['total_runs']==35 and r['failed_runs']==0; assert all(s['successful_runs']==5 for s in r['summary']); print('PASS: 35 benchmark runs')"
```

Ba notebook phải Run All từ kernel mới không có traceback, hiển thị bảng và biểu đồ. Repository hiện không có thư mục `tests/`; các bước trên là kiểm tra sau chạy, không thay thế toàn bộ regression suite đã được lưu ngoài repo.

Với GUI: chạy 3/15/48 city, kiểm tra tour có đủ thành phố và khép vòng 1-based; nhập sai mutation rate để xác nhận thông báo lỗi; chạy budget lớn rồi Dừng để nhận `CANCELLED`. Chạy lại cùng cấu hình và seed, lưu JSON để đối chiếu route, distance, evaluations và numeric history với CLI (không so elapsed). Bộ kiểm tra và giới hạn nghiệm thu GUI được ghi tại [gui_guide.md](docs/gui_guide.md).

### Academic Reference

Slowik, A. (Ed.). _Swarm Intelligence Algorithms: A Tutorial_. CRC Press, 2020.

## License

Original authorized contributions are licensed under [MIT](LICENSE). Third-party datasets and inherited/reference material whose licenses are unverified are excluded from that grant; see [source attribution](docs/source_attribution.md).
