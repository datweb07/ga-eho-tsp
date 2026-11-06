# Nghiệm thu GA và ba notebook bàn giao — 06/11/2026

Phạm vi: final cleanup/review GA0.2.0, không thêm thuật toán hoặc đổi shared contract, không triển khai EHO/GUI. Nguồn code là working tree có thay đổi chưa commit trên main, HEAD `e6dfb233a0f5dbe55a17e8b9c8812ee602d63d20`. Tất cả số dưới là kết quả chạy thực; thời gian phụ thuộc máy, không phải cam kết hiệu năng.

## Environment và trước cleanup

Python3.11.9, Windows10 build26300. `python -m pytest -q` trước xóa: **166 passed in1.22s,0failed,0skipped**; log và source suite đã backup ngoài repo. Không dùng việc xóa tests để báo xanh. Snapshot467file đã test ZIP/SHA256, gồm working tree/untracked/config/results và notebook original; vị trí ở [source_attribution.md](source_attribution.md).

Đã chạy166regression tests trước khi xóa tests theo chỉ thị leader, nên repo cuối không còn automated pytest regression suite; việc này là một thay đổi có chủ đích và là rủi ro khi phát triển EHO. GUIDELINES giữ nguyên dù cây đích từng yêu cầu tests; các assertions trong notebook/QA release không thay thế suite regression lâu dài. Team nên thống nhất khôi phục tests khi bắt đầu EHO.

`python -m pip install -r requirements.txt` đã thành công ở `.venv` dự án và một **venv sạch độc lập** ở Temp đường dẫn ngắn. Cả hai `pip check` pass. Phiên bản đã dùng: Matplotlib3.11.2, Notebook7.6.4, ipykernel7.4.0, nbclient0.11.0, nbformat5.11.1. NumPy2.4.6 là dependency của Matplotlib, notebook không import trực tiếp. Venv QA đầu tiên đặt trong đường dẫn quá dài bị OSError khi giải nén JupyterLab; tạo lại tại Temp ngắn đã cài xong và chạy đủ notebook. Run All ban đầu trong sandbox không hoàn tất và đã được dừng; chạy lại với quyền khởi tạo kernel/kết nối local thành công. Bảng dưới chỉ ghi các lần Run All hoàn tất, headless.

## Thiết kế ba notebook mới

Ba notebook tham chiếu gốc37/20/43cells được phục hồi để đọc từ Git và backup, nhưng code/kết luận cũ không được copy sang bản mới. Bản bàn giao dùng public solve/load_matrix/GAConfig/RunResult, không import GA.py/TSP.py hoặc chỉnh sys.path.

| Notebook | Cells/code cells | Nội dung | Quick runs | Figures | Root/.venv Run All(s) | Experiment/venv sạch(s) |
|---|---:|---|---:|---:|---:|---:|
| [Experiment1–2](../Experiment/Experiment%201-2.ipynb) |17/10|Operators OFAT, sensitivity, hội tụ/diversity|80|4|6.742|4.186|
| [Experiment3](../Experiment/Experiment%203.ipynb) |13/8|Phân bố/stability/excess so với best-observed|30|2|3.999|3.814|
| [Experiment4](../Experiment/Experiment%204.ipynb) |13/8|15/26/42/48city, P1/P2, accounting/local-search trade-off|120|3|9.063|9.009|

**3/3 Run All pass ở cả hai cwd/kernel**. Mỗi lượt230runs; hai lượt lặp cùng seeds để kiểm tra portability, không coi là460seed độc lập. Mọi numeric summaries khớp giữa môi trường; thời gian không cần khớp. Notebook hợp lệ nbformat4.5, mọi code cell có execution_count, không output lỗi/traceback, plots được tạo và đã xem trực quan mẫu ở từng notebook. Kích thước bản executed khoảng164/102/127KB, không nhét raw JSON hàng MB. Outputs bảng/ảnh hiện tại là lần Run All bằng `.venv` dự án.

Quick seeds `[11,23,37,53,71]`; Full opt-in25seeds `[101..125]` **chưa chạy nghiệm thu**. Mỗi notebook có run-count cap, tổng solver-time cap120s Quick/600s Full, cooperative per-run cap5s/15s và finite evaluation budgets; không vòng chạy tới target. Tổng cap không phải hard real-time và không bao gồm người dùng ngồi đọc giữa cell. First cell hướng dẫn kernel; tìm root từ cwd/parents, không hard-code đường dẫn cá nhân hoặc os.chdir.

### Notebook1–2: operators và sensitivity

15city,P40,elites2,Quick budget2000. So control với rank/roulette/PMX/swap/insertion/scramble, mỗi lần đổi một yếu tố, không tích3×2×4. Các operator runs đều2000evaluations. Sensitivity thay P20/P80, mutation0.05/0.30, generations10/max_iterations20, elites0/4 và crossover0.60. Với cap thế hệ, actual evaluations thấp hơn được báo rõ; không gọi đó là so sánh fixed-budget công bằng. Base đã đặt generations/max_iterations2000; muốn vượt250 phải tăng cả hai caps.

| Variant | Mean/median cost | Sample std |
|---|---:|---:|
| Control |1235.0/1225|43.86|
| Rank |1413.6/1402|81.79|
| Roulette |1400.8/1340|158.48|
| PMX |1275.4/1279|38.34|
| Swap |1317.0/1289|113.40|
| Insertion |1319.8/1287|68.16|
| Scramble |1473.0/1391|152.78|

PMX không hơn control ở cấu hình này. Notebook có table actual evaluations/runtime, bar mean±sample std, convergence best-so-far theo cumulative evaluations và diversity trên population commit. Đồ thị một seed minh họa dùng seed11 cố định, không chọn run tốt nhất hoặc nội suy mean qua seeds. NN/mixed/adaptive nâng cao ở notebook này chỉ chạy Full; Quick thông báo rõ phần chưa chạy.

### Notebook3: distribution/stability

6datasets3/6/15/26/42/48city,P40,budget4000,5seed/dataset. Histogram không tự thêm bin giả tại0; mỗi panel có thang chi phí riêng. Excess được định nghĩa distance−best_observed; relative excess chỉ khi best_observed>0. Best-observed là min mẫu, không phải optimum của bài lớn.

| n | Min/mean/median/max | Sample std | Tỉ lệ hit min quan sát |
|---|---:|---:|---:|
|3|6/6/6/6|0|100%|
|6|1248/1248/1248/1248|0|100%|
|15|1194/1200.2/1194/1225|13.86|80%|
|26|969/1046/1034/1186|82.85|20%|
|42|1102/1151.6/1133/1211|49.75|20%|
|48|51215/55404.6/55339/59638|3031.79|20%|

Hit-rate không phải xác suất tìm optimum thật; min/hit có thể đổi khi thêm seeds. So sánh std tuyệt đối giữa các thang cost khác nhau không phải một đánh giá uncertainty chuẩn hóa. Notebook kiểm chứng offline n3/n6 bằng2!/5!tail permutations, cost tính trực tiếp từ matrix/cạnh cuối: minima6/1248. Đây chỉ là kiểm chứng nhỏ, không thêm solver thứ ba và không thay registry known_optimum=None.

### Notebook4: challenging cases và kết quả âm

15/26/42/48city,P40,budget4000,5seeds,6variants. Cùng actual evaluations, ghi thêm runtime, committed generations và full local calls. Mean cost:

| n | Control | PMX | Mixed25% | NN | Adaptive | GA+2-opt |
|---|---:|---:|---:|---:|---:|---:|
|15|1200.2|1219.2|1194.0|1194.0|1228.0|1336.2|
|26|1046.0|1054.0|958.6|961.8|1016.4|1388.8|
|42|1151.6|1114.8|811.8|782.2|1112.4|1750.2|
|48|55404.6|55073.2|37222.2|36559.0|53912.2|81489.6|

2-opt **kém control ở cả bốn bài** trong preset này, dù mỗi accepted move cải thiện child. Trên48city, local probes tiêu thụ trung bình3163.4/4000calls, chỉ commit20.6generations so control104. Không coi probes là0work; full objective calls nằm trong total evaluations. NN/mixed tốt hơn trên mẫu này nhưng có thêm initialization work trong runtime. Giữ default random/tournament/OX/inversion để so với EHO sau này; không chọn default chỉ từ một instance/5seed.

Notebook dùng convergence fixed seed11, ma trận chi phí48city và route text đóng vòng để minh họa; không vẽ tọa độ đường phố/GPS. Full thêm adaptive+2-opt nhưng chưa chạy trong phiên Quick.

## QA sau khi xóa tests

Bộ assertions tạm **ngoài repo** đã thực chạy bằng interpreter sạch: **2071checks pass,0fail**. Có OX/PMX/mutation trên3/4/6/15/26/42/48city nhiều seed; selection ties/zero/extreme costs; parent immutable; NN/mixed; odd P; objective sum độc lập; RNG/reproducibility; elitism/global archive khi population cuối xấu đi; two iteration caps; atomic/time/cancel/partial; callback exceptions; exact objective-call counts ở budget9..29, adaptive/2-opt counters và invalid configs. Test riêng cố ý inject lỗi xác nhận benchmark ghi đủ5FAILED, không nuốt failure; không trộn lỗi tiêm vào batch thực nghiệm thật.

CLI validate7/7dataset pass, SHA256 trước/sau không đổi. Default và PMX+mixed+budget trên3/15/48city, mỗi cấu hình chạy2lần: route/cost/evaluations/status/numeric history giống nhau, cost đối chiếu trực tiếp matrix. Mỗi default run19580evaluations/250iterations; mỗi budget variant6000/75full iterations, phần generation sau được ghi partial theo contract.

| n | Default distance | PMX+mixed distance | Seed |
|---|---:|---:|---:|
|3|6|6|42|
|15|1225|1194|42|
|48|38410|36098|42|

Đây là smoke một seed, không kết luận ưu thế tổng quát từ bảng này. RunResult cost/route hợp lệ; history0/final/monotonic và evaluation counts đã được kiểm tra độc lập.

## Benchmark mẫu sau cleanup

Đã chạy `python -m ga_eho_tsp.cli benchmark --config examples/ga_benchmark.json` bằng venv sạch. **35runs=7datasets×5seeds,0failed,tất cả valid**, mỗi run6000evaluations. P80,random/tournament/OX/inversion,elites2,generations/max_iterations2000,record_every5; actual committed generation có thểpartial vì budget. Paths resolve từ examples/, outputs đi vào ignored outputs/ rồi được archive/xóa trước bàn giao.

| n | Mean distance | Sample std | Runtime mean(s) |
|---|---:|---:|---:|
|3|6|0|0.043994|
|4|189|0|0.047088|
|6|1248|0|0.050767|
|15|1200.2|13.86|0.064215|
|26|1056.4|72.84|0.081771|
|42|1166.2|26.28|0.101169|
|48|54194.4|3861.50|0.115391|

CSV/structured JSON được kiểm tra lại bằng route invariants và cost sum độc lập, không chỉ tin exit0. Summary có mean/sample std/median/min/max, config/seed/version/source hashes; raw/history lưu trong evidence ZIP **ngoài repo** theo source_attribution.md. Không giữ thư mục reports/outputs trong cây bàn giao. Unknown optimum/gap để trống, không lấy name hint.

## Lịch sử và giới hạn bàn giao

Paired performance trước đây có median speedup khoảng1.21×/1.72×/1.68× (tournament/rank/roulette,48city,19580evaluations). **Đây là lịch sử đo phiên trước**, không phải số được đo lại trong final cleanup. Số liệu/full source/report cũ được bảo toàn trong backup; không có lệnh paired-performance mồ côi trong code bàn giao. Final cleanup không sửa GA nên không tuyên bố tối ưu mới. Kết quả âm2-opt trước đây vẫn được giữ, và batch mới cũng cho thấy trade-off âm trong preset Quick này.

Đã kiểm tra compileall, pip check ở2venv, imports, shared-domain bytes/solver signature, expected CLI EHO rejection, notebook Run All, sample config, Markdown links và cây artifact cuối. Không commit/push/reset/đổi branch; các thay đổi chưa commit trước phiên có backup và được giữ trừ phần cleanup leader đã chỉ định.

Giới hạn: Full Mode chưa chạy, chỉ5seed Quick; không có kiểm định thống kê rộng/máy thứ hai; optimum/licensing/provenance chưa xác minh đầy đủ; EHO/GUI/TSPLIB chưa có; không có suite pytest thường trực sau bàn giao. Notebook inline checks và QA release không bảo đảm thay đổi EHO tương lai không gây regression. Mọi thay đổi domain phải được leader review, nên thống nhất khôi phục regression suite từ backup khi mở giai đoạn EHO.
