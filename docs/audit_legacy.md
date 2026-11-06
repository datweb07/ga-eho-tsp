# Audit repository thật — 05/11/2026

Đã đọc hết `GUIDELINES.md` (940 dòng, FINAL.MD V1.0). **Không có file tên `final.md`**; không tạo bản sao khác tên hoặc sửa baseline. GUIDELINES là file untracked đã có trước khi làm việc. Không phát hiện AGENTS.md trong workspace. Đã đọc toàn bộ các Python, README, .gitignore; parse mọi cell source của ba notebook bằng JSON (37/20/43 cells), xem metadata/count outputs. Không chạy lại các notebook có vòng lặp không giới hạn và không xác minh ảnh output như kết quả mới.

## Cây thật trước khi sửa và phân loại

```text
ga-eho-tsp/
├── .gitignore                       [config]
├── GUIDELINES.md                    [docs: frozen specification, untracked]
├── README.md                        [docs]
├── Demo.py                          [legacy/current app: Tkinter]
├── benchmark_all.py                 [experiment: script bổ sung, tác giả unknown]
├── visualize_run.py                 [experiment/current app: tác giả unknown]
├── src/
│   ├── __init__.py                   [legacy]
│   ├── GA.py                         [legacy/current solver]
│   └── TSP.py                        [legacy/current domain + visualization]
├── data/                            [data: explicit matrices]
│   ├── 03Cities-6.txt
│   ├── 04Cities-189.txt
│   ├── 06Cities-1248.txt
│   ├── 15Cities-1194.txt
│   ├── 26Cities-937.txt
│   ├── 42Cities-699.txt
│   └── 48Cities-33523.txt
└── Experiment/                      [experiment: legacy notebooks]
    ├── Experiment 1-2.ipynb
    ├── Experiment 3.ipynb
    └── Experiment 4.ipynb
```

Đã loại .git, .venv, cache khỏi cây. Ban đầu không có tests, pyproject, requirements, LICENSE, domain package, EHO hoặc output nghiên cứu mới. README nói planned NumPy/Matplotlib/Tkinter, bỏ sót NetworkX đang import trong TSP; không có lock dependency. `src/__init__.py` chỉ `from . import *`. Remote repo hiện tại: datweb07/ga-eho-tsp; attribution upstream là repo ThienNguyen3001, không đánh đồng hai repo.

## Call graph/API legacy

| Entry point | Function → input/output | Phụ thuộc và nguy cơ |
|---|---|---|
| Demo.py → UI.run_algorithm (65–88) | parse số/form/file → read_matrix → genetic_algorithm → dict hiển thị | sys.path theo cwd, os.listdir(data), Tkinter main thread chạy solver đồng bộ; chỉ bắt ValueError |
| benchmark_all.py → run_benchmarks (62–104) | 7 config khác nhau → dict route/distance/fitness → in bảng gap | chèn src vào sys.path; time.time; không seed/evaluation count; gọi mọi hậu tố tên file là ground truth không kiểm chứng |
| visualize_run.py → run_and_plot (17–57) | filename + params → GA → convergence và TSP.visualize | đổi route closed 1-based về open 0-based đúng ở dòng 56; plt.show hai lần; nhãn “tối ưu” quá mạnh |
| GA.genetic_algorithm (218–261) | n_cities, distances, P,G,rate,operator strings → route closed 1-based/distance/fitness | random + numpy.random global; không validation; không seed param; không global archive |
| initialize → TSP.generate_random_route (6–9) | n → list [0]+shuffled 1..n−1 | random global; không kiểm tra n |
| GA.fitness (211–216) → TSP.compute_route_distance (14–18) | population → list tour costs | fitness append route[0], objective lại modulo; thêm self-loop 0→0, hiện diagonal=0 nên **không tính đôi cạnh đóng vòng** |
| GA.selection (67–76) | population,costs,name → P//2 parent references | elitism/tournament/rank/roulette; không survivor elitism; enum sai trả [] |
| GA.crossover (146–155) | parents,name → 2 list routes | prefix order, single-point, repaired two-point, uniform no-op; unknown trả [],[] |
| GA.mutate (200–209) | mutable route, rate,name → route | swap/inversion/insertion sửa in-place; scramble tạo list khi áp dụng; unknown [] |
| TSP.read_matrix (20–26) | path → list[list[int]] | whitespace int, không header/dimension/finite/symmetry validation |
| TSP.visualize (28–64) | matrix, route 0-based → plt.show | NetworkX complete graph + circular_layout, không tọa độ địa lý; không validate route |
| Notebook solve wrappers | ../src + ../data → GA dict → plots/histogram | cwd phụ thuộc notebook; không phải package; xem phân tích bên dưới |

Stopping legacy chỉ `range(generations)`; history ghi min **trước** tạo con ở mỗi vòng nên thiếu quần thể cuối. Best cuối được tính độc lập nhưng không có early stopping/cancel/time budget, evaluations hoặc solver-only runtime contract.

## Phát hiện theo mức độ

Các dòng dưới trỏ tới bản giữ nguyên trong `legacy/`; số dòng khớp file ban đầu. Không thấy CRITICAL gây phá dữ liệu/bảo mật từ kiểm tra này. HIGH là lỗi tính đúng/thực nghiệm; không tự nâng mọi điểm thành CRITICAL.

| Mức | File/function/dòng | Input tái hiện / bằng chứng và tác động |
|---|---|---|
| HIGH | original_src/GA.py elitism_selection 5–12 | scores [10,20,30,40], P=4 → chọn index 0 hai lần, scores đổi [0,20,30,40]. Đây không phải survivor elitism; population sụp đa dạng |
| HIGH | GA.py uniform_crossover 123–144 | parents (0,1,2,3)/(0,3,2,1): random()<1 luôn true → con bằng parent; repair không chạy trên parent hợp lệ |
| HIGH | GA.py genetic_algorithm 239–255 | 15 city, random.seed(0), P=10,G=10,mutation=1,tournament,order/swap: đã thấy cost 2180 trong history nhưng return 2559. Không global best |
| HIGH | GA.py roulette_wheel_selection 47–64 | mọi cost=6 → adjusted total=0, pick=0, current>=pick ngay index 0. **Không chia 0/crash** trong bản thật; thiên vị chọn đầu |
| MEDIUM | GA.py swap_mutate 180–185 | rate áp dụng n−1 lần/route; khác một Bernoulli của inversion/insertion/scramble, làm benchmark tham số khó diễn giải; tự swap cũng có thể xảy ra |
| HIGH | GA.py genetic_algorithm 233–244 | P=5,G=3: sizes ở fitness [5,4,4], mất cá thể. P=2/3: selected chỉ 1 phần tử → random.sample(...,2) ValueError; tournament nhỏ cũng có nguy cơ |
| MEDIUM | GA.py inversion_mutate 157–164; scramble 167–178 | route [0,1,2], rate=1: start:end chỉ 1 phần tử → không đổi. Endpoint cuối không thuộc segment. Mutation in-place có thể sửa caller/parent nếu dùng trực tiếp |
| MEDIUM | GA.py order_crossover 78–88, single_point 90–98 | cùng seed/parents → cùng công thức prefix fill, không phải OX hai điểm chuẩn. two_point sửa permutation nhưng không phải PMX; chưa chứng minh semantics như tên |
| MEDIUM | GA.py fitness 211–216, result 256–257; TSP.py 14–18 | core list open 0-based; trả output closed 1-based. Với diagonal 0 cost vẫn đúng; với diagonal khác 0 fitness thêm self-edge, best cuối khác fitness; ma trận lỗi không bị reject |
| HIGH | GA.py 1–3, rank_selection 29–45 | seed random đơn lẻ không seed NumPy: notebooks Experiment1-2 rank không reproducible; global state ảnh hưởng run khác |
| HIGH | original_scripts/benchmark_all.py 15–59,62–104 | một run/config mỗi dataset, budgets khác nhau, không seed/evaluations; optimum chỉ hard-code. Không thể dùng làm đối chiếu công bằng/khẳng định improvement |
| LOW | TSP.py visualize 38; visualize_run.py 39 | circular_layout chỉ topology, không địa lý; nhãn “tối ưu” không có chứng minh |
| HIGH | GA.py 3; Demo.py 5–8; src/__init__.py | `python -c "import src.GA"` ở root → ModuleNotFoundError: No module named 'TSP'; chạy script chèn sys.path thì được |
| HIGH | TSP.py read_matrix 20–26; GA dispatch 67–76,146–155,200–209 | matrix jagged/âm/sai n không validation; enum sai trả mảng rỗng và lỗi muộn. Demo catch số không bao phủ file/index/algorithm errors |
| MEDIUM | original_demo/Demo.py UI.run_algorithm 79–81 | solver chạy ngay trên main Tk thread → thiết kế chặn event loop khi lâu; chưa đo độ đơ UI thực tế |
| HIGH | original_experiments/Experiment 4.ipynb cells 4,6,8,12,14,21,24,26,30,33,36,38,42 | `while distance != target`/`>threshold` không giới hạn số lần → có thể treo và cherry-pick run đạt target, không hợp lệ làm benchmark trung bình |

Kiểm tra mục 3.1 đủ cả 12: lỗi roulette là bias chứ không division-by-zero; representation hiện không làm sai cost trên 7 matrix zero diagonal; visualization conversion script mới đã đúng; không gán lỗi không có thật. Không tự sửa code legacy để lấy baseline đẹp.

## Notebook

- Experiment 1-2: 37 cells; wrapper seed random=9 mỗi solve, không seed NumPy; dataset 15 city. So sánh 4 bộ selection/crossover/mutation cùng đổi ba yếu tố, rồi khảo sát P=100/500/1000, G=100/500/1000, rates 0.01/0.05/0.1 và phối hợp. Không nhiều seed/thống kê runtime/evaluations; các kết luận “tối ưu/gần tối ưu”, elitism bảo toàn best và uniform trộn ngẫu nhiên không được code hỗ trợ. Output cũ không được tái nhận là bằng chứng mới.
- Experiment 3: 20 cells; 1000 runs trên 3/4/15/26/42/48 (không 6), không quản seed; abs difference làm tròn, histogram thêm một bin tại 0 giả có count=0, không phải gap phần trăm. Không chạy lại 6000 runs; kết luận phần trăm cũ chưa kiểm chứng.
- Experiment 4: 43 cells; 15/26/42/48, lặp đến đạt target rồi vẽ run được chọn; có run đổi P=500 xuống 400 trong vòng while cell42. Không chạy các vòng không chặn; cần viết lại experiment có budget và lưu mọi run.

## Baseline đã chạy trước khi di chuyển file

Môi trường Python 3.11.9 Windows, NumPy 2.4.6, Matplotlib 3.11.2, NetworkX 3.6.1. Chưa có pytest; hiện đã cài pytest 8.3.5 phục vụ bộ mới.

- `python -c "import src.GA"`: FAIL như lỗi import trên.
- Smoke headless bằng inline Python với sys.path=src, seed random/NumPy=42, P20/G10 trên 7 file: PASS; raw route/cost/history/runtime ở `experiments/reports/legacy_baseline.json`. Seed là chuỗi RNG liên tiếp giữa các run, không phải 42 reset cho mỗi dataset.
- `python benchmark_all.py` trước di chuyển: PASS 7/7, distances 6/189/1248/1219/1060/729/36891; console làm tròn runtime 0.00/0.00/0.02/0.15/0.60/1.20/1.61 s. Không seed nên không cam kết tái lập; không dùng gap “chuẩn” từ script làm bằng chứng optimum.
- `$env:MPLBACKEND='Agg'; python visualize_run.py`: PASS headless, distance 1333; hai warning FigureCanvasAgg non-interactive. Chỉ xác minh solve + đường code dựng hình, **không xác minh hiển thị/GUI tương tác**.
- Script `experiments/scripts/audit_legacy.py` sau archive: thực sự chạy và lưu `legacy_regressions.json`, gồm lỗi global-best seed0, odd sizes và checksum source. Legacy code nguyên vẹn, script đổi đường dẫn để kiểm tra có kiểm soát.
- Lần in notebook đầu gặp UnicodeEncodeError do console cp1258; chạy lại với PYTHONIOENCODING=utf-8 đã đọc được toàn bộ source. Không có test framework ban đầu.

## Kiểm tra dữ liệu, nguồn và quyền sử dụng

Cả 7 đều square/symmetric/diagonal-zero/finite/nonnegative. Sample route là `(0,1,...,n−1)` và đóng cạnh qua objective. Dimension/sample cost: 3/6; 4/224; 6/1248; 15/1312; 26/1140; 42/699; 48/157553. SHA256 đầy đủ trong `legacy_baseline.json` và `data/README.md`; file chuyển vị trí giữ nguyên byte, đã đối chiếu lại checksum. Exhaustive permutation trên ba file nhỏ bằng tests xác nhận optimum 6/189/1248 độc lập, nhưng registry vẫn để None đến khi bổ sung provenance/verification metadata chính thức.

Đã mở [repo upstream](https://github.com/ThienNguyen3001/Travelling-Salesman-Genetic-AI-Final) và [FSU TSP](https://people.sc.fsu.edu/~jburkardt/datasets/tsp/tsp.html) ngày 05/11/2026. Upstream root không thấy LICENSE; README ghi nhóm Nguyễn Ngọc Thiện, Nguyễn Minh Nhựt, Nguyễn Trọng Hưởng, Trần Viết Gia Huy, có tham khảo FSU. FSU mô tả att48/dantzig42/fri26 cùng các mức 33523/699/937 và nêu MIT cho thông tin trên trang. **Chưa đối chiếu từng phần tử các file local với file FSU, chưa xác lập quyền phân phối bộ local hoặc toàn bộ code qua tuyên bố của trang khác.** Nguồn 3/4/6/15 chưa được xác minh. Không nâng known optimum chỉ từ trùng dimension/tên. Không có PDF giảng viên hoặc chương sách EHO trong workspace để kiểm tra nội dung/quyền dùng lại; chưa sao chép nội dung các tài liệu đó.

## Mapping bảo tồn → implementation mới

| Legacy function/file | Module mới đề xuất/đã làm | Decision | Rationale |
|---|---|---|---|
| TSP.generate_random_route | domain/operators.py + ga/initialization.py | reuse idea, rewrite | Fixed 0, tuple, RNG injection |
| TSP.compute_distance/compute_route_distance | domain/objective.py + models.TSPProblem | rewrite | Một objective có validation/closing edge |
| TSP.read_matrix | data/matrix_loader.py | rewrite | Lỗi rõ, checksum, shared validation |
| TSP.visualize | visualization/routes.py giai đoạn sau | archive | Circular layout cần nhãn minh họa; chưa viết GUI |
| GA.elitism_selection | ga/survivor.py | rewrite | Survivor giữ index tốt nhất; bỏ parent selection lỗi |
| GA.tournament_selection | ga/selection.py | reuse idea, rewrite | Một parent/lần, RNG riêng, validate k |
| GA.rank_selection/roulette_wheel_selection | ga/selection.py | rewrite | Không NumPy, equal-cost an toàn, weights có tài liệu |
| GA.order_crossover/single_point_crossover | ga/crossover.py OX | rewrite | OX hai điểm thật, bỏ menu tên trùng ngữ nghĩa |
| GA.two_point_crossover/uniform_crossover | không dùng ở app mới | remove from current, archive | Không giữ toán tử lỗi; PMX P1 chưa làm |
| GA.swap/inversion/insertion/scramble_mutate | ga/mutation.py | rewrite | Một rate/cá thể, không mutate parent, inclusive endpoints |
| GA.fitness | TSPProblem.route_length | rewrite | Loại tự thêm start, đếm objective nhất quán |
| GA.selection/crossover/mutate dispatch | GAConfig + operator modules | rewrite | Enum lạ bị reject, không silent [] |
| GA.genetic_algorithm | ga/solver.py | rewrite | Archive, evaluation/history, stop contract |
| Demo.UI | gui/* giai đoạn sau | archive | Bảo tồn, không giới thiệu GUI mới giả |
| benchmark_all.run_benchmarks | experiments/benchmark.py + CLI wrapper | rewrite | 5 seed, cùng budget/config, raw CSV/JSON |
| visualize_run.run_and_plot | visualization/* giai đoạn sau | archive | Không mang logic legacy vào core mới |
| notebook solve/calculate_deviation/plot_* | experiments/benchmark.py; plots sau | archive/rewrite measurement | Loại cherry-picking, không giữ số liệu cũ làm kết quả mới |
| src/__init__.py | ga_eho_tsp/__init__.py | rewrite | Package src-layout cài editable |

Các file gốc di chuyển vào legacy/original_src, original_demo, original_scripts, original_experiments; dữ liệu sang data/legacy. Không sửa nội dung gốc; đối chiếu HEAD normalize CRLF/LF đều bằng nhau (HEAD chuẩn hóa LF, working tree Windows có CRLF nên hash byte với git blob có thể khác). Hash bản làm việc giữ trong báo cáo regression. Experiment/ rỗng không còn file được quản lý. Root Demo.py/visualize_run.py không giữ launcher giả khi GUI/visualization mới chưa có; README chỉ dẫn rõ trạng thái.

## Chưa kiểm tra / giới hạn

Chưa chạy tương tác Tkinter, notebook end-to-end, hình plot bằng mắt, môi trường sạch trên máy thứ hai, TSPLIB parser, quyền tác giả bằng văn bản, nhận diện dataset từ checksum upstream, Turnitin/tài liệu học thuật đầy đủ. Chưa có benchmark GA–EHO hoặc speedup before/after cùng budget. Chưa tạo PR/commit hoặc gửi tin cho thành viên. Kết quả tests/benchmark mới xem `experiments.md`; không coi audit này là hoàn thành toàn đồ án.
