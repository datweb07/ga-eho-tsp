# Form GA và nghiệm thu bàn giao — 06/11/2026

Ứng dụng dùng Tkinter + ttk + Matplotlib, gọi trực tiếp GA 0.2.0. EHO chưa triển khai. Đây là bàn giao GA để tích hợp EHO, không phải nghiệm thu toàn bộ đồ án.

## Cài và chạy trên Windows / VS Code

Từ root repository, Python 3.11+:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pip check
python -m ga_eho_tsp.gui
# hoặc
python Demo.py
```

Nếu PowerShell chặn activate, dùng `.\.venv\Scripts\python.exe` thay `python`. Trong VS Code chọn interpreter `.venv`, mở terminal mới rồi chạy lệnh trên. `Demo.py` chỉ gọi cùng `main()` với module launcher, không chứa GA riêng.

Tkinter/ttk thường đi kèm bản Python Windows chính thức; kiểm tra bằng `python -m tkinter`. Nếu thiếu `_tkinter`, bổ sung Tcl/Tk qua bộ cài Python hoặc gói hệ thống tương ứng trên Linux; không `pip install tkinter`. Tk cần desktop/display. CLI và notebook không phụ thuộc Tk. Matplotlib đã có trong requirements, không thêm framework mới.

Module launcher hoạt động từ cwd khác root khi đã cài package. Dataset được tìm từ vị trí package tới `data/` ở repository; nếu cài wheel riêng không có data cạnh package, dùng Duyệt file. Không sửa sys.path và không hardcode đường dẫn máy cá nhân trong app. Chỉ mở cửa sổ không sinh outputs.

## Thao tác

1. Chọn một trong 7 file thật hoặc **Duyệt file .txt**. Định dạng ma trận whitespace, không header: n≥3, vuông, finite, không âm, đối xứng, chéo 0. Loader hiển thị lỗi cụ thể; không hỗ trợ TSPLIB `.tsp`.
2. Giữ thuật toán **Genetic Algorithm (GA)**. EHO hiển thị trạng thái đang phát triển và khóa Run.
3. Chọn preset hoặc sửa form. Hai tab **Cơ bản / Nâng cao** cuộn được; chọn field để đọc giải thích phía dưới. Mọi field lấy default từ `GAConfig()` và được validate bằng schema này. Preset điền lại toàn bộ form để cấu hình cuối luôn nhìn thấy.
4. **Chạy GA** khóa dataset, algorithm, preset và tham số. Tab **Chi tiết** ghi snapshot input thực chạy. Mỗi lần chỉ một worker; không sửa population từ GUI.
5. **Dừng** gửi Event cooperative, chờ result thật và giữ best đã tìm được. Trạng thái hủy là `CANCELLED`; run rất nhanh có thể hoàn tất trước lúc bấm. Đóng khi đang chạy hỏi xác nhận, gửi Stop rồi chỉ destroy Tk sau khi worker đã thoát; chọn Không để tiếp tục.
6. Xem **Tuyến đường**, **Hội tụ**, **Chi tiết**. JSON/CSV/PNG chỉ ghi khi chọn đường dẫn trong dialog; dialog có xác nhận overwrite. Export bị khóa trong lúc chạy. CSV/JSON chứa toàn bộ history, kể cả partial.

| Preset | Khác với schema default |
|---|---|
| Mặc định / Reset default | Không khác: P80, generations250, max_iterations250, seed42 |
| Demo nhanh | P40, generations60, max_iterations60 |
| Giới hạn evaluations | generations2000, max_iterations2000, max_evaluations6000, record_history_every5 |

Default random/tournament3/OX0.9/inversion0.15/elites2. Form hỗ trợ rank/roulette_wheel, PMX, swap/insertion/scramble, NN/mixed, optional stagnation/adaptive và bounded 2-opt. Adaptive và 2-opt OFF mặc định. Bật local search phải đặt moves≥1; tắt cần moves=0, không tự sửa giá trị hộ người dùng. Biến thể được ghi **GA + 2-opt (biến thể thực nghiệm)**, result `algorithm=GA+2-opt`. NN/mixed là heuristic khởi tạo, không phải thuật toán chính thứ ba.

Số thế hệ thực chạy tối đa `min(generations, max_iterations)`; muốn vượt250 cần tăng cả hai. Budget evaluations phải ≥P. Time/Stop chỉ được kiểm tra sau khởi tạo atomic và giữa các candidate/probe, không phải hard real-time.

## Đọc kết quả đúng

- Tour hiển thị **1-based, khép vòng**, city1 được đánh dấu bắt đầu/kết thúc. JSON giữ đúng core tuple/list0-based, bắt đầu0, không lặp city cuối. Chi phí là đơn vị ma trận, không mặc định km.
- Với 7 dataset không có coordinates: **“Sơ đồ minh họa, không phải vị trí địa lý”** luôn hiện trên tuyến và PNG. Không tính cost theo vị trí các điểm trên hình. Khi problem có coordinates, renderer dùng tọa độ đó và đổi ghi chú.
- Hội tụ dùng cumulative evaluations, không dùng index history làm thế hệ. `best_so_far` không tăng; best_current/mean/diversity thuộc quần thể đã commit. Hai snapshot cùng iteration khi partial là hợp lệ. Diversity có thể None với solver khác.
- Progress nhận snapshot thật qua queue, throttle khoảng6.7 event/s. Khi tab Hội tụ đang mở, chart live tối đa khoảng3.3 lần/s, tối đa1000 snapshot gần nhất; chart cuối dùng history đầy đủ. Tab ẩn không render chart liên tục. Chi tiết chỉ hiển thị200 snapshot cuối để gọn; export giữ đầy đủ.
- Trạng thái cuối phân biệt `MAX_ITERATIONS`, `MAX_EVALUATIONS`, `TIME_LIMIT`, `CANCELLED`, `STAGNATION`. Không có phần trăm tiến độ suy đoán.
- Không công bố optimum từ hậu tố tên file. Gap chỉ hiện nếu problem có known_optimum>0 đã xác minh; 7 file hiện không có.

## Audit và sửa trong lượt GUI

Đã đọc toàn bộ `GA_GUI_Final_Handoff_Prompt.md`, `GUIDELINES.md`, tài liệu architecture/algorithm_ga/experiments/README, mọi module Python hiện tại, cấu hình/dependencies/ignore, code và markdown ba notebook. Đã truy luồng CLI/benchmark → load_matrix → GAConfig/solve → RunResult. Trước sửa, Git chỉ có Master Prompt GUI untracked; giữ nguyên file đó. `Demo.py` cũ, GA.py/TSP.py và GUI chưa tồn tại trong working tree; không giả định đã đọc chúng.

Không phát hiện bug GA cần sửa trong các ca kiểm chứng lượt này. Toàn bộ byte domain, algorithms/ga, data và notebook được so SHA256 trước/sau, không đổi. Cần xử lý ở lớp UI: hai iteration caps, sparse/partial history, cooperative stop, không gọi widget từ worker, format tour và circular layout. Đã sửa lỗi phát hiện trong GUI mới khi nghiệm thu: cancel `draw_idle` bằng root làm command Tcl của canvas bị xóa hai lần lúc destroy; đổi sang `canvas.get_tk_widget().after_cancel(...)`, rồi chạy lại toàn bộ smoke thành công. Lượt driver đầu dùng `root.update()` không hoàn tất ở ca dài; thay driver kiểm chứng bằng các nhịp mainloop thật và không tính lượt đó là PASS. Không sửa GA để né lỗi UI.

## Kiểm tra lặp lại

```powershell
python -m pip check
python -m ga_eho_tsp.cli validate --dataset data/06Cities-1248.txt
python -m ga_eho_tsp.cli solve --algorithm ga --dataset data/15Cities-1194.txt --seed 42
python -m ga_eho_tsp.cli solve --algorithm ga --dataset data/48Cities-33523.txt --seed 42 --crossover-method pmx --initialization-method mixed --max-evaluations 6000
python -m ga_eho_tsp.cli benchmark --config examples/ga_benchmark.json
python -m compileall -q src
```

Trong GUI dùng Reset default, chọn15city, Run, lưu JSON. Đối chiếu CLI với **tất cả** field trong config_snapshot, gồm generations/max_iterations/record_history_every; elapsed và thời điểm cancellation không cần khớp. Kiểm tra permutation, tính lại đủ n cạnh từ matrix và history monotonic. Bật tab Hội tụ, thử budget lớn, Stop, run lại, nhập mutation_rate=-1, thử file sai, rồi đóng khi chạy.

Kết quả chi tiết và 10 release gates được ghi trong [gui_verification.md](gui_verification.md). Không viện dẫn166tests cũ như bằng chứng GUI mới. Repo không có pytest suite thường trực; script QA tạm và artifact chạy được lưu ngoài repo. Đây vẫn là rủi ro regression khi team sửa tiếp. Full notebook mode, Linux/macOS và đóng gói wheel/executable chưa nghiệm thu. Notebook executed đang giữ nguyên là snapshot lịch sử trước GUI; câu “GUI chưa triển khai” trong output cũ không mô tả trạng thái code mới.
