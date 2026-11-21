# Bàn giao EHO rời rạc cho TSP

Owner shared domain/GA: **Trương Thành Đạt**. EHO rời rạc cho TSP có `clans.py`, `solver.py`, `discrete_ops.py` và `separation.py`; mỗi clan giữ archive matriarch tốt nhất, tâm dùng medoid và các di chuyển giữ permutation hợp lệ. Solver đã được đăng ký trong CLI, benchmark và GUI. Xem [thiết kế Discrete EHO](algorithm_eho.md). EHO là biến thể rời rạc, không phải bản sao đại số của EHO liên tục.

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

EHOConfig default 4 clans × 20 elephants, iterations 250/max_iterations 250, alpha 0.7/beta 0.3/separation 1, random initialization, preserve_global_best=True. Population property=clans×elephants. Solver được gọi qua CLI/GUI bằng `EHOConfig`; cần chạy regression review theo [thiết kế Discrete EHO](algorithm_eho.md). GAConfig có các options riêng của GA, không dùng nó để thay EHOConfig.

## Stop, history và evaluation accounting

`progress_callback(stat)` nhận snapshot, không nhận population sống. Solver không gọi Tk/Matplotlib, không I/O, không vẽ. Worker gọi solver trên thread riêng; callback chỉ enqueue. Callback lỗi phải truyền ra caller, không âm thầm trả thành công.

`stop_requested()` kiểm tra Event của GUI. Giữ best đã đánh giá khi hủy; trả reason CANCELLED. Cùng time/budget/iteration caps cần quy tắc rõ và dùng min(iterations,max_iterations). Khởi tạo đủ population atomic để có nghiệm hợp lệ/history0. Kiểm tra Stop/time trước từng candidate hoặc bước bounded thích hợp, không hứa hard real-time. Budget nhỏ hơn population bị schema reject.

Đếm mỗi full objective call một lần, kể cả route trùng và separation/rejected candidates. Những lookups/operator work không phải full evaluations vẫn nằm trong runtime. Không cộng kiểm chứng độc lập sau run vào evaluations của solver. CLI benchmark kiểm lại route/cost bên ngoài solver.

Archive best toàn cục cập nhật sau mỗi candidate, không lấy best chỉ ở quần thể cuối. Archive matriarch từng clan cũng cập nhật sau mỗi candidate nhưng chỉ được commit khi generation đầy đủ; partial iteration không làm thay đổi clan đang chạy. `iterations_completed` chỉ đếm vòng hoàn tất. Với partial iteration, giữ best của candidate đã evaluate, history cuối có evaluations thực và `metadata.partial_iteration`. History có thể có hai snapshot cùng iteration nhưng evaluations khác; `best_current`/mean chỉ từ population đã commit. Luôn có snapshot 0/final; `best_so_far` không tăng. EHO chưa tính population diversity nên trường này để `None`.

Elapsed đo perf_counter trong solver; không bao loader/GUI/export. Cùng dataset/config/seed/version cho numeric history/route/cost tái lập, trừ time/cancel nondeterministic. GA callback có throttle ở adapter để không bắt solver redraw; result.history vẫn đầy đủ. Xem [architecture.md](architecture.md) về semantics chính xác hiện tại.

## Điểm tích hợp GUI

`gui/controller.py` đăng ký `eho_solve` cùng `EHOConfig`; `gui/app.py` chọn form EHO khi người dùng chọn thuật toán EHO. Worker gọi solver qua common interface, progress/stop/result dùng contract chung. GA và EHO chạy riêng từng lượt, chưa phải solver lai.

## Kiểm tra còn cần hoàn tất

| Hạng mục | Trạng thái |
|---|---|
| Package EHO rời rạc và tích hợp CLI/GUI | Đã có trong source |
| Route hợp lệ và cost khớp objective trên 7 dataset | Đã smoke-check; cần regression suite tái lập |
| Pytest regression suite | Test files có trong repo; cần chạy trong môi trường cài pytest |
| Benchmark đối chứng GA–EHO | Chưa có batch paired cùng config/seed/budget |

Các benchmark độc lập không đủ để kết luận thuật toán nào tốt hơn. Cần dùng cùng dữ liệu, seed, objective-evaluation budget và môi trường. Chưa có TSPLIB loader; dataset provenance/licensing và optimum bài lớn vẫn cần xác minh.
