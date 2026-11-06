# MASTER PROMPT — XÂY DỰNG GIAO DIỆN FORM CHO GA VÀ NGHIỆM THU BÀN GIAO EHO

> **Dùng cho Codex/Cursor/AI coding agent tại thư mục gốc `ga-eho-tsp`.**
> **Hành động yêu cầu: đọc repo thật, chỉnh sửa code thật, chạy kiểm chứng thật; không chỉ viết kế hoạch.**
> Chủ nhiệm GA, kiến trúc chung: **Trương Thành Đạt**. Dự án: **Đề tài 6 — Ứng dụng Genetic Algorithm (GA) và Elephant Herding Optimization (EHO) cho Traveling Salesman Problem (TSP)**.

## 0. Bối cảnh đã được xác minh — KHÔNG tự giả định lại

- Repository hiện đã có package `src/ga_eho_tsp/`, GA P1/P2, `domain/`, `data/`, CLI, benchmark/export, ba notebook trong `Experiment/`, `GUIDELINES.md`, `README.md`, `requirements.txt`, `pyproject.toml`.
- Code GA chính thức là `src/ga_eho_tsp/algorithms/ga/solver.py`; không còn API cũ `src.GA.genetic_algorithm` và `src.TSP.read_matrix`.
- API công khai: `solve(problem: TSPProblem, config: GAConfig, *, progress_callback=None, stop_requested=None) -> RunResult`.
- `load_matrix(path)` trả `TSPProblem`; `RunResult` có `best_route`, `best_distance`, `iterations_completed`, `evaluations`, `elapsed_seconds`, `seed`, `history`, `stopping_reason`, `metadata`.
- `EHOConfig` và solver protocol đã có, nhưng **EHO SOLVER CHƯA ĐƯỢC TRIỂN KHAI**.
- 7 dataset `.txt` ở `data/`: `03Cities-6`, `04Cities-189`, `06Cities-1248`, `15Cities-1194`, `26Cities-937`, `42Cities-699`, `48Cities-33523`. Chúng là **ma trận khoảng cách**, không phải dữ liệu tọa độ địa lý. Không suy đoán optimum từ tên file.
- Giao diện Tkinter `Demo.py` của đàn anh là mã tham chiếu, dùng import/hàm cũ nên không tương thích với package hiện tại. Chỉ học cách bố trí form/chọn tham số; không copy API/hàm cũ.
- Trong `GUIDELINES.md`, Mục 10 **đã khóa lựa chọn GUI là Tkinter + ttk + Matplotlib**; Mục 11 yêu cầu `python -m ga_eho_tsp.gui`. **Không đổi sang web, PySide6, Streamlit, Flet hoặc framework khác.**
- Các lượt cleanup đã cố ý xóa `tests/`; đây là rủi ro. Không được viện dẫn "166 passed" từ lượt cũ làm bằng chứng code GUI mới đã được kiểm tra.
- Repo đang có khả năng chứa thay đổi **chưa commit**. Nghiêm cấm `git reset --hard`, `git clean -fd`, checkout bỏ thay đổi, xóa dữ liệu, tự commit/push hoặc đổi nhánh.

## 1. Mục tiêu chính, thứ tự ưu tiên

**P0 — bắt buộc hoàn thành trong lượt này:**

1. Xây dựng **giao diện desktop form thực sự có thể chạy** bằng Tkinter + ttk, tích hợp trực tiếp GA hiện tại, không chạy demo giả.
2. Tạo lệnh `python -m ga_eho_tsp.gui` và file **`Demo.py` ở root làm launcher mỏng**. Hai cách khởi động phải dẫn đến cùng một ứng dụng.
3. Người dùng chọn dataset, nhập/chỉnh tham số GA, Run/Stop, xem kết quả, tuyến đường, biểu đồ hội tụ; xuất dữ liệu hợp lệ.
4. Thiết kế một điểm mở rộng rõ ràng để nhóm EHO đưa solver vào sau, **không implement EHO trong lượt này** và không tạo kết quả EHO giả.
5. Kiểm tra GA core/contract và chạy lại các smoke tests sau thay đổi. Không tùy tiện sửa thuật toán đã ổn định chỉ vì giao diện cần format khác.
6. Hoàn thiện tài liệu cài đặt/chạy form và tài liệu bàn giao EHO.

**P1 — làm nếu P0 đã chạy ổn:** tối ưu trải nghiệm giao diện, preset dễ hiểu, xuất hình/CSV/JSON, xem fitness/diversity và bảng thông số chạy. **Không ưu tiên theme/animation so với correctness.**

## 2. Audit trước khi sửa (phải báo kết quả ngắn gọn)

Đọc tất cả các file sau và truy import thực tế:

- `GUIDELINES.md` (nhất là Mục 6, 7, 8, 10, 11, 12), `docs/architecture.md`, `docs/algorithm_ga.md`, `docs/experiments.md`, `README.md`.
- `src/ga_eho_tsp/domain/models.py`, `objective.py`, `protocols.py`, `operators.py`.
- `src/ga_eho_tsp/algorithms/ga/{solver,selection,crossover,mutation,initialization,local_search,monitoring,survivor}.py`.
- `src/ga_eho_tsp/data/{matrix_loader,registry}.py`, `cli.py`, `experiments/{benchmark,export}.py`.
- `pyproject.toml`, `requirements.txt`, `.gitignore`, `examples/ga_benchmark.json`.
- Các notebook và dữ liệu để chắc GUI không phá workflow hiện có.
- Nếu `Demo.py` cũ có sẵn trong workspace, đọc rồi đối chiếu; nếu không thì ghi rõ là không có, **không giả vờ đã đọc**.

Ghi nhận trạng thái Git (`git status --short`), chỉ ra API thật, default GA thật và các vấn đề UI cần xử lý. **Sau audit, tiến hành triển khai trực tiếp, không chờ leader trả lời nếu không có blocker thực sự.**

## 3. Cấu trúc code yêu cầu

Ưu tiên tách UI khỏi domain và GA, không nhồi toàn bộ vào `Demo.py`:

```text
ga-eho-tsp/
├── Demo.py                      # wrapper siêu mỏng: gọi main() của GUI mới
├── requirements.txt             # giữ tương thích với notebook/CLI
├── src/ga_eho_tsp/
│   ├── algorithms/ga/            # KHÔNG chỉnh khi không có bug được tái hiện
│   ├── domain/                   # GIỮ NGUYÊN contract GA–EHO
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── __main__.py           # python -m ga_eho_tsp.gui
│   │   ├── app.py                # layout + vòng đời cửa sổ
│   │   ├── controls.py           # widgets, input validation, preset
│   │   ├── controller.py         # task worker, queue, lifecycle/stop
│   │   ├── plots.py              # vẽ tuyến và convergence; chỉ presentation
│   │   └── export.py             # xuất dữ liệu/ảnh từ RunResult, nếu cần
│   └── ...
├── docs/
│   ├── gui_guide.md             # hướng dẫn cài/chạy/dùng, giới hạn
│   └── eho_handoff.md           # API + checklist bàn giao (mới)
└── ...
```

Có thể hợp nhất các module UI rất nhỏ khi hợp lý, nhưng phải tách **main UI / worker orchestration / plotting**. Không tạo hàng chục lớp hoặc thiết kế plugin phức tạp.

## 4. Thiết kế cửa sổ: dễ demo trong lớp, tiếng Việt, thao tác được

Sử dụng **một cửa sổ chính** có bố cục responsive cơ bản, ttk styles thống nhất, cuộn khi cần, kích thước tối thiểu vừa màn hình laptop 1366×768. Không tạo 10 cửa sổ con, không yêu cầu trình duyệt.

**Vùng A — Dataset TSP**

- Dropdown liệt kê 7 file `.txt` thật từ `data/`; có nút **Duyệt file** để mở ma trận whitespace đối xứng cùng định dạng, không quảng cáo hỗ trợ `.tsp` khi chưa viết loader TSPLIB.
- Hiển thị tên, n thành phố, kiểm tra vuông/đối xứng, nguồn file, lỗi dữ liệu bằng tiếng Việt.
- Đường dẫn tìm từ vị trí package/repo và cho phép file tùy chọn; không hardcode `D:\\ga-eho-tsp` hay giả định current working directory; không `sys.path.append('./src')`.
- Chú ý data currently là matrices, **không có tọa độ thật**.

**Vùng B — Thuật toán và tham số**

- Thuật toán: `Genetic Algorithm (GA)` **sử dụng được**; `Elephant Herding Optimization (EHO)` hiển thị **"Đang phát triển — nhóm EHO sẽ bổ sung"**, không cho bấm Run EHO khi chưa tồn tại implementation. Không làm EHO giả hoặc gọi GA rồi đổi tên kết quả.
- GA controls phản ánh chính xác `GAConfig`: `population_size`, `generations`, `max_iterations`, `max_evaluations`, `seed`, `selection_method` (tournament/rank/roulette_wheel), `tournament_size`, `crossover_method` (OX/PMX), `crossover_rate`, `mutation_method` (inversion/swap/insertion/scramble), `mutation_rate`, `elite_count`, `initialization_method` (random/nearest_neighbor/mixed), `nn_seed_fraction`.
- Chế độ **Nâng cao** có `stagnation_patience`, `adaptive_mutation` + các min/max/patience, `local_search_enabled` + moves/probes, `time_limit_seconds`, `record_history_every` nếu thực sự hữu ích.
- Giá trị mặc định phải lấy từ schema thật (GAConfig), KHÔNG copy default của Demo.py cũ. Cấu hình P2 `adaptive_mutation` và `2-opt` **OFF mặc định**; khi bật 2-opt hiển thị rõ **"GA + 2-opt (biến thể thực nghiệm)"**, không giới thiệu như thuật toán GA thuần.
- Preset `Demo nhanh`, `Mặc định`, `Giới hạn evaluations`; không được đổi ngầm tham số mà không hiển thị cấu hình cuối. Có nút Reset về default và tooltip/mô tả thuật ngữ.
- Dùng validate theo GAConfig, hiển thị lỗi ngay cạnh trường hoặc hộp thoại rõ ràng; không bắt lỗi chung thành thông báo "hãy nhập số" nếu sai cấu trúc, range hay path.

**Vùng C — Điều khiển chạy**

- `Chạy GA`, `Dừng`, trạng thái `Sẵn sàng/Đang chạy/Đã hủy/Hoàn thành/Lỗi`, runtime, seed, số thế hệ, `evaluations`, `best_so_far`, stopping reason.
- Đảm bảo **không đóng băng UI** với 48 city và budget lớn. Solver chạy trong `threading.Thread` và truyền tiến độ bằng `queue.Queue`; main Tk chỉ cập nhật từ `root.after(...)`. **Worker tuyệt đối không chỉnh widget, canvas, messagebox hay Tk variables.**
- Stop dùng `threading.Event` nối đúng `stop_requested` của solver; tránh kill thread cứng. Nút Stop chỉ xác nhận yêu cầu hủy, chờ worker phát result; nếu thuật toán quá nhanh có thể hoàn tất trước khi Stop.
- Khóa hoặc snapshot toàn bộ dataset/config đang chạy; không cho bấm chồng hai solver jobs; nút/close window xử lý worker đang chạy an toàn. Không dùng `time.sleep()` trên main thread.
- Progress callback nhận `IterationStat` snapshot; cập nhật tối đa ~5–10 lần/giây cho chart tránh lag. Không dùng phần trăm tiến độ giả nếu run dừng bởi time/cancel/stagnation.
- Phân biệt `MAX_ITERATIONS`, `MAX_EVALUATIONS`, `TIME_LIMIT`, `CANCELLED`, `STAGNATION`; `history` có thể chứa hai snapshots cùng iteration khi partial, dùng `evaluations` làm trục khi cần.

**Vùng D — Kết quả và trực quan hóa**

- Kết quả: `best_distance`, tour khép vòng 1-based (`1 → ... → 1`) kèm n, seed, iterations, evaluations, runtime và trạng thái. Core giữ route 0-based không có city cuối lặp lại.
- Tab **Tuyến đường**: Matplotlib embedded FigureCanvasTkAgg, vẽ đầy đủ cạnh khép kín, đánh dấu bắt đầu/kết thúc. Khi `TSPProblem.coordinates` tồn tại thì dùng tọa độ; với 7 matrix hiện tại dùng circular layout và **luôn có dòng chữ nhìn thấy: “Sơ đồ minh họa, không phải vị trí địa lý”**. Không gọi đây là đường đi trên bản đồ thực tế hoặc quãng đường Euclid theo vị trí vẽ.
- Tab **Hội tụ**: vẽ `best_so_far` theo iterations/evaluations, có thể thêm `best_current`; nhãn rõ ràng và cập nhật sau khi có RunResult. Không vẽ metric bịa ra từ kết quả chưa có.
- Tab **Chi tiết**: bảng config thực chạy, history cơ bản, evaluation count, metadata, cảnh báo tùy chọn 2-opt, thông tin dataset; nếu có known optimum được xác thực mới hiển thị gap.
- Tab **So sánh GA/EHO** (tùy chọn): chỉ hiển thị placeholder "Đợi nhóm EHO" lúc này; không tính bằng số liệu giả. Để mở rộng sau khi EHO team hoàn thành, GUI phải gọi solver EHO qua common contract mà không sửa code GA.
- Xuất kết quả JSON (phù hợp `RunResult`); xuất PNG từ figure; xuất CSV history nếu triển khai. File dialog không ghi đè file người dùng khi chưa được chọn/xác nhận. Không phát sinh outputs trong repo chỉ vì mở UI.

## 5. EHO integration seam — đặc biệt quan trọng trước khi bàn giao

- `domain/models.py`, `domain/objective.py`, `domain/operators.py`, `domain/protocols.py` **không đổi public API, tên trường hoặc semantics**.
- GA solver tiếp tục import domain, không import GUI/EHO. GUI phụ thuộc một **adapter/dispatcher gọn** dùng chuẩn `solve(problem, config, progress_callback, stop_requested)`; có GA entry thật, EHO chỉ có trạng thái chưa khả dụng hoặc lazy import khi module thật tồn tại.
- Không viết `algorithms/eho/solver.py` giả, không sửa `EHOConfig` để hợp GUI, không thay đổi CLI benchmark để pretends EHO supported.
- Không sửa GA để gửi dữ liệu tọa độ, đẩy progress sang Tk, hoặc nhúng figure. Những việc đó thuộc adapter/GUI.
- Ghi `docs/eho_handoff.md`: public API, route contract, objective & dataset, RNG, history/partial behavior, evaluation accounting, stop/progress, `EHOConfig` và cách đăng ký EHO vào UI sau này. Nêu rõ trạng thái hiện tại **EHO TODO**, trình tự tích hợp, cách xác minh, và danh sách file EHO team được phép sửa.
- Bàn giao là **GA ready for EHO integration**, KHÔNG phải "Đồ án hoàn chỉnh" vì EHO chưa có.

## 6. Xác minh GA và tránh sửa quá tay

**Trước và sau khi dựng UI**, chạy ít nhất:

```powershell
python -m pip install -r requirements.txt
python -m pip check
python -m ga_eho_tsp.cli validate --dataset data/06Cities-1248.txt
python -m ga_eho_tsp.cli solve --algorithm ga --dataset data/15Cities-1194.txt --seed 42
python -m ga_eho_tsp.cli solve --algorithm ga --dataset data/48Cities-33523.txt --seed 42 --crossover-method pmx --initialization-method mixed --max-evaluations 6000
python -m ga_eho_tsp.cli benchmark --config examples/ga_benchmark.json
python -m compileall -q src
```

- Không khẳng định các lệnh đã pass nếu chưa **chạy thật**; nếu môi trường thiếu GUI/display, report rõ Headless PASS / GUI manual NOT VERIFIED.
- So khớp một mẫu GA GUI và GA CLI với **cùng dataset, cùng seed, cùng TOÀN BỘ GAConfig**, cùng solver version: route, best_distance, evaluations, numeric history cần khớp; elapsed có thể khác. Hãy chú ý cả `max_iterations` và `generations`.
- Kiểm tra tour qua `problem.route_length(result.best_route)`; đúng permutation bắt đầu 0, không trùng/mất city; best_so_far không tăng; mỗi evaluation count đúng với cap; reproducibility khi chạy lại cùng input.
- Edge cases: 3/4 city; 15/48 city; seed0; odd/even population; PMX/OX; mutation 0/1; max_evaluations=population_size; time_limit; Stop; invalid dataset; invalid parameter; không có dataset trong cwd; đóng cửa sổ khi worker đang chạy.
- Không tái lập 166 tests đã xóa bằng lời nói. Nếu cần một vài kiểm tra tạm, chạy trong shell hoặc thư mục ngoài repo và báo rõ. **Không tự tái tạo cả `tests/` khi leader đang yêu cầu repo gọn**, nhưng ghi rủi ro regression test thiếu trong bàn giao.
- **Nếu GA có lỗi thật**, đưa ra input tái hiện và bằng chứng rồi sửa tối thiểu, kiểm chứng lại. **Nếu không có lỗi, giữ nguyên byte các module `algorithms/ga/` và `domain/`**; chỉ thêm GUI/launcher/docs/dependencies.

## 7. Cài đặt và trải nghiệm người dùng

- Cập nhật `requirements.txt` và/hoặc `pyproject.toml` khi thực sự cần; `matplotlib` đã có, `tkinter` trên Windows thường đi cùng Python nhưng có thể phải cài gói hệ thống trên Linux. Không đưa `tkinter` vào pip requirements nếu không có package phù hợp.
- README phải có lệnh mới, từ root Windows PowerShell:

```powershell
python -m pip install -r requirements.txt
python -m ga_eho_tsp.gui
# hoặc
python Demo.py
```

- Đảm bảo `python Demo.py` chỉ gọi GUI mới; không có bản `genetic_algorithm` copy trong file root.
- `docs/gui_guide.md` chỉ dẫn thao tác từng bước, các preset, ý nghĩa biểu đồ circular layout, cách Stop, lưu kết quả, cách nhóm EHO gắn solver.
- Cập nhật README không mâu thuẫn với LICENSE/repository thực; không xóa `GUIDELINES.md` hoặc các notebook.
- Không auto-commit, auto-push, auto-tag, không sửa `.git`/`.venv`, không xóa dữ liệu hoặc ghi đè notebook executed.

## 8. Definition of Done — cổng nghiệm thu không được bỏ qua

Chỉ ghi **"GA GUI READY — SẴN SÀNG BÀN GIAO CHO NHÓM EHO"** khi tất cả các điều kiện bắt buộc đều PASS:

1. Có file `Demo.py` thật ở root và package `ga_eho_tsp.gui` thật với launcher chạy được.
2. Giao diện đúng **Tkinter+ttk+Matplotlib**, có thể chọn dataset và nhập GAConfig hợp lệ.
3. Bấm Run gọi đúng core GA hiện tại và trả đúng kết quả, không mock.
4. Vẽ tour khép vòng và convergence, dùng labels đúng (circular schematic ≠ địa lý).
5. Run dài không khóa main UI, có Stop cooperative hoạt động, không race khi đóng.
6. Lỗi input/dataset được báo rõ mà GUI vẫn dùng được.
7. CLI, benchmark, 7 dataset và 3 notebook không bị phá; `domain/*`/GA API không đổi khi không có bug.
8. Bộ smoke 3/15/48 city và so khớp GUI-vs-CLI với cùng cấu hình đã chạy; ghi pass/fail trung thực.
9. README, requirements, docs/gui_guide.md và docs/eho_handoff.md được cập nhật.
10. EHO chưa triển khai, nhưng integration seam rõ và không cần sửa logic GA khi EHO team bắt đầu.

**Trình bày cuối lần chạy trong chat:**

- Bảng `File created / modified / deleted` với lý do.
- Lệnh đã chạy và kết quả thực tế, phân biệt **automated/headless** với **GUI manual**.
- Ảnh giao diện chụp thực tế nếu có display; nếu không có, không bịa ảnh.
- Bảng 10 release gates PASS/FAIL/NOT VERIFIED, kèm blockers.
- Cách leader chạy demo trong VS Code/Windows, cách team EHO bắt đầu code.
- Trạng thái GA/EHO/GUI riêng biệt; **không nói "tất cả ổn" nếu form chưa chạy thật**.

**BẮT ĐẦU NGAY:** đọc repo và `GUIDELINES.md` → audit → code GUI & Demo.py → kiểm thử thực tế → tài liệu & handoff. Không dừng ở việc lập roadmap hoặc báo cáo ý tưởng.
