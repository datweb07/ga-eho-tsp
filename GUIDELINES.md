# FINAL.MD — ĐẶC TẢ ĐÓNG BĂNG & MASTER PROMPT TRIỂN KHAI GA–EHO–TSP

> **Trạng thái:** BASELINE V1.0 — tài liệu nguồn sự thật duy nhất (*single source of truth*) của nhóm.
> 
> **Cách dùng:** Đặt file này tại thư mục gốc repository `ga-eho-tsp/`, mở repository bằng AI coding agent (Codex/Cursor hoặc công cụ tương đương), yêu cầu agent **đọc toàn bộ `final.md` rồi thực thi Mục 21**. Agent phải đối chiếu code thực tế trước khi thay đổi bất cứ thứ gì. **Ngay trong lần thực thi đầu tiên, chỉ audit toàn bộ repository rồi triển khai giai đoạn GA; KHÔNG triển khai thuật toán EHO cho tới khi có lệnh riêng.**
>
> **Nguyên tắc:** Đây là một tài liệu vừa mô tả hệ thống sẽ hoàn thiện ra sao, vừa là chỉ thị triển khai kỹ thuật. Các quyết định kiến trúc và hợp đồng dữ liệu bên dưới được khóa làm baseline. Mọi thay đổi có tác động tới giao diện giữa GA–EHO phải có đề xuất thay đổi, lý do, tác động, cập nhật test và được leader chấp thuận.

---

## 0. CHỈ THỊ ƯU TIÊN CAO NHẤT CHO AI CODING AGENT

Bạn là **Senior Python Engineer + AI/Optimization Engineer + Technical Lead**, chịu trách nhiệm chuẩn hóa một đồ án học phần Trí tuệ nhân tạo đủ rõ ràng để 4 sinh viên năm 3 hoàn thành, giải thích, kiểm thử và bảo vệ trong **8 tuần**.

**Bạn phải làm theo thứ tự sau:**

1. **Đọc toàn bộ `final.md`** và ghi nhận đây là đặc tả chính thức; không tự đổi tên đề tài, phương pháp GA/EHO, dạng biểu diễn TSP, quy tắc đo hiệu năng, GUI hoặc cơ cấu phân công.
2. **Quét toàn bộ repository thực tế**, bao gồm `src/`, `data/`, `Experiment/`, `Demo.py`, `benchmark_all.py`, `visualize_run.py`, `README.md`, `.gitignore`, file cấu hình và mọi mã nguồn/nghiên cứu từ đàn anh đã được đưa vào. Không suy đoán rằng file nào tồn tại nếu chưa kiểm tra.
3. **Chạy baseline (nếu môi trường cho phép)** mà không chỉnh mã cũ; mô tả cách chạy, phụ thuộc, API, đầu vào/đầu ra, thuật toán hiện có, notebook, dữ liệu, đường đi chương trình, lỗi thực chứng và mức độ tái sử dụng. Nếu không chạy được, ghi rõ lỗi cụ thể; tuyệt đối không tuyên bố đã chạy.
4. **Lập sơ đồ tái cấu trúc và bảo toàn mã nguồn cũ.** Cô lập mã kế thừa trong `legacy/` (hoặc cơ chế tham chiếu không phá lịch sử) sau khi xác định rõ xuất xứ; mã thuật toán đánh giá chính thức phải được nhóm cài đặt lại, diễn giải được và có test. Không xóa không lưu bản gốc, không sao chép mù quáng.
5. **Xây dựng bộ lõi chung TSP và hợp đồng dữ liệu chung cho GA/EHO**, kèm kiểm thử nền tảng.
6. **Triển khai GA hoàn chỉnh trước**, gồm các toán tử, hiệu năng, khả năng tái lập, kiểm thử, CLI và bộ đo kết quả. Có thể triển khai/điều chỉnh GUI GA ở cuối giai đoạn này nếu lõi và test đã đạt.
7. **Dừng ở điểm bàn giao GA**, tổng kết phần đã làm, những file đã sửa, test thực chạy, cách sử dụng, những điểm chưa đạt, API ổn định và danh sách việc EHO sẵn sàng nhận. **Không tự động viết EHO**, trừ phần interface chung hoặc test hợp đồng không chứa thuật toán EHO.
8. Khi leader ra lệnh giai đoạn EHO, mới triển khai EHO dựa trên cùng TSP core/contract; tiếp đó tích hợp GUI, benchmark, báo cáo.

**Hạn chế bắt buộc:** Không tự ý đưa thêm A*, ACO, PSO, Simulated Annealing hay thuật toán ngoài đề tài để khoe tính năng. Có thể dùng khởi tạo nearest-neighbor hoặc toán tử 2-opt như thành phần hỗ trợ có giải thích rõ, nhưng không giới thiệu chúng thành thuật toán chính thứ ba; cấu hình benchmark mặc định phải công bằng.

**Phong cách lập trình:** Python thuần, PEP 8, type hints đầy đủ, tên hàm/biến tiếng Anh rõ nghĩa, docstring tiếng Việt dễ đọc, không viết tắt khó hiểu, không dồn logic vào một file, không tạo abstraction vô ích, không dùng biến trạng thái toàn cục, không nuốt exception, không in output rác; nguyên tắc *correctness → reproducibility → measurement → optimization → GUI*.

---

## 1. THÔNG TIN DỰ ÁN CỐ ĐỊNH

| Hạng mục | Thông tin chính thức |
|---|---|
| Repository | `ga-eho-tsp` |
| Tên đăng ký | **Đề tài 6: Ứng dụng thuật toán Genetic Algorithm và Elephant Herding Optimization cho bài toán người du lịch (Traveling Salesman Problem - TSP)** |
| Bảng phân loại | **Hàng GA × cột TSP = số 6** |
| Danh sách mô tả 20 đề tài | Nội dung tương ứng là mục số **8** trong danh sách tuần tự 1–20; **khi điền bảng phân loại/đăng ký hiện tại, dùng số 6** |
| Môn học | Trí tuệ nhân tạo |
| Trường | UEH — Đại học Kinh tế Thành phố Hồ Chí Minh |
| Nhóm | 4 thành viên |
| Trưởng nhóm | **Trương Thành Đạt** — phụ trách toàn bộ GA, kiến trúc chung, tích hợp và nghiệm thu |
| Nhánh thuật toán seminar | **Elephant Herding Optimization (EHO)** |
| Ngôn ngữ | Python |
| Đầu ra chính | GA giải TSP, Discrete EHO giải cùng TSP, GUI form, benchmark minh bạch, báo cáo và demo |
| Thời hạn thiết kế | 8 tuần kể từ ngày nhóm bắt đầu phát triển; không tự gán ngày nộp khi chưa có thông tin |

**Tuyên bố mục tiêu:** Xây dựng ứng dụng desktop hỗ trợ nhập/chọn bài toán người du lịch, giải bằng GA hoặc EHO trên **cùng dữ liệu và hàm mục tiêu**, trực quan hóa tuyến đường, theo dõi hội tụ, điều chỉnh tham số, đo chất lượng nghiệm/chi phí tính toán và chạy thực nghiệm nhiều lần có thể tái lập.

**Không cam kết:** Tìm nghiệm tối ưu toàn cục cho mọi TSP, tạo thuật toán mới ở cấp nghiên cứu, mô hình giao thông thời gian thực, định tuyến nhiều xe, VRP, bản đồ GPS trực tuyến, dịch vụ web, phần mềm thương mại hoặc kết quả GA chắc chắn tốt hơn EHO.

---

## 2. QUY ĐỊNH GIẢNG VIÊN VÀ PHẠM VI ĐÁNH GIÁ

### 2.1 Bắt buộc

- Bài toán: Traveling Salesman Problem (TSP).
- Thuật toán chính theo đề tài: Genetic Algorithm (GA).
- Thuật toán seminar bổ sung: Elephant Herding Optimization (EHO), áp dụng **cùng bài toán TSP**.
- Thuật toán được **cài đặt lại từ đầu**, cấu trúc rõ, phân tách hàm và mô tả được từng bước.
- Khai thác sâu trường hợp/biến thể tham số và cách giải của GA; có so sánh GA với EHO trong phạm vi đề tài.
- Có giao diện dạng form bằng Python; có trực quan hóa và demo.
- Báo cáo theo mẫu giảng viên (khi được cung cấp), giải thích nội dung, không chỉ dán ảnh; có báo cáo kiểm tra trùng lặp Turnitin theo cấu hình mặc định, **<30%** như yêu cầu. Chỉ số này không thay thế việc trích dẫn trung thực.
- Thuyết trình, chạy thử và trả lời được câu hỏi sâu về GA, EHO, TSP, thiết kế, hiệu năng, giới hạn.

### 2.2 Phân loại phạm vi

- **P0 — PHẢI CÓ:** Lõi TSP, GA đúng, EHO dạng rời rạc đúng, tải dữ liệu, GUI form tối thiểu, biểu đồ hội tụ/tuyến đường, thí nghiệm có seed, test, README, báo cáo.
- **P1 — NÊN CÓ:** Nhiều toán tử GA, elitism, restart/điều kiện dừng, phân tích tham số, EHO ablation nhỏ, xuất CSV/JSON/PNG, chọn cấu hình chạy tương đương, progress và hủy tác vụ an toàn.
- **P2 — CHỈ LÀM KHI P0/P1 ĐÃ ỔN:** Tinh chỉnh GUI, tối ưu tốc độ sâu, benchmark lớn, nghiên cứu thêm local search, đóng gói executable, đa ngôn ngữ.
- **Ngoài phạm vi:** Thuật toán chính thứ ba, hybrid GA–EHO, máy chủ, tài khoản, database, bản đồ giao thông trực tuyến, GPU, distributed computing, ML training, mô hình VRP.

### 2.3 Quy tắc về nguồn đàn anh

Repository nền tảng: `ThienNguyen3001/Travelling-Salesman-Genetic-AI-Final`.

- Dùng làm **reference/legacy baseline**: xem cấu trúc chương trình, dữ liệu, ý tưởng thuật toán, giao diện và thí nghiệm.
- Mã nguồn công khai **không tự động đồng nghĩa với có quyền sao chép/phân phối**; kiểm tra giấy phép hoặc xin phép tác giả trước khi phân phối phần kế thừa. Nếu chưa rõ, giữ repository Private.
- Vì giảng viên yêu cầu **"cài đặt lại từ đầu"**, phần lõi GA và EHO nộp chính thức phải được nhóm tự xây dựng/cài đặt lại có giải thích, test, commit và đối chiếu. Không trình bày mã tác giả cũ như thành quả tự viết.
- Ghi công đúng README, tài liệu và báo cáo; nếu dùng đoạn mã được cho phép, nêu rõ nguồn, phần được kế thừa, phần chỉnh sửa và ai thực hiện.
- **Không phá hủy code legacy** để còn đối chiếu khi bảo vệ.

---

## 3. KIỂM KÊ KHỞI ĐẦU VÀ NHỮNG ĐIỂM PHẢI AUDIT LẠI

Dựa trên **bản ZIP của repo đàn anh đã được cung cấp để thiết kế tài liệu này**, cấu trúc cũ có:

```text
Travelling-Salesman-Genetic-AI-Final-main/
├── Demo.py
├── README.md
├── .gitignore
├── src/
│   ├── GA.py
│   ├── TSP.py
│   └── __init__.py
├── data/
│   ├── 03Cities-6.txt
│   ├── 04Cities-189.txt
│   ├── 06Cities-1248.txt
│   ├── 15Cities-1194.txt
│   ├── 26Cities-937.txt
│   ├── 42Cities-699.txt
│   └── 48Cities-33523.txt
└── Experiment/
    ├── Experiment 1-2.ipynb
    ├── Experiment 3.ipynb
    └── Experiment 4.ipynb
```

Ảnh chụp workspace mới có thêm `benchmark_all.py`, `visualize_run.py` ở root, cùng `src/`, `data/`, `Experiment/`, `.venv/`, `Demo.py`. **Hai script mới này chưa được kiểm chứng nội dung**; AI phải đọc thật trước khi đề xuất xóa/đổi tên. Nếu repo đã khác bản ZIP, **trạng thái repository mới nhất có ưu tiên làm bằng chứng**, nhưng không được bỏ qua lịch sử nguồn gốc.

### 3.1 Các vấn đề nổi bật cần xác nhận/test trong GA cũ

1. `elitism_selection()` lấy `min(fitness_scores)` nhưng sau khi chọn lại gán điểm của cá thể về `0`; đối với bài toán minimization và khoảng cách không âm, thao tác này có thể khiến cá thể vừa chọn được chọn lặp lại. Phải sửa thiết kế chọn bố mẹ/elitism.
2. `uniform_crossover()` chứa điều kiện `random.random() < 1`, nghĩa là nhánh `else` bất khả thi; phép lai đồng đều như đang tên gọi không thực sự hoạt động.
3. Hàm GA cũ chỉ tìm best của **quần thể cuối cùng** để trả về, không duy trì `global_best` trong mọi vòng lặp; nghiệm tốt có thể mất.
4. `roulette_wheel_selection()` cần xử lý trường hợp mọi điểm fitness bằng nhau (`total_fitness == 0`), cùng công thức chuyển bài toán tối thiểu thành trọng số chọn hợp lệ.
5. `swap_mutate()` áp dụng xác suất trên từng vị trí, trong khi các mutation khác áp dụng một xác suất trên cả cá thể; phải chuẩn hóa ngữ nghĩa tham số trước khi benchmark.
6. Phần sinh con với `population_size // 2` có nguy cơ làm kích thước quần thể thay đổi khi kích thước lẻ; cần ràng buộc/đảm bảo số lượng cá thể.
7. Nhiều toán tử cần test tính hợp lệ của hoán vị, tính bất biến của thành phố gốc `0` và không tác động ngoài ý muốn lên bố mẹ.
8. Tính quãng đường có biểu diễn route đóng vòng không đồng nhất giữa hàm fitness và kết quả; chuẩn hóa một chuẩn duy nhất.
9. Có sử dụng ngẫu nhiên toàn cục (`random`/`numpy.random`), chưa có cơ chế seed thống nhất, khó tái lập kết quả.
10. Đo thời gian và số lần đánh giá hàm mục tiêu chưa được chuẩn hóa; benchmark phải có cùng điều kiện và thống kê đúng.
11. `TSP.py` dùng `networkx.circular_layout()` để vẽ, **không có nghĩa tuyến đường thể hiện tọa độ địa lý thật**; ghi rõ loại hình hiển thị.
12. Đường dẫn import/module cũ và các file root phải được kiểm tra lại trên Windows khi chuyển sang kiến trúc package.

**Không coi các nhận xét trên là bản audit kết thúc.** AI phải chỉ ra file, hàm, khoảng dòng, đầu vào tái hiện, test và tác động. Không bịa lỗi nếu đã được sửa ở repo hiện tại.

### 3.2 Dữ liệu legacy

7 file `.txt` gốc là **ma trận khoảng cách đối xứng, vuông, đường chéo bằng 0, giá trị không âm** trong bản ZIP đã kiểm tra. Tuy nhiên:

- Các số trong tên file như `-937`, `-699`, `-33523` chỉ được coi là **metadata/hint** cho tới khi xác minh từ tài liệu gốc hoặc nghiệm độc lập; không tự nhận tất cả là optimum chính thức.
- Không tự thay ma trận, chỉnh dataset để làm đẹp kết quả, hoặc trộn chi phí từ các quy tắc khoảng cách khác nhau.
- Ghi rõ nguồn, checksum, số thành phố, định dạng và giá trị optimum/known-best **có chứng cứ**.

---

## 4. CÁC QUYẾT ĐỊNH KIẾN TRÚC ĐÃ ĐÓNG BĂNG

1. **Desktop app bằng Tkinter + ttk + Matplotlib**: phù hợp mã nguồn nền và thời hạn 8 tuần. Không đổi đột ngột sang Web/Streamlit/PySide6; nếu muốn đổi GUI phải được leader chấp thuận sau khi thuật toán ổn định. Có thể cải thiện theme, bố cục, responsiveness trong Tkinter.
2. **Python 3.11+** là ngưỡng hỗ trợ; khai báo và khóa các dependency thực tế trong `pyproject.toml` hoặc `requirements.txt` + file dev rõ ràng. Không lạm dụng package chỉ vì tiện.
3. **Package `src/ga_eho_tsp/`**; root là nơi lưu file chạy mỏng, cấu hình và tài liệu, không chứa core logic.
4. **Shared TSP domain** là nguồn định nghĩa objective, đường đi, dữ liệu, validity, kết quả và metrics dùng chung.
5. GA và EHO **là hai solver độc lập**, có cùng API `solve(problem, config, *, progress_callback=None, stop_requested=None) -> RunResult` (có thể chuyển callback thành protocol/typed callable ở code, nhưng hành vi và fields phải giữ ổn định).
6. **Route biểu diễn trong core**: hoán vị `tuple[int, ...]` dài `n`, đánh số **0-based**, phần tử đầu cố định `0`, chứa mỗi thành phố `0..n-1` đúng một lần, **không gắn `0` ở cuối**. GUI/CSV có thể hiển thị `0 → ... → 0` hoặc `1 → ... → 1` sau khi chuyển đổi ở presentation layer.
7. **Mặc định TSP đối xứng** (symmetric TSP, complete weighted graph). Không tự mở rộng ATSP/VRP.
8. **Distance/fitness duy nhất**: cùng `TSPProblem.route_length(route)` cho cả hai solver; objective là **minimize tour length**.
9. **Reproducibility**: mỗi run có seed được truyền tường minh, random generator thuộc từng run; **không gọi ngẫu nhiên toàn cục trong logic solver**.
10. **Benchmark bằng code CLI/headless**, không phụ thuộc GUI, không vẽ biểu đồ trong vòng lặp tính toán, tách thời gian giải khỏi thời gian render/file I/O.
11. **Không cho GUI đóng băng** khi chạy thuật toán: solver chạy ở worker thread/task; GUI chỉ được cập nhật ở main thread qua `queue`/`after`.
12. **No silent fallback**: nhập sai/param sai/dataset không hợp lệ phải báo lỗi có ý nghĩa, không tự chọn lại thuật toán hoặc trả nghiệm giả.
13. **Tất cả logic quan trọng phải test được không cần giao diện**.
14. **Tài liệu `final.md` là baseline**; file docs khác là diễn giải/nhật ký/chi tiết, không được mâu thuẫn baseline.

---

## 5. MÔ HÌNH TOÁN, HỢP ĐỒNG DỮ LIỆU VÀ BẤT BIẾN

### 5.1 Bài toán TSP

Với tập thành phố `V = {0,...,n-1}` và ma trận khoảng cách `D` kích thước `n × n`, tìm chu trình Hamilton có tổng chi phí nhỏ nhất:

`min L(π) = Σ[i=0..n-1] D[π[i], π[(i+1) mod n]]`

Ràng buộc `π[0] = 0`; `π` là hoán vị đầy đủ của `0..n-1`. Cạnh từ thành phố cuối trở lại thành phố đầu **luôn được tính đúng một lần**.

**Tập kiểm tra tối thiểu:**

- `n >= 3`, ma trận vuông `n × n`, số hữu hạn, khoảng cách không âm, đường chéo bằng `0`.
- Đối xứng `D[i][j] == D[j][i]` (sai số số thực được chọn rõ; dữ liệu nguyên dùng so sánh chính xác).
- Không chấp nhận NaN, infinity, ma trận rỗng, thiếu dòng/cột, tuyến có trùng thành phố, thiếu thành phố, khóa `0` bị di chuyển.
- Cạnh off-diagonal có thể bằng 0 với thành phố đồng vị trí; không tự xem là lỗi trừ khi đặc tả dataset yêu cầu.
- Kích thước input hợp lý cho demo; dataset lớn giới hạn bằng cảnh báo hoặc định mức tài nguyên.

### 5.2 Data contracts (tên được đề xuất cố định)

- `TSPProblem`: `name`, `distance_matrix`, `dimension`, `source`, `coordinates | None`, `known_optimum | None`, `metadata`.
- `RunConfigBase`: `seed`, `max_iterations`, `max_evaluations | None`, `time_limit_seconds | None`, `record_history_every`.
- `GAConfig`: `population_size`, `generations`, `selection_method`, `crossover_method`, `crossover_rate`, `mutation_method`, `mutation_rate`, `elite_count`, `initialization_method`, `local_search_enabled`, `local_search_max_moves`, và trường thừa kế từ base nếu phù hợp.
- `EHOConfig`: `clan_count`, `elephants_per_clan`, `iterations`, `alpha`, `beta`, `separation_count_per_clan`, `initialization_method`, `preserve_global_best`, và trường base.
- `IterationStat`: `iteration`, `best_current`, `best_so_far`, `mean_fitness`, `evaluations`, `elapsed_seconds`, `population_diversity | None`.
- `RunResult`: `algorithm`, `problem_name`, `best_route`, `best_distance`, `iterations_completed`, `evaluations`, `elapsed_seconds`, `seed`, `history`, `config_snapshot`, `stopping_reason`, `is_valid`, `metadata`.
- `ExperimentRecord`: dataset, algorithm, seed, config/variant, best distance, known optimum nếu có, relative gap nếu có, runtime, evaluations, run status, environment/version.

Trong code có thể dùng `@dataclass(frozen=True)` cho các bản ghi immutable phù hợp; **đừng serialize object Python tùy tiện**, xuất JSON an toàn bằng chuyển đổi có kiểm soát. Không bắt buộc tạo lớp kế thừa phức tạp khi các dataclass rõ ràng là đủ.

### 5.3 API bắt buộc và ý nghĩa

```python
# HỢP ĐỒNG API MINH HỌA — chưa phải mã triển khai
result = solve(
    problem: TSPProblem,
    config: GAConfig | EHOConfig,
    *,
    progress_callback: ProgressCallback | None = None,
    stop_requested: Callable[[], bool] | None = None,
) -> RunResult
```

- `solve()` hoàn trả dữ liệu, không tự gọi `plt.show()`, không tạo cửa sổ GUI, không tự ghi file.
- Các toán tử nhận RNG `random.Random` được truyền vào; không tự tạo seed mới bên trong toán tử.
- Không sửa `TSPProblem` từ solver.
- `best_route` trong kết quả là permutation **không khép vòng** và `best_distance` được đối chiếu độc lập từ objective.
- `history` tối thiểu ghi nhận trạng thái ở iteration `0` sau khởi tạo và các iteration tiếp theo; nếu chạy không đủ vòng vì `stop_requested`/time budget, kết quả phải ghi đúng trạng thái.
- `best_so_far` **không bao giờ tăng** khi tối thiểu hóa; `best_current` có thể tăng khi quần thể biến động.
- Mỗi lần gọi hàm objective dùng để đánh giá một candidate phải được đếm vào `evaluations`. Cần thống nhất cách đếm và ghi rõ trong báo cáo.
- `relative_gap_percent = 100 * (best_distance - known_optimum) / known_optimum` khi known optimum **đã xác minh và >0**; không có optimum thì để trống, không lấy tên file làm chứng cứ.

---

## 6. CẤU TRÚC THƯ MỤC ĐÍCH — CHÍNH THỨC

```text
ga-eho-tsp/
├── final.md                           # TÀI LIỆU ĐÓNG BĂNG — không sửa tùy tiện
├── README.md                          # Giới thiệu, lệnh cài/chạy, phân công, attribution
├── .gitignore
├── .gitattributes                     # Nếu cần thống nhất line endings / notebook
├── pyproject.toml                     # Package, dependencies, công cụ test/lint
├── requirements.txt                   # Chỉ giữ nếu thật sự cần cho người chạy nhanh
├── Demo.py                            # Compatibility launcher mỏng, nếu cần giữ
├── benchmark_all.py                   # Launcher mỏng, chỉ nếu đang tồn tại/cần tương thích
├── visualize_run.py                   # Launcher mỏng, chỉ nếu đang tồn tại/cần tương thích
│
├── src/
│   └── ga_eho_tsp/
│       ├── __init__.py
│       ├── cli.py                      # Lệnh solve / benchmark / validate
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── models.py               # TSPProblem, configs, result, stats
│       │   ├── objective.py            # route_length và validate route
│       │   ├── operators.py            # Permutation primitives chung, KHÔNG chứa GA/EHO policy
│       │   └── protocols.py            # Solver/Progress contracts
│       ├── data/
│       │   ├── __init__.py
│       │   ├── matrix_loader.py        # Đọc ma trận .txt legacy
│       │   ├── tsplib_loader.py        # TSPLIB95 subset/adapter, P1
│       │   └── registry.py             # Chỉ mục dataset + nguồn + known optimum
│       ├── algorithms/
│       │   ├── __init__.py
│       │   ├── ga/
│       │   │   ├── __init__.py
│       │   │   ├── solver.py           # vòng lặp GA, trạng thái run
│       │   │   ├── initialization.py   # khởi tạo quần thể
│       │   │   ├── selection.py        # chọn bố mẹ
│       │   │   ├── crossover.py        # các crossover hợp lệ TSP
│       │   │   ├── mutation.py         # các mutation hợp lệ TSP
│       │   │   └── survivor.py         # elitism, replacement
│       │   └── eho/
│       │       ├── __init__.py
│       │       ├── solver.py           # vòng lặp EHO rời rạc
│       │       ├── clans.py            # tổ chức đàn, lãnh đạo, chọn thành viên
│       │       ├── discrete_ops.py     # diễn dịch clan update cho permutation
│       │       └── separation.py       # thay thế cá thể yếu, bổ sung đa dạng
│       ├── experiments/
│       │   ├── __init__.py
│       │   ├── benchmark.py            # chạy hàng loạt, seed, fairness
│       │   ├── metrics.py              # mean/std/gap/statistics
│       │   ├── export.py               # CSV/JSON/reproducible metadata
│       │   └── presets.py              # cấu hình demo & benchmark
│       ├── visualization/
│       │   ├── __init__.py
│       │   ├── routes.py               # hình TSP, đóng vòng ở display
│       │   ├── convergence.py          # hội tụ theo iteration/evaluations
│       │   └── comparisons.py          # đối chiếu kết quả đúng đơn vị
│       └── gui/
│           ├── __init__.py
│           ├── __main__.py             # python -m ga_eho_tsp.gui
│           ├── app.py                  # cửa sổ chính
│           ├── controls.py             # form/select/config validation
│           ├── worker.py               # background execution/queue/cancel
│           ├── plots.py                # Matplotlib canvas integration
│           └── views.py                # tab/panel và kết quả
│
├── data/
│   ├── legacy/                       # 7 ma trận gốc (giữ nguyên byte khi có thể)
│   ├── tsplib/                       # Chỉ dataset được chọn và ghi rõ nguồn
│   └── README.md                      # nguồn dữ liệu/định dạng/optimum/checksum
│
├── legacy/                           # Bản tham chiếu có ghi nguồn, tránh import vào app mới
│   ├── README.md
│   ├── original_src/                  # Bảo quản GA.py, TSP.py nếu được phép
│   ├── original_demo/                 # Demo.py gốc nếu cần
│   └── original_experiments/          # notebook gốc nếu cần
│
├── Experiment/                       # Notebook cũ: di chuyển/cô lập có kiểm soát
├── experiments/                      # CẤU HÌNH thực nghiệm và kết quả đã chọn
│   ├── configs/
│   ├── scripts/                      # Script chạy thí nghiệm end-to-end
│   └── reports/                      # Các summary nhỏ có thể commit
│
├── tests/
│   ├── conftest.py
│   ├── test_tsp_problem.py
│   ├── test_data_loaders.py
│   ├── test_route_operators.py
│   ├── ga/
│   │   ├── test_selection.py
│   │   ├── test_crossover.py
│   │   ├── test_mutation.py
│   │   ├── test_ga_solver.py
│   │   └── test_ga_reproducibility.py
│   ├── eho/
│   │   ├── test_clans.py
│   │   ├── test_discrete_ops.py
│   │   ├── test_separation.py
│   │   ├── test_eho_solver.py
│   │   └── test_eho_reproducibility.py
│   └── integration/
│       ├── test_solver_contract.py
│       ├── test_benchmark.py
│       └── test_cli.py
│
├── docs/
│   ├── audit_legacy.md               # Đối chiếu repo cũ với mã mới
│   ├── architecture.md                # Luồng dữ liệu, dependency direction
│   ├── algorithm_ga.md                # Pseudocode, toán tử, tham số
│   ├── algorithm_eho.md               # Công thức gốc và phép chuyển rời rạc
│   ├── experiments.md                 # Phương pháp đo và kết quả, không tự bịa
│   ├── gui_guide.md                   # Hướng dẫn UI + screenshot thật
│   ├── team_plan.md                   # Task ownership và milestone
│   ├── references.md                  # Tài liệu học thuật và attribution
│   └── changelog_decisions.md         # Bản ghi thay đổi so với final.md
│
└── outputs/                           # MẶC ĐỊNH .gitignore: csv/json/png/log tạm
    ├── runs/
    ├── benchmarks/
    └── figures/
```

**Đây là cấu trúc ĐÍCH, không phải yêu cầu phải sinh ra tất cả file rỗng ngay hôm nay.** Tạo folder/file khi tới đúng giai đoạn; không tạo skeleton khổng lồ vô dụng. Nếu repo đã có file cần bảo tồn, tạo mapping rõ ràng `old → new`. Không tạo 2 implementations cùng là nguồn chạy chính thức. Không xóa lịch sử git. Không lồng thêm một `src/` bên trong package.

### Hướng phụ thuộc

`domain` ← `data` / `algorithms.ga` / `algorithms.eho` ← `experiments` / `visualization` ← `gui` / `cli`.

- `domain` không import GUI, algorithm hoặc loader.
- `algorithms.ga` không import `algorithms.eho` và ngược lại.
- GUI không sao chép hàm mục tiêu, không can thiệp population, không tự tính toán một kết quả khác solver.
- `experiments` gọi solver qua interface chung; không hard-code truy xuất biến nội bộ của GA/EHO.

---

## 7. GA — PHẠM VI ĐẦY ĐỦ DO TRƯƠNG THÀNH ĐẠT CHỊU TRÁCH NHIỆM

### 7.1 Mục tiêu nghiên cứu/triển khai GA

Cài đặt **Genetic Algorithm cho TSP dưới dạng hoán vị**, kế thừa *ý tưởng và dữ liệu* GA của đàn anh nhưng cải thiện đáng kể tính đúng, cấu trúc, hiệu năng, khả năng điều chỉnh, độ ổn định và giá trị thực nghiệm. Trọng tâm là **khai thác sâu GA**, không chỉ đạt một tuyến đường trên giao diện.

### 7.2 GA pipeline chuẩn

```text
TSPProblem + GAConfig + seed
  → validate cấu hình/dữ liệu
  → tạo RNG riêng cho run
  → khởi tạo quần thể permutation hợp lệ
  → đánh giá khoảng cách bằng shared objective
  → lưu global_best, iteration history và evaluation_count
  → lặp cho đến khi đạt iteration/evaluation/time/stop criterion:
       → chọn bố mẹ
       → lai ghép theo xác suất crossover_rate
       → đột biến theo xác suất mutation_rate/cá thể
       → kiểm tra tính hợp lệ nghiệm
       → survivor selection + elitism
       → đánh giá, cập nhật global_best và stats
  → trả RunResult hợp lệ
```

### 7.3 Các chức năng GA P0

1. `random_permutation` giữ cố định city `0`.
2. Khởi tạo toàn bộ random; không tạo hai tuyến cùng tham chiếu mutable.
3. **Selection:** `tournament` (default), `rank` và `roulette_wheel` (chọn nếu cần phục vụ thực nghiệm). Bảo đảm hoạt động khi fitness bằng nhau, nhỏ nhất là tốt nhất, phân bố chọn hợp lệ.
4. **Crossover:** Order Crossover chuẩn **OX** (default) và **PMX** (P1); điều chỉnh phép lai nếu giữ điểm xuất phát `0`, chỉ tác động phần `1..n-1`. Các phương pháp trong legacy như `single_point`, `two_point`, `uniform` phải được audit và hoặc triển khai lại đúng ngữ nghĩa permutation, hoặc thay bằng danh mục toán tử có tên chuẩn và chứng minh đúng; **không giữ toán tử lỗi chỉ vì tên cũ**.
5. **Mutation:** `swap`, `inversion` (default), `insertion`, `scramble`; tất cả luôn giữ city `0`, mỗi phương pháp có một ngữ nghĩa `mutation_rate` rõ ràng: xác suất áp dụng mutation cho **cả cá thể**. Các xác suất theo gene phải dùng tham số khác, không lẫn lộn.
6. **Elitism:** là *survivor strategy*, giữ `elite_count` cá thể tốt nhất trực tiếp sang quần thể kế tiếp; không dùng thủ thuật gán fitness=0.
7. Có `crossover_rate`, `mutation_rate`, `population_size`, `generations`, `elite_count`, `selection_method`, `crossover_method`, `mutation_method`, `seed` và validate input.
8. Quần thể giữ kích thước đúng mọi vòng, cả khi kích thước lẻ (nếu cho phép lẻ) hoặc cấu hình bị reject có thông báo rõ.
9. Theo dõi `global_best` đúng, history monotonic cho `best_so_far`, không bỏ qua quần thể khởi tạo và thế hệ cuối.
10. Lưu `evaluations`, thời gian bằng `perf_counter`, `stop_requested`; không bắt `KeyboardInterrupt` rồi âm thầm trả kết quả chưa rõ.
11. Xuất `RunResult` theo hợp đồng mục 5; CLI chạy được trên 7 file ma trận cũ.

### 7.4 Nâng cao GA P1 (chỉ sau khi P0 đúng)

- **Tối ưu nội bộ:** Không tính lại fitness không cần thiết; giảm deep copy, dùng cấu trúc tuple/list hợp lý, hạn chế callback vẽ ở mỗi cá thể; cân nhắc cache route length nếu benchmark chứng minh lợi ích mà không làm sai phép đếm objective.
- **Nearest-neighbor seeding có kiểm soát:** Tùy chọn khởi tạo một phần quần thể bằng tuyến tham lam. Phải ghi chính xác đây là *initialization heuristic*, không phải thuật toán chính riêng; so sánh công bằng với bản random-only và EHO nếu sử dụng cùng chính sách.
- **Adaptive mutation (P1/P2):** Thử nghiệm thích nghi theo mức trì trệ/diversity chỉ khi chứng minh được bằng ablation, không thêm biến thể thiếu cơ sở.
- **Bounded 2-opt local improvement (P2):** Chỉ như operator bổ trợ có switch default OFF; nếu bật, ghi nhãn `GA+2-opt`, đếm objective/evaluations đúng, không dùng làm đối chiếu mặc định với EHO không có local search.
- **Termination:** `max_iterations`, `max_evaluations`, `time_limit_seconds`; optional `stagnation_patience` nếu có test và được leader đồng ý.
- **Ablation:** khảo sát selection, crossover, mutation, population size, mutation rate, elitism và seed; không cần thử toàn bộ tích Descartes (quá tải 8 tuần).

### 7.5 Preset GA dự kiến để khởi chạy

| Parameter | Default đề xuất | Điều kiện |
|---|---:|---|
| `population_size` | 80 | >= 4 và đủ cho selection; kiểm soát giới hạn GUI |
| `generations` | 250 | >= 1 |
| `selection_method` | `tournament` | một trong supported values |
| `tournament_size` | 3 | từ 2 tới `population_size` |
| `crossover_method` | `ox` | permutation-preserving |
| `crossover_rate` | 0.9 | `[0,1]` |
| `mutation_method` | `inversion` | permutation-preserving |
| `mutation_rate` | 0.15 | `[0,1]`, xác suất / cá thể |
| `elite_count` | 2 | `0..population_size-1` |
| `initialization_method` | `random` | baseline công bằng |
| `local_search_enabled` | `False` | giữ nguyên trong benchmark chính |
| `seed` | 42 | có thể thay trong experiment grid |

**Đây là preset xuất phát, không khẳng định tối ưu.** Benchmark nhiều seed để chọn tham số khả thi, không chọn kết quả tốt nhất rồi quảng cáo là thành tích trung bình.

### 7.6 Tiêu chí nghiệm thu GA

- Tất cả toán tử hoạt động với TSP nhỏ `n=3`, `n=4`, `n=6` và dataset lớn hơn khi hợp lệ.
- Route không có city lặp/thiếu; `route[0] == 0`; `route_length` đúng và có vòng quay về.
- Cùng `problem + config + seed + version` → kết quả/diễn tiến nhất quán trên cùng môi trường.
- Có ít nhất 1 test kiểm tra mọi lỗi nghiêm trọng đã audit ở legacy.
- CLI chạy GA headless; có thể xuất report JSON hoặc CSV; không bắt mở Tkinter khi chạy test.
- Trình bày được từng toán tử với ví dụ hoán vị cụ thể và pseudocode.
- So sánh GA cải tiến với phiên bản GA legacy **khi có thể chạy và ghi rõ hạn chế thực nghiệm**, không khẳng định tăng hiệu năng khi chưa đo.

---

## 8. EHO — ĐẶC TẢ ĐẦY ĐỦ CHO 3 THÀNH VIÊN (CHƯA CODE TRONG GIAI ĐOẠN ĐẦU)

### 8.1 Ràng buộc nền tảng

**EHO nguyên bản được định nghĩa cho vector liên tục**, với phép toán cập nhật vị trí, tâm đàn và tách đàn. TSP lại là bài toán **hoán vị rời rạc**. Vì thế **KHÔNG** được dùng trực tiếp phép cộng/trừ vector thực lên route, cast sang int rồi gọi đó là EHO chuẩn. Phiên bản nhóm xây dựng phải gọi đúng là **Discrete Elephant Herding Optimization (D-EHO) adapted for TSP**, và báo cáo rõ phần **giữ từ EHO gốc** và phần **thiết kế ánh xạ mới**.

Nguồn nền: *Swarm Intelligence Algorithms: A Tutorial* (ed. Adam Slowik), Chương 12 **Elephant Herding Optimization**, gồm clan updating, separation, pseudocode và ví dụ tính từng bước. Đọc **trực tiếp chương này** khi đến giai đoạn EHO, không chỉ tóm tắt từ blog.

### 8.2 Các thành phần bắt buộc của EHO

1. **Population = elephants:** mỗi voi là một tour TSP hợp lệ.
2. **Clans:** chia tổng quần thể thành `clan_count` đàn, mỗi đàn có `elephants_per_clan` cá thể; tổng `population_size = clan_count × elephants_per_clan`.
3. **Matriarch:** voi có tour length tốt nhất trong đàn hiện tại, hoặc global best của đàn được lưu theo chính sách thống nhất. Đặc tả mặc định: tốt nhất trong đàn hiện tại; giữ `global_best` riêng toàn bộ run.
4. **Clan updating operator:** tác động hướng các voi về tour leader dưới phép biến đổi hợp lệ trên permutation; độ mạnh điều khiển bởi `alpha` và số ngẫu nhiên `r`.
5. **Matriarch updating operator:** EHO gốc dùng tâm trung bình (continuous centroid), nhưng centroid của các route không phải permutation. Với D-EHO, dùng **clan medoid** hoặc đại diện hợp lệ khác có định nghĩa toán học rõ; beta điều tiết mức dịch chuyển của matriarch/leader về đại diện đàn. Đây là **lựa chọn thiết kế rời rạc**, không được mô tả như công thức gốc giữ nguyên từng ký hiệu.
6. **Separation operator:** thay 1 hoặc số cấu hình voi có chi phí tệ nhất mỗi clan bằng tour hợp lệ được tạo ngẫu nhiên/đa dạng; tái lập được theo seed; số lượng voi trong mỗi clan không đổi.
7. Đánh giá fitness, lưu `global_best`, `history`, `evaluations`, stop criteria và trả `RunResult` **giống GA**.
8. Mỗi toán tử EHO được kiểm thử độc lập, giải thích trong báo cáo và slide.

### 8.3 Phương án chuyển đổi rời rạc ĐƯỢC CHỌN CHO BASELINE

**Phép biểu diễn:** route với city `0` cố định; chỉ biến đổi đoạn `route[1:]` bằng các hoán đổi/chèn/đảo đoạn có chủ đích.

**Khoảng cách giữa hai cá thể:** `HammingDistance(a,b)` trên đoạn city `1..n-1` hoặc số phép swap cần để khớp permutation. Baseline chọn **số vị trí khác nhau (Hamming)**, dùng đồng nhất cho medoid và thống kê hướng di chuyển; đây là *khoảng cách giữa các nghiệm*, **khác với tour length**.

**Guided clan update:**

- Với voi `x` và matriarch `m`, tạo danh sách các vị trí `i >= 1` đang có `x[i] != m[i]`.
- Đặt số bước `k = floor(alpha × r × HammingDistance(x,m))` (bounded, có thể `0`), với `r` lấy từ RNG của run.
- Lặp tối đa `k` lần: chọn một vị trí sai khác, tìm vị trí của thành phố mục tiêu `m[i]` trong `x`, swap hai vị trí (không chạm vị trí `0`). Mỗi swap làm khớp thêm ít nhất vị trí được chọn, vẫn là permutation hợp lệ.
- Không lẫn operator crossover/selection của GA vào EHO. Nếu có bổ sung nhiễu ngẫu nhiên phải đánh dấu variant riêng, giải thích và đo ablation.

**Matriarch update (rời rạc):**

- Xác định **medoid của clan**: cá thể có tổng Hamming distance tới các thành viên clan là nhỏ nhất; khi hòa, dùng quy tắc tie-break ổn định (tour cost rồi thứ tự index).
- Biến đổi matriarch về medoid bằng guided swaps với hệ số `beta` và RNG; nếu trùng nhau thì giữ nguyên. Không tính trung bình số học trên mã city.
- Chính sách lưu `global_best` đảm bảo không mất nghiệm tốt nhất từng tìm thấy, dù leader hiện tại bị thay đổi.
- Nếu muốn thay thiết kế medoid bằng cơ chế literature khác, phải làm mini-proposal mô tả sự khác biệt so với EHO gốc, test và được leader chấp thuận **trước khi sửa baseline**.

**Separation:**

- Sau cập nhật/đánh giá clan, tìm `separation_count_per_clan` cá thể có chi phí tệ nhất ở từng clan, ưu tiên không xóa thông tin `global_best` trong archive.
- Thay bằng permutation ngẫu nhiên mới với RNG của run. Nếu muốn tránh trùng cá thể, giới hạn số lần thử và chấp nhận trùng khi không thể tránh; không treo vô hạn.
- Giữ nguyên kích thước mỗi clan. Sau khi thay, đánh giá đúng số objective calls và cập nhật thống kê.

**Một iteration EHO đề xuất:**

```text
Khởi tạo clan/population → fitness → global_best/history(0)
For iteration = 1..max_iterations:
    Với mỗi clan:
        xác định matriarch (tốt nhất hiện tại)
        xác định medoid hợp lệ
        tạo next_clan qua guided update cho các voi không phải leader
        cập nhật leader hướng tới medoid theo beta (quy tắc đã đóng băng)
        đánh giá next_clan
        thực hiện separation: thay các voi tệ nhất bằng tour ngẫu nhiên
        đánh giá voi mới
    cập nhật global_best; ghi stats; kiểm tra stop criteria
Trả RunResult với route tốt nhất lịch sử
```

**Chú ý học thuật:** Thuật toán trên là **phương án D-EHO do nhóm thiết kế** để làm TSP; phải đưa công thức EHO liên tục gốc rồi biện luận phép biến đổi này. Không khẳng định nó là phiên bản chuẩn được công bố hay chắc chắn tốt hơn GA. Ưu tiên tính đúng, giải thích được và reproducibility.

### 8.4 Preset EHO dự kiến

| Parameter | Default đề xuất | Điều kiện |
|---|---:|---|
| `clan_count` | 4 | >= 2 |
| `elephants_per_clan` | 20 | >= 3 |
| total `population_size` | 80 | cùng population với GA trong baseline |
| `iterations` | 250 | >= 1; benchmark điều chỉnh để cân bằng evaluations |
| `alpha` | 0.7 | `[0,1]` |
| `beta` | 0.3 | `[0,1]` |
| `separation_count_per_clan` | 1 | `1..clan_size-1` |
| `initialization_method` | `random` | giống GA baseline |
| `preserve_global_best` | `True` | best archive, không sửa result |
| `seed` | 42 | explicit |

Các preset chỉ là khởi đầu; số objective evaluations thực tế của EHO có thể khác GA vì separation/leader update. **Đừng tuyên bố công bằng chỉ vì cùng số iteration hoặc population**: cần ràng buộc/ghi nhận `max_evaluations` nếu làm benchmark budget-matched.

### 8.5 Tiêu chí nghiệm thu EHO

- Có clan, matriarch, discrete clan update, discrete medoid update, separation; không phải một random search đổi tên.
- Tất cả tour hợp lệ sau mọi operator, dữ liệu không bị mutation ngoài ý muốn.
- `alpha=0` không ép guided movement; `beta=0` không ép leader update; separation vẫn điều khiển bằng config. Có test cho các biên này.
- Quần thể không đổi kích thước, cả khi worst = best hoặc có tie.
- `best_so_far` monotonic, cùng seed tái lập; dừng sớm/hủy giữa iteration có kết quả nhất quán.
- Giao diện và benchmark chỉ dùng common contract, không đọc biến riêng trong solver.
- Có file `docs/algorithm_eho.md` phân biệt **EHO công thức gốc** với **phép ánh xạ rời rạc do nhóm thiết kế**.

---

## 9. KIỂM SOÁT PHÉP SO SÁNH VÀ PHƯƠNG PHÁP THỰC NGHIỆM

### 9.1 Câu hỏi thực nghiệm

- GA và D-EHO tìm tour tốt đến đâu trên cùng TSP instance?
- GA thay đổi như thế nào khi thay `selection_method`, `crossover_method`, `mutation_method`, `mutation_rate`, `population_size`, `elite_count`?
- D-EHO thay đổi thế nào khi thay `alpha`, `beta`, `clan_count`, `separation_count_per_clan`?
- Kết quả hội tụ, tính ổn định giữa các random seed, thời gian thực thi và số lần tính objective khác nhau ra sao?
- Quy mô số thành phố ảnh hưởng đến hiệu quả và runtime thế nào?

### 9.2 Dataset plan

**P0:** 7 ma trận `data/legacy/` (3, 4, 6, 15, 26, 42, 48 thành phố). Chọn test nhanh 3–6, test trung bình 15–26, benchmark thực tế 42–48.

**P1:** TSPLIB95 chính thống, ưu tiên subset vừa sức như `burma14`, `eil51`, `berlin52`, `kroA100` (không nhất thiết đủ cả bốn). Sử dụng thư viện `tsplib95` hoặc loader tương đương có test; **bảo toàn chính xác `EDGE_WEIGHT_TYPE`** (`EUC_2D`, `ATT`, `GEO`, `EXPLICIT`...), không dùng Euclidean thô cho mọi instance. Ghi nguồn và `known_optimum` đã xác minh; có thể bắt đầu từ `eil51`/`berlin52` để đơn giản.

**Nguồn:** https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/

### 9.3 Benchmark chuẩn bắt buộc

- Cùng dataset, cùng objective, cùng version, cùng máy/môi trường, cùng tập seed và quy tắc dừng rõ ràng.
- **Mặc định các kết quả chính dùng random initialization, không local search ở cả hai**, để không thiên vị.
- Ghi số objective evaluations thực tế và runtime; với đối chiếu chính ưu tiên **ngân sách evaluations tương đương**, nếu không thể đúng tuyệt đối phải nêu chênh lệch. Có thể thêm benchmark fixed-time riêng nhưng không đánh đồng hai loại ngân sách.
- Tối thiểu **5 seed độc lập** (đề xuất `[11, 23, 37, 53, 71]`) cho mỗi tổ hợp chính; 10 seed nếu ngân sách thời gian đủ. Không chỉ chạy một lần rồi chọn run tốt nhất.
- Mỗi run có `run_id`, `dataset`, `seed`, thuật toán, config, objective evaluations, runtime solver-only, best distance, validation, version/commit nếu lấy được.
- Tổng hợp `mean`, `std`, `median`, `min`, `max` của best distance và runtime; `relative gap` khi có known optimum. Giải thích rằng nghiệm metaheuristic có phương sai do tính ngẫu nhiên.
- Biểu đồ convergence có trục X ghi rõ: **iteration** hoặc **cumulative objective evaluations**; ưu tiên đường `best_so_far` theo evaluations trong so sánh liên thuật toán.
- Nếu vẽ mean convergence nhiều seed, cần đồng bộ mốc evaluation và chỉ ghi điểm mà dữ liệu hỗ trợ (không tạo đường giả bằng interpolation không giải thích).
- Không tính thời gian đọc file, khởi tạo UI, xuất PNG/CSV, matplotlib rendering vào solver runtime trừ khi báo cáo riêng.

### 9.4 Xuất kết quả

- File raw results: CSV mỗi hàng một run, có đầy đủ config/seed/dataset/metrics; số và đơn vị chính xác.
- Structured run JSON: route/params/history/evaluation-count/stopping-reason/elapsed.
- Summary CSV/Markdown và chart PNG do script tạo từ raw results, không chỉnh bằng tay để tăng điểm.
- Cả hai thuật toán phải qua validation route độc lập khi benchmark ghi nhận.
- Log thất bại/timeouts có trạng thái rõ; không xóa những run thất bại khỏi thống kê mà không giải thích.

### 9.5 Đánh giá cải tiến GA legacy

Có thể chạy bản GA cũ như **baseline nội bộ** để cho thấy sự khác biệt về độ đúng, tính ổn định và hiệu năng; tuyệt đối không sửa bản cũ để "tăng điểm" trước khi thu baseline. Nếu legacy không chạy chuẩn thì trình bày lỗi và dùng comparison theo operator/budget trên bản GA mới thay vì bịa đồ thị before/after.

---

## 10. GUI FORM — BẢN FINAL SAU KHI HAI SOLVER ỔN ĐỊNH

**Framework đã chọn: Tkinter + ttk + Matplotlib (embedded canvas).** Lý do: có sẵn từ legacy, nhẹ, đủ form/biểu đồ, khả thi trong 8 tuần; chất lượng GUI chấm bằng khả năng sử dụng thật, không phải chỉ bằng số widget.

### 10.1 Cấu trúc màn hình gợi ý

**Một cửa sổ chính** chia bốn khu vực rõ ràng, không tạo 10 cửa sổ con:

1. **Dataset panel:** chọn file có sẵn, duyệt file `.txt`/`.tsp` được hỗ trợ, hiển thị tên, số city, dạng dữ liệu, source, known optimum (nếu được xác minh), cảnh báo khi dữ liệu lỗi.
2. **Algorithm & parameters:** chọn `GA` hoặc `EHO`, hiển thị form đúng cho thuật toán tương ứng; preset `Quick demo / Standard / Benchmark`, seed, budget. Form GA có selection/crossover/mutation/elitism; form EHO có clans/alpha/beta/separation.
3. **Execution/status:** `Run`, `Stop` (cooperative), progress bar, elapsed time, evaluations, current best, best so far, thông báo lỗi và trạng thái hoàn tất. Không cho người dùng tạo hai job xung đột cùng lúc trừ khi có queue rõ ràng.
4. **Visualization & results:** hai tab `Tour` / `Convergence` và tab `Comparison` (nếu đã chạy hai thuật toán trên cùng dataset). Tô tuyến hợp lệ và đóng vòng, danh sách route dạng 1-based ở UI, chi phí và metadata; xuất PNG/CSV/JSON.

### 10.2 Chi tiết hiển thị

- Dataset có tọa độ thật: vẽ điểm theo `coordinates`; không có tọa độ: vẽ circular layout và gắn nhãn **"sơ đồ minh họa, không phải vị trí địa lý"**.
- Người dùng có thể xem đường đi trước/sau chạy, route text, fitness history.
- Khi thay dữ liệu trong khi job đang chạy, không làm hỏng kết quả của job cũ; khóa input hoặc snapshot input.
- Worker không trực tiếp gọi thao tác Tkinter, GUI nhận event qua thread-safe queue / `after`.
- Giao diện không tự reset lựa chọn tham số ngoài ý muốn; validate gần nơi nhập.
- Không hiển thị thành tích "optimum" nếu chỉ là best tìm được.
- Mặc định tiếng Việt cho labels/hướng dẫn/ lỗi; tên thuật toán và tên tham số kỹ thuật có thể giữ English.

### 10.3 P2, không bắt buộc

Dark/light theme, hướng dẫn tooltip, phóng to đồ thị, export báo cáo HTML, animation tiến trình có giảm tần suất cập nhật. **Không** ưu tiên P2 trước test/dataset/benchmark.

---

## 11. THIẾT KẾ CLI, KHẢ NĂNG CHẠY THỬ VÀ LỆNH ĐÍCH

Chọn cách cài đặt hỗ trợ `pip install -e .` trong virtual environment. Sau khi code được triển khai, cần có các lệnh tương đương:

```bash
python -m ga_eho_tsp.cli validate --dataset data/legacy/06Cities-1248.txt
python -m ga_eho_tsp.cli solve --algorithm ga --dataset data/legacy/15Cities-1194.txt --seed 42
python -m ga_eho_tsp.cli solve --algorithm eho --dataset data/legacy/15Cities-1194.txt --seed 42
python -m ga_eho_tsp.cli benchmark --config experiments/configs/baseline.json
python -m ga_eho_tsp.gui
python -m pytest -q
```

**Chú ý:** Đây là **hợp đồng lệnh đầu ra sau khi hoàn thành**, không có nghĩa các lệnh đã chạy được tại thời điểm viết `final.md`. Nếu CLI thiết kế argparse có flag khác cần giữ cú pháp trên bằng alias hoặc sửa tài liệu theo quy trình change control. Không chạy benchmark EHO trước khi EHO được triển khai.

`Demo.py` cũ: nếu giữ, chỉ được là wrapper gọi `ga_eho_tsp.gui`, không chứa một bản thuật toán thứ hai. Các file root `benchmark_all.py`, `visualize_run.py` tương tự: xác định đang có chức năng gì, sau đó làm wrapper hoặc di chuyển hợp lý, tránh copy-paste logic.

---

## 12. KIỂM THỬ VÀ TIÊU CHÍ CHẤT LƯỢNG BẮT BUỘC

### 12.1 Unit tests TSP/domain

- Ma trận 3 city tự đặt biết trước optimum, tính đúng cạnh cuối → đầu.
- Route đúng/thiếu city/trùng city/sai start/wrong type.
- Ma trận không vuông, lệch đối xứng, âm/NaN/inf, không zero diagonal.
- Dataset legacy đủ 7 file được đọc đúng kích thước và số lượng.
- Cùng một route với thứ tự đảo chiều có cùng chi phí trong symmetric TSP.
- Input không bị thay đổi khi tính objective/validate.

### 12.2 Unit tests GA

- Selection không lỗi nếu mọi điểm fitness bằng nhau, `tournament_size` biên, roulette tổng trọng số 0.
- Crossover luôn trả con hợp lệ, giữ `0`, không sửa bố mẹ; test nhiều seed và n.
- Mutation luôn trả route hợp lệ, tôn trọng `mutation_rate=0/1`, và không phụ thuộc random global.
- Elitism thật sự giữ elite; không gán bừa fitness; có test cụ thể lỗi chọn lặp trước đây.
- `best_so_far` không tăng; output distance match objective; history/evaluations nhất quán.
- Cùng seed reproducible; thay seed có thể ra kết quả khác nhưng không được bắt buộc khác.
- Xử lý `population_size` nhỏ và cấu hình odd (hoặc reject documented).
- Cancel/time limit trả trạng thái thật; không ghi solved-complete nếu đã hủy.

### 12.3 Unit tests EHO

- Clan count và clan size được duy trì qua mọi iteration.
- Guided swaps không chạm city 0, không thiếu/trùng city và có hướng về matriarch theo thiết kế.
- Medoid xác định được khi tie; `beta=0` bất biến leader; `alpha=0` không thực hiện guided steps.
- Separation thay cá thể yếu đúng số lượng, route hợp lệ; tính đa dạng có thể kiểm soát.
- Cùng seed deterministic, best history monotonic, objective same as GA.
- No-op/small n/tie fitness không gây lỗi hoặc vòng lặp vô hạn.

### 12.4 Integration tests

- Load → solve GA/EHO → validate → export → import/display.
- CLI `validate`, `solve`, `benchmark` không mở GUI.
- GUI dừng job an toàn, không cập nhật widget sai luồng, không treo UI.
- Cross-algorithm fairness: cùng dataset cùng objective; budgets/evaluations ghi đúng.
- Chạy được trên Windows là môi trường demo ưu tiên; README ghi rõ terminal/virtualenv.

### 12.5 Quy tắc nghiệm thu về chất lượng

- **Không báo "100% test passed" nếu chưa chạy.** Trong tổng kết phải in các lệnh đã chạy và kết quả thật.
- Không xóa hoặc bỏ qua failing tests để hoàn tất nhanh.
- `pytest -q` xanh trên phần đã triển khai; type check/lint ưu tiên P1 nhưng lỗi chất lượng nghiêm trọng phải sửa.
- Tối thiểu mọi bug critical có 1 test tái hiện trước hoặc kèm khi fix.
- Không dùng kết quả stochastic để tạo test brittle đòi route bằng một đường cố định nếu không cần thiết; test validity/reproducibility/known optimal ở bài nhỏ.

---

## 13. HIỆU NĂNG VÀ TÍNH ĐÚNG — THỨ TỰ ƯU TIÊN

1. **Correctness:** không có route lỗi, tính objective đúng, best archive đúng.
2. **Reproducibility:** seed, config snapshot, phiên bản library, data checksum.
3. **Measurement:** evaluations, wall-clock compute time, gap với optimum có kiểm chứng, repeated runs.
4. **Algorithmic optimization:** O(1) lookup distances, giảm copy, tối ưu evaluation cache có giải thích, giảm operations không cần thiết; benchmark trước/sau để kết luận.
5. **Advanced heuristics:** 2-opt, adaptive mutation, init hỗn hợp — chỉ khi có điều kiện và báo cáo công bằng.

**Không được:** chỉnh dataset/stop early để làm đẹp điểm số, dùng Numba/Cython/GPU khiến thành viên không giải thích được, dùng library solver GA/EHO có sẵn thay cho tự cài đặt, hard-code lời giải cho file benchmark, hoặc lén thêm thuật toán bên ngoài đề tài.

---

## 14. PHÂN CÔNG 4 THÀNH VIÊN — OWNER RÕ RÀNG

> Chỉ có tên trưởng nhóm **Trương Thành Đạt** được xác nhận. 3 người còn lại tạm ghi **Thành viên EHO 1/2/3** để tránh tự điền sai danh sách. Leader cập nhật tên thật vào `docs/team_plan.md` khi nhóm thống nhất. **Cả ba thành viên đều có nhiệm vụ trọng tâm là EHO**, nhưng phân mảng khác nhau để tránh chồng chéo.

| Người | Chịu trách nhiệm chính (owner) | Deliverable bắt buộc | Reviewer |
|---|---|---|---|
| **Trương Thành Đạt — Leader / GA owner** | Audit GA legacy; core TSP/contract; kiến trúc; toàn bộ GA; benchmark framework phần chung; hợp nhất PR | `domain/*`, `algorithms/ga/*`, test GA, docs GA, API ổn định, tích hợp final | EHO 1 hoặc EHO 2 review logic domain/GA |
| **Thành viên EHO 1 — EHO algorithm owner** | Đọc/giải thích EHO gốc, clan/matriarch, pseudocode, main loop D-EHO | `algorithms/eho/solver.py`, `clans.py`, `docs/algorithm_eho.md` phần lý thuyết | EHO 2 + Leader |
| **Thành viên EHO 2 — EHO operators & correctness owner** | Guided swaps, medoid/beta, separation, validation, unit tests các toán tử; tham số EHO | `discrete_ops.py`, `separation.py`, `tests/eho/*`, phần phép biến đổi rời rạc | EHO 1 + Leader |
| **Thành viên EHO 3 — EHO evaluation & integration owner** | Tập dữ liệu EHO, benchmark EHO, UI form EHO (sau core), kết quả thí nghiệm, hình/bảng EHO | `experiments` configs cho EHO, test integration, màn hình EHO, bảng/đồ thị, báo cáo thực nghiệm | Leader + EHO 1 |

**Cam kết giao tiếp:** Tất cả thành viên hiểu được GA/EHO ở mức giải thích và demo, không chỉ phụ trách phần mình. Người chưa rành API phải đọc hợp đồng mục 5 và docs kiến trúc trước khi làm.

### Quy tắc ownership

- Leader có quyền duyệt thay đổi các file chung `domain/`, `models.py`, `protocols.py`, `experiments/benchmark.py`, `final.md`.
- Thành viên EHO không sửa core GA hoặc TSP objective để thích nghi với EHO; phải yêu cầu change request.
- GA owner không tự viết EHO thay ba thành viên; có thể tạo interface và tích hợp sau khi PR EHO được review.
- Mọi PR liên quan thuật toán phải có test và ghi rõ người viết, nguồn tham khảo, cách tái hiện kết quả.
- Đến cuối kỳ, mỗi người phải có đóng góp kỹ thuật cụ thể, commit có ý nghĩa và phần bảo vệ riêng.

---

## 15. TIẾN ĐỘ 8 TUẦN — THỰC TẾ CHO SINH VIÊN NĂM 3

| Tuần | Leader / GA | EHO 1 | EHO 2 | EHO 3 | Điểm nghiệm thu |
|---|---|---|---|---|---|
| **1** | Audit repo, chạy legacy, chốt core TSP/data/API | Đọc chương EHO, tóm tắt toán học | Nghiên cứu permutation operators và tính khả thi | Kiểm kê dataset, benchmark plan | Audit + test TSP nhỏ + contract được thông qua |
| **2** | Implement GA basic đúng, selection, crossover, mutation | Viết pseudocode EHO gốc và đề xuất chuyển đổi | Thiết kế guided swaps, medoid, test case trên giấy | Thiết kế dataset registry/report schema | GA P0 trên dataset nhỏ, EHO design review (chưa merge code EHO) |
| **3** | GA elitism/global best, logging/history, tests, CLI | Bắt đầu EHO clans/main loop sau khi API GA ổn | Bắt đầu EHO discrete operators + unit tests | Thiết lập EHO benchmark configs và test harness | GA P0 xanh; D-EHO primitive tests xanh |
| **4** | GA profiling/tối ưu an toàn; docs GA; review EHO PR | Hoàn thiện EHO solver | Hoàn thiện separation, reproducibility/test biên | Tích hợp EHO CLI + dữ liệu EHO | GA stable; EHO chạy 3–26 city và trả RunResult |
| **5** | Củng cố domain/CLI/integration, GUI khung chung | Sửa lỗi EHO, chạy nhiều seed | Cải thiện độ đúng và test EHO | GUI form EHO, biểu đồ/benchmark | Cả GA & EHO chạy trên cùng dữ liệu/GUI |
| **6** | Benchmark chính, GA ablations, profiling có đo | Thực nghiệm alpha/clan_count | Thực nghiệm beta/separation, tổng hợp sai số | Charts/export/results + integration tests | Raw CSV/JSON + bảng/biểu đồ chính xác |
| **7** | Viết phần GA/kiến trúc, rà soát code/release | Viết lý thuyết EHO, pseudocode | Viết biến đổi permutation và kiểm thử | Viết phương pháp & kết quả thực nghiệm, hình GUI | Báo cáo nháp hoàn chỉnh + demo không lỗi |
| **8** | Hợp nhất báo cáo, kiểm tra nguồn, Turnitin, demo | Bảo vệ EHO theory | Bảo vệ EHO implementation | Bảo vệ benchmark/GUI | Code freeze, kiểm thử cuối, slide, luyện Q&A |

**Điều chỉnh thực tế:** Tuần 1–2 các thành viên EHO chuẩn bị thiết kế và kiểm thử lý thuyết; **chưa cần đợi leader xong GA mới học EHO**. Phần **code EHO** được mở sau khi interface chung ổn định (dự kiến tuần 3), tránh ba người viết trên API đang thay đổi.

### Milestone / Gate

- **M0 / cuối tuần 1:** Có audit chính xác, dataset loader, objective, API, tests cơ bản.
- **M1 / cuối tuần 3:** GA hoàn chỉnh P0, test xanh; EHO kiến trúc thống nhất, có thể code độc lập.
- **M2 / cuối tuần 4:** GA stable; EHO minimal solver đúng, cùng API.
- **M3 / cuối tuần 6:** GUI và benchmark end-to-end, thí nghiệm đủ dữ liệu.
- **M4 / cuối tuần 8:** Báo cáo chuẩn, có Turnitin, demo, Q&A.

**Nếu trễ:** Ưu tiên P0, giảm số configs ablation và hiệu ứng GUI; không giảm tính đúng hoặc bỏ test.

---

## 16. QUY TẮC GIT/GITHUB CHO NHÓM 4 NGƯỜI

### Branches

- `main`: luôn chạy/kiểm thử được và chứa phiên bản đã được duyệt.
- `feature/ga-core`, `feature/ga-operators`, `feature/ga-benchmark` — leader.
- `feature/eho-core`, `feature/eho-discrete-operators`, `feature/eho-experiments` — 3 thành viên EHO theo ownership.
- `feature/gui-integration`, `docs/report`, `fix/<mo-ta-ngan>` cho tác vụ phối hợp.

### Workflow

1. Mỗi task có GitHub Issue: mục tiêu, owner, phạm vi file, acceptance criteria, deadline theo tuần.
2. Branch từ `main` mới nhất, commit nhỏ, có tiêu đề rõ (`feat(ga): implement permutation-safe OX crossover`, `test(eho): validate clan separation`).
3. Pull Request ghi **what/why/how tested**, ảnh UI nếu có thay đổi giao diện, benchmark số liệu nếu claim hiệu năng.
4. Ít nhất một thành viên khác review; thay đổi core chung cần leader review.
5. Merge sau khi tests của vùng thay đổi xanh; không push trực tiếp lên `main` khi đã mở workflow nhóm.
6. Không commit `.venv/`, `__pycache__/`, binary output lớn, token/secrets, log tạm. Dataset nhỏ, test fixture và config benchmark được commit có chọn lọc.
7. Không force-push để xóa dấu vết kế thừa hay sửa lịch sử đã public; khi di chuyển file ghi nguồn rõ.
8. Đóng milestone bằng checklist và link PR; tránh "xong rồi" không có kiểm thử.

### Definition of Done cho một task

`Code + docs/pseudocode nếu đổi thuật toán + unit test + lệnh tái hiện + review + không phá shared contract`.

---

## 17. DOCUMENTATION & REPORT DELIVERABLES

### 17.1 Tài liệu source-of-truth

- `final.md`: phạm vi cố định và master prompt.
- `docs/audit_legacy.md`: bảng mapping code gốc → code mới, lỗi xác thực, ảnh hưởng và quyết định giữ/viết lại.
- `docs/architecture.md`: mô-đun, luồng dữ liệu, coupling, sơ đồ module; cách chạy GUI và CLI.
- `docs/algorithm_ga.md`: mô hình chromosomes, population, fitness, selection, crossover, mutation, elitism, stopping, pseudocode, độ phức tạp gần đúng.
- `docs/algorithm_eho.md`: EHO nguyên bản vs D-EHO cho permutation, công thức/giả thiết, clan/separation, pseudocode, minh họa chuyển đổi một tour.
- `docs/experiments.md`: dataset, seed, config, môi trường, đo thời gian/evaluations, bảng số liệu thực, ý nghĩa/giới hạn.
- `docs/team_plan.md`: người thật, task, PR, milestone, phụ trách phần báo cáo.
- `docs/references.md`: khoa học + nguồn mã gốc + nguồn dataset, format citations.
- `docs/changelog_decisions.md`: nếu có đề xuất rời baseline, ghi ADR (decision, alternatives, impact, approver).

### 17.2 Dàn ý báo cáo đề xuất (phải theo mẫu giảng viên nếu có)

1. Tổng quan TSP, mục tiêu, phạm vi, đóng góp nhóm và nguồn tham khảo.
2. Nền tảng toán học TSP; GA; EHO gốc; trở ngại continuous→permutation.
3. Thiết kế chung: dữ liệu, ma trận khoảng cách, representation, fitness, module/API.
4. Cài đặt GA và các biến thể, mô tả cách cài đặt lại/khắc phục hạn chế legacy.
5. Cài đặt D-EHO, phép rời rạc hóa, clan/matriarch/separation.
6. Giao diện, luồng thao tác, kiểm thử chức năng.
7. Phương pháp thực nghiệm, dataset, tham số, kết quả nhiều seed, hội tụ và hiệu năng.
8. Nhận xét, limitations, hướng phát triển có kiểm soát, kết luận.
9. Phân công/đóng góp; tài liệu tham khảo; phụ lục lệnh chạy và số liệu; báo cáo Turnitin theo yêu cầu.

### 17.3 Yêu cầu trung thực

- Không tự sinh số liệu/ảnh màn hình chưa chạy.
- Không cố tình paraphrase để che giấu nguồn.
- Không trình bày D-EHO adaptation như công thức nguyên bản đã công bố.
- Không dùng tên `GA+EHO hybrid` khi hệ thống chỉ có hai solver độc lập.
- Phân tích đúng: nghiệm tốt nhất, độ ổn định, thời gian và đánh đổi; nêu trường hợp thuật toán kém.

---

## 18. CÁC TÌNH HUỐNG BIÊN BẮT BUỘC DEMO ĐƯỢC

1. TSP 3 city dễ kiểm chứng bằng tay; cả GA và EHO trả route đúng và có đánh dấu đóng vòng.
2. Ma trận 4–6 city có known best nhỏ, kiểm tra nhanh kết quả hợp lệ.
3. Dataset 15/26/42/48 city: thời gian hợp lý, GUI không đơ; output không tràn màn hình.
4. Dataset sai số dòng/cột, số âm, NaN, thiếu file: báo lỗi dễ hiểu.
5. Tham số vô lý: mutation negative, `elite_count >= population`, `clan_count` quá lớn, `alpha/beta` ngoài `[0,1]`.
6. Dừng giữa chừng: trả best đã tìm được và trạng thái `CANCELLED`/`STOPPED`, không giả là chạy xong.
7. Seed cố định: thử chạy lại và so nghiệm/history; ghi rõ CPU/time runtime có thể khác nhẹ.
8. Cùng dataset chạy lần lượt GA rồi EHO: xem route, length, convergence, thống kê.
9. Xuất kết quả, đọc lại JSON/CSV và kiểm tra độ chính xác dữ liệu.
10. Không có coordinates: GUI ghi rõ hình tròn chỉ là minh họa topology.

---

## 19. QUALITY GATES/ACCEPTANCE CHECKLIST KHI ĐỒ ÁN HOÀN THÀNH

### P0 — không được thiếu

- [ ] Đề tài đúng số **6** theo ma trận GA × TSP; tên đề tài đúng và có EHO.
- [ ] GA và EHO cùng giải **symmetric TSP** trên một `TSPProblem`/distance function.
- [ ] Code solver chính thức được nhóm tự cài đặt, hiểu, test, ghi nhận nguồn legacy.
- [ ] 7 legacy datasets được load/validate; có dataset benchmark minh bạch.
- [ ] GA có selection, OX crossover, mutation, survivor elitism, seed, global best.
- [ ] EHO có nhiều clan, matriarch, discrete update, medoid, separation, seed, global best.
- [ ] Mọi route luôn hợp lệ và chi phí tự tính lại khớp kết quả.
- [ ] GUI form chạy được, không đơ, có tour/convergence/parameter controls.
- [ ] Benchmark nhiều seeds, có CSV/JSON raw, bảng summary và các kết luận dựa trên số thật.
- [ ] Unit/integration tests quan trọng xanh; README cài/chạy rõ trên máy mới.
- [ ] Có báo cáo, trích dẫn nguồn, tài liệu tham khảo và kiểm tra Turnitin theo yêu cầu.
- [ ] Thành viên nào cũng giải thích được phần mình và luồng chung.

### P1 — tăng chiều sâu học thuật

- [ ] GA có ít nhất 2 selection methods và ít nhất 2 mutation operators được thử nghiệm.
- [ ] Có ablation nhỏ với GA mutation/selection và D-EHO alpha/beta/separation.
- [ ] Có đối chiếu theo evaluations (hoặc lý giải rõ khác biệt ngân sách) và runtime.
- [ ] Có mốc optimum được kiểm chứng từ TSPLIB để báo gap.
- [ ] Có error handling, stop button và file export đầy đủ.

### Những điều không được đánh đồng

- "Code chạy" ≠ "thuật toán đúng".
- "Kết quả có vẻ ngắn" ≠ "tối ưu toàn cục".
- "Cùng 250 vòng" ≠ "cùng ngân sách tính toán".
- "Cải tiến" ≠ "nhanh hơn" nếu không có trước/sau đo thực tế.
- "Repo public" ≠ "được phép sao chép không giới hạn".

---

## 20. DANH SÁCH TÀI LIỆU KỸ THUẬT & NGHIÊN CỨU ƯU TIÊN

**Nguồn giảng viên / seminar (do nhóm cung cấp):**

1. `DANH SÁCH ĐỀ TÀI - Trí tuệ nhân tạo.pdf`: số 6 trong ma trận GA × TSP; phải bổ sung thuật toán seminar; cài đặt lại; GUI; đánh giá và Turnitin.
2. *Swarm Intelligence Algorithms: A Tutorial*, Adam Slowik (ed.), Chương 12 — Elephant Herding Optimization: clan updating, separation, công thức gốc, pseudocode, code minh họa.

**Nguồn tham khảo kỹ thuật và dữ liệu:**

3. Legacy code: https://github.com/ThienNguyen3001/Travelling-Salesman-Genetic-AI-Final
4. TSPLIB95 official: https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/
5. TSPLIB95 file format: https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf
6. `tsplib95` Python docs (nếu dùng): https://tsplib95.readthedocs.io/en/latest/
7. Python GUI comparison (giảng viên gợi ý): https://www.pythonguis.com/faq/which-python-gui-library/
8. Tài liệu nghiên cứu thêm về GA/TSP, EHO/TSP chỉ đưa vào nếu thành viên **đã đọc và kiểm chứng**; không tự bịa tiêu đề/DOI hoặc mô tả rằng phép chuyển D-EHO của nhóm là nguyên văn paper.

---

## 21. PROMPT THỰC THI CHÍNH THỨC — DÁN CHO AI CODING AGENT

> **Chạy mục này tại repository `ga-eho-tsp/`. Đây là lời giao việc, không phải đoạn để AI viết một bài phân tích chung.**

### 21.1 Vai trò và ngữ cảnh

Tôi là **Trương Thành Đạt**, leader của nhóm 4 sinh viên năm 3, phụ trách **100% triển khai GA**, còn ba thành viên khác phụ trách **EHO**. Đồ án trong 8 tuần có tên **"Đề tài 6: Ứng dụng thuật toán Genetic Algorithm và Elephant Herding Optimization cho bài toán người du lịch (Traveling Salesman Problem - TSP)"**.

Tôi đã đưa code GA của đàn anh vào workspace dự án mới `ga-eho-tsp`. Bạn phải xem repository đang mở là nguồn code thật; đọc kỹ `final.md` từ đầu đến cuối. Đây là **frozen specification**: tuyệt đối không tự thu hẹp/tự mở rộng phạm vi, đổi kiến trúc, đổi TSP representation, đổi tên đề tài, gộp EHO vào GA hoặc bỏ yêu cầu test/benchmark.

**Mục tiêu LẦN CHẠY NÀY:** Audit lại mọi phần liên quan GA trong repo hiện tại, hoàn thiện TSP core/shared interfaces và **bắt đầu + hoàn tất GA P0 với kiểm thử** trong phạm vi có thể thực thi ngay. Thiết kế sẵn contract EHO để sau này ba người còn lại làm độc lập, **nhưng KHÔNG code D-EHO trong lần chạy này**.

### 21.2 Bước A — Quét thực chứng toàn bộ repository

1. Liệt kê cấu trúc cây thật (loại `.venv`, cache, output lớn) và phân loại file: legacy, current app, data, experiment, test, docs, unknown.
2. Đọc kỹ mọi file Python đang ảnh hưởng GA, đặc biệt `src/GA.py`, `src/TSP.py`, `Demo.py`, `benchmark_all.py`, `visualize_run.py`; đọc cấu trúc và logic các notebook `Experiment/`; đọc README, .gitignore, danh sách dependency; đối chiếu với `final.md`.
3. Xác định chính xác cách nhập ma trận, route representation, fitness, selection, crossover, mutation, best route, generation, stopping, visualization, CLI, benchmark và import package của bản hiện tại.
4. Dựng call graph hoặc bảng `entry point → function → input/output → phụ thuộc → nguy cơ`.
5. Chạy những lệnh baseline có thể chạy trong môi trường. Nếu có nguy cơ GUI headless không chạy thì dùng smoke test headless, không giả lập log.
6. Audit bug theo mức `CRITICAL/HIGH/MEDIUM/LOW`, dẫn file/function/dòng và input tái hiện; ưu tiên kiểm tra 12 vấn đề mục 3.1, **không rập khuôn** nếu code hiện tại đã khác.
7. Kiểm tra 7 ma trận dataset (dimension, symmetry, diagonal, finite, sample route cost). Kiểm tra xuất xứ/giấy phép tài liệu dùng lại.
8. Ghi kết quả vào `docs/audit_legacy.md`, trong đó có bảng `legacy function → proposed new module → decision (reuse idea / rewrite / remove / archive) → rationale`, ghi chính xác những gì chưa thể kiểm tra.

### 21.3 Bước B — Chốt kiến trúc kỹ thuật trước khi code

1. Đối chiếu kiến trúc mục 6 với repo. Chỉ tạo đúng các module cần cho **domain + GA** và các interface chung; `eho/` chỉ tạo khi bắt đầu giai đoạn EHO, không tạo solver EHO giả.
2. Chuẩn hóa package `src/ga_eho_tsp`, dữ liệu core 0-based, fixed start `0`, route không khép vòng; chỉ GUI/CLI format đường khép vòng.
3. Thiết kế `TSPProblem`, `GAConfig`, `EHOConfig` (schema chuẩn cho EHO chưa triển khai), `RunResult`, `IterationStat`, validation, RNG, stop/progress contract. Đảm bảo hợp đồng có thể dùng được cho cả EHO mà không import EHO.
4. Quy định owner của `domain` là leader; người EHO muốn sửa hợp đồng phải đề xuất.
5. `docs/architecture.md` mô tả luồng dữ liệu và sơ đồ module. Nếu có quyết định thay đổi so với `final.md`, **đề xuất và dừng thay đổi đó**, không tự viết đè baseline.

### 21.4 Bước C — Thực thi GA P0

1. Giữ bản legacy an toàn và rõ nguồn. Viết lại các thuật toán GA cần nộp theo cấu trúc `algorithms/ga/*`, dựa trên kiến thức/thiết kế đã phân tích chứ không bê nguyên nội dung không kiểm chứng.
2. Implement domain `route_length`, permutation validator, matrix loader, registry, test dataset.
3. Implement GA đúng pipeline mục 7: `random initialization`, tournament selection, OX crossover, inversion mutation, elitism, global-best tracking, seed, history, validations, evaluation count, callback, stop criteria.
4. Sau default path, bổ sung thêm `rank/roulette` và `swap/insertion/scramble` nếu không làm chậm nghiệm thu; đảm bảo mỗi operator có test. PMX là P1, không được hy sinh default GA để chạy theo feature count.
5. Phân tách selection / crossover / mutation / survivor; mỗi hàm rõ input/output/side effects; deterministic RNG injection, không mutate parent in place.
6. Tạo `python -m ga_eho_tsp.cli validate` và `solve --algorithm ga`, thông điệp lỗi tiếng Việt dễ hiểu, kết quả hiển thị distance, tour, seed, iterations, evaluations, runtime.
7. Tạo unit/integration tests đặc biệt cho các bug cũ đã phát hiện. Chạy `pytest -q`, các smoke test 3/4/6/15/26 và ít nhất một dataset 42/48 city nếu môi trường cho phép.
8. Tạo báo cáo test/runtime thật; nếu chưa nhanh, profile và đề xuất tối ưu có số liệu, đừng tự tuyên bố "đã tối ưu" chỉ vì đổi list thành NumPy.
9. Viết `docs/algorithm_ga.md`, cập nhật README với lệnh cài/chạy GA hiện có, trạng thái EHO là **planned / not implemented** (không tạo cảm giác EHO đã hoàn tất).
10. Không tự sửa `final.md` hoặc ép EHO chạy bằng dữ liệu giả.

### 21.5 Bước D — Hoàn tất giai đoạn GA, bàn giao cho nhóm EHO

Trước khi kết thúc lần làm việc này, bạn **phải** trả lời bằng báo cáo tiếng Việt ngắn gọn nhưng đủ bằng chứng:

- Đã đọc/kiểm tra những file nào và phát hiện chính xác những lỗi/điểm yếu gì?
- Những file đã tạo/sửa/di chuyển/giữ nguyên, và lý do.
- GA hiện hỗ trợ những chức năng/toán tử nào (P0/P1), chức năng nào chưa có.
- Tests và lệnh đã **thực sự chạy**, pass/fail/skip và giới hạn; không bịa thời gian/tốc độ.
- Một ví dụ lệnh GA và kết quả có thật trên dataset.
- API/contract GA–EHO đã sẵn sàng để 3 thành viên EHO code chưa? Điểm nào cần leader quyết định?
- Các issue còn tồn đọng, thứ tự ưu tiên và PR/task tiếp theo.

**DỪNG Ở ĐÂY.** Không đi vào EHO, GUI lớn, package executable, hybrid algorithm, báo cáo học thuật hoàn chỉnh nếu leader chưa yêu cầu. Nếu thời gian thực thi giới hạn, hoàn thành phần GA quan trọng nhất với test và liệt kê phần còn lại, tuyệt đối không vờ đã làm xong.

### 21.6 Prompt dành riêng cho PHIÊN SAU khi leader bật EHO

**Chỉ sử dụng đoạn này sau khi GA P0 ổn và leader giao nhiệm vụ EHO:**

> Đọc toàn bộ `final.md`, `docs/architecture.md`, `docs/audit_legacy.md`, `docs/algorithm_ga.md`, `docs/team_plan.md` và code thật đang có. Xác nhận contract `TSPProblem/RunResult/solver` ổn định. Từ Mục 8 của `final.md`, triển khai **Discrete Elephant Herding Optimization for TSP** bằng clan updating/leader/medoid/separation, có giải thích sự khác biệt với EHO liên tục của chương 12 trong sách seminar. Tách module `algorithms/eho/*`, dùng RNG riêng, shared objective, output contract giống GA; có tests từng operator, reproducibility, logging và CLI `--algorithm eho`. Không sửa core GA hay objective; nếu cần thay đổi shared contract, đề xuất PR riêng để leader duyệt. Tiếp theo mới tích hợp EHO GUI và chạy benchmark chung theo mục 9; báo cáo bằng số liệu thực, không tuyên bố EHO tốt hơn GA khi chưa chứng minh.

### 21.7 Prompt dành riêng cho PHIÊN TÍCH HỢP CUỐI

**Chỉ sử dụng sau khi cả hai solver pass tests:**

> Đọc `final.md`, kiểm tra đầy đủ code GA/EHO, hợp nhất CLI và GUI Tkinter + ttk + Matplotlib theo Mục 10. Xây dựng khả năng chọn dataset, chọn thuật toán, chỉnh tham số, chạy ở worker không chặn UI, stop, progress, vẽ tour/convergence, so sánh kết quả trên cùng instance và xuất CSV/JSON/PNG. Sau đó chạy benchmark nhiều seed, đo objective evaluations, runtime solver-only, gap khi có optimum xác minh, tổng hợp bảng/biểu đồ; cập nhật `docs/experiments.md`, README và test. Không thêm thuật toán khác, không thay đổi baseline `final.md`, không bịa hiệu năng hay ảnh chạy demo. Dừng với báo cáo nghiệm thu P0/P1 và những rủi ro còn lại.

---

## 22. QUY TRÌNH THAY ĐỔI BASELINE (CHANGE CONTROL)

Nếu phát sinh yêu cầu mới từ giảng viên, thiếu tài liệu, bug kiến trúc hoặc nhóm thống nhất đổi implementation:

1. Tạo GitHub Issue/ADR ghi `vấn đề → phương án A/B → tác động đến GUI/GA/EHO/tests/8 tuần → đề xuất → reviewer`.
2. Leader duyệt thay đổi trước khi sửa shared contract hoặc mục tiêu chính.
3. Cập nhật `docs/changelog_decisions.md`, version baseline và `final.md` trong PR có review. Nếu đổi mã dữ liệu, bắt buộc cập nhật test cả hai solver.
4. Chỉ gọi `FINAL V1.1/V2.0` sau khi nhóm đồng ý; **không sửa âm thầm**.

### Định nghĩa thành công của toàn dự án

**Một dự án có GA tự cài đặt đúng, D-EHO có luận giải rời rạc minh bạch, dùng cùng TSP core, có form ứng dụng, nhiều dataset, số liệu benchmark tái lập được và bốn thành viên hiểu rõ công việc của mình** quan trọng hơn một ứng dụng hào nhoáng nhưng thuật toán không kiểm chứng.

**END OF FROZEN SPECIFICATION — V1.0.**
