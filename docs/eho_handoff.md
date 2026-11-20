# Bàn giao GA cho nhóm EHO

Owner shared domain/GA: **Trương Thành Đạt**. GA P1/P2 và GUI hiện có. EHO core có `clans.py`, `solver.py`, `discrete_ops.py` và `separation.py`; solver đã được nối với clan/medoid và toán tử rời rạc, nhưng chưa được nghiệm thu bằng regression suite hoặc tích hợp CLI/GUI. Xem [thiết kế Discrete EHO](algorithm_eho.md). Không import GA private internals hoặc đổi shared schema để thích nghi với form.

## API cần dùng

```python
from ga_eho_tsp.data.matrix_loader import load_matrix
from ga_eho_tsp.domain.models import EHOConfig, IterationStat, RunResult, TSPProblem
from ga_eho_tsp.domain.protocols import Solver

# Public signature của solver EHO core.
# solve(problem: TSPProblem, config: EHOConfig, *,
#       progress_callback=None, stop_requested=None) -> RunResult
```

| Hợp đồng | Quy tắc |
|---|---|
| TSPProblem | Immutable matrix, name, source, coordinates optional, known_optimum optional, metadata; dimension property |
| Route | tuple[int,...], dài n, permutation0..n−1, route[0]=0, không lặp0 cuối |
| Objective | `problem.route_length(route)` tính đủ cạnh cuối về0; minimize. Validation chung ở domain/objective.py |
| Data | 7 ma trận trực tiếp `data/`; load_matrix trả problem đã validate và SHA256. Không coi filename suffix là optimum |
| RNG | Mỗi run tạo random.Random(config.seed), truyền cho operator; không dùng RNG global |
| Config | EHOConfig đã có, frozen; field chính clan_count, elephants_per_clan, iterations, alpha, beta, separation_count_per_clan, initialization_method, preserve_global_best |
| Base config | seed, max_iterations, max_evaluations, time_limit_seconds, record_history_every |
| Result | RunResult: algorithm, problem_name, best_route, best_distance, iterations_completed, evaluations, elapsed_seconds, seed, history, config_snapshot, stopping_reason, is_valid, metadata |
| Progress | Frozen IterationStat(iteration,best_current,best_so_far,mean_fitness,evaluations,elapsed_seconds,population_diversity=None) |

EHOConfig default 4 clans × 20 elephants, iterations 250/max_iterations 250, alpha 0.7/beta 0.3/separation 1, random initialization, preserve_global_best=True. Population property=clans×elephants. Core solver chưa được đăng ký vào GUI/CLI và cần regression review theo [thiết kế Discrete EHO](algorithm_eho.md). GAConfig có các options riêng của GA, không dùng nó để thay EHOConfig.

## Stop, history và evaluation accounting

`progress_callback(stat)` nhận snapshot, không nhận population sống. Solver không gọi Tk/Matplotlib, không I/O, không vẽ. Worker gọi solver trên thread riêng; callback chỉ enqueue. Callback lỗi phải truyền ra caller, không âm thầm trả thành công.

`stop_requested()` kiểm tra Event của GUI. Giữ best đã đánh giá khi hủy; trả reason CANCELLED. Cùng time/budget/iteration caps cần quy tắc rõ và dùng min(iterations,max_iterations). Khởi tạo đủ population atomic để có nghiệm hợp lệ/history0. Kiểm tra Stop/time trước từng candidate hoặc bước bounded thích hợp, không hứa hard real-time. Budget nhỏ hơn population bị schema reject.

Đếm mỗi full objective call một lần, kể cả route trùng và separation/rejected candidates. Những lookups/operator work không phải full evaluations vẫn nằm trong runtime. Không cộng kiểm chứng độc lập sau run vào evaluations của solver. CLI benchmark kiểm lại route/cost bên ngoài solver.

Archive global-best cập nhật sau mỗi candidate, không lấy best chỉ ở quần thể cuối. iterations_completed chỉ đếm vòng hoàn tất. Với partial iteration, giữ best của candidate đã evaluate, history cuối có evaluations thực và metadata.partial_iteration. History có thể có hai snapshot cùng iteration nhưng evaluations khác; best_current/mean/diversity chỉ từ population commit. Luôn có snapshot0/final; best_so_far không tăng. Nếu EHO không có diversity cùng định nghĩa, để None và ghi rõ.

Elapsed đo perf_counter trong solver; không bao loader/GUI/export. Cùng dataset/config/seed/version cho numeric history/route/cost tái lập, trừ time/cancel nondeterministic. GA callback có throttle ở adapter để không bắt solver redraw; result.history vẫn đầy đủ. Xem [architecture.md](architecture.md) về semantics chính xác hiện tại.

## Điểm tích hợp GUI

`algorithms/eho/solver.py` tồn tại nhưng `gui/controller.py` chưa đăng ký solver EHO và Run cho EHO vẫn bị khóa. `RunController` không import Tk và không biết GA private state; worker chỉ gọi common solve signature.

Sau khi EHO solver được review:

1. Review `clans.py`, refactor solver để dùng Clan/medoid theo [thiết kế Discrete EHO](algorithm_eho.md), và thêm/khôi phục tests correctness trước integration.
2. Sau review core, thêm import/register public EHO solve trong ALGORITHMS, giữ config_type EHOConfig. Không sửa GA registry thành alias EHO.
3. Thêm EHO form/preset riêng trong controls và chọn form theo algorithm trong app.start_run. Hiện app chỉ dựng ConfigForm GA; không được bật EHO bằng cách truyền GAConfig hoặc đổi config_type. Chỉ bước này và registration cần sửa UI, không sửa GA/domain.
4. Worker/queue/Stop, result/export, renderer tour/convergence dùng chung ngay khi EHO trả đúng contract. Không cần fake progress, coordinates hoặc history để lấp UI.
5. Bổ sung CLI/benchmark EHO thật sau tests; hiện CLI vẫn từ chối EHO. So cùng dữ liệu/objective/seeds/evaluation budgets và báo runtime/separation accounting thực.
6. Chạy lại gates, GUI Run/Stop/close/export, cùng seed reproducibility, objective cost, history/partial, 3/4/6/15/26/42/48city; EHO GUI–CLI exact numeric comparison. Không nghiệm thu chỉ vì form mở được.

## Ownership và công việc tiếp theo

| Thành viên | File/phạm vi được triển khai |
|---|---|
| EHO1 | Review clans.py và solver.py theo docs/algorithm_eho.md; xử lý core findings |
| EHO2 | Review discrete_ops.py, separation.py; khôi phục/bổ sung permutation, medoid, guided update, separation tests |
| EHO3 | EHO form/registration trong gui sau solver review; configs/experiments EHO, CLI integration qua PR leader review |
| Leader | Review shared contract, GA ownership, nghiệm thu tích hợp/benchmark |

Không tự sửa domain/*, algorithms/ga/*, matrix hoặc GUIDELINES. Thay đổi contract cần proposal có input tái hiện/tác động/tests và leader duyệt. Các tên thành viên chưa xác nhận vẫn là EHO1/2/3, không tự điền người thật.

Ưu tiên kế tiếp: khôi phục regression suite từ backup (repo đã bỏ tests theo yêu cầu cleanup), kiểm chứng core theo thiết kế, rồi tích hợp CLI/GUI → benchmark. Chưa có TSPLIB loader; dataset provenance/licensing và optimum bài lớn vẫn chưa xác minh đầy đủ. MIT không cấp lại quyền với dữ liệu/legacy chưa rõ giấy phép. Không có blocker buộc sửa shared schema để bắt đầu EHO.
