# Thiết kế Discrete EHO cho TSP

Tài liệu này chốt cấu trúc package và cách chuyển các toán tử EHO sang nghiệm TSP dạng hoán vị. Nó tuân theo hợp đồng TSP trong `GUIDELINES.md`: route là tuple 0-based, city `0` đứng đầu, objective là `TSPProblem.route_length`, và mỗi lần chạy dùng RNG riêng. Tài liệu không thay đổi `EHOConfig`, shared domain hay API solver.

## Phạm vi thuật toán

EHO liên tục cập nhật vector bằng phép nhân/cộng tọa độ, trong khi route TSP là hoán vị. Vì vậy solver TSP dùng các phép swap có hướng để biểu diễn chuyển động. Đây là phép rời rạc hóa có chủ đích; không khẳng định các công thức trên hoán vị tương đương đại số với công thức liên tục.

Mỗi generation gồm các bước:

1. Từ clan hiện tại, chọn matriarch được giữ trong archive tốt nhất của clan và chọn các index separation có chi phí cao nhất. Vai trò separation được xác định từ generation cha và không xếp hạng lại sau khi tạo candidate.
2. Tính tâm clan theo định nghĩa medoid bên dưới, chỉ từ clan hiện tại.
3. Tạo generation mới đồng bộ: voi dẫn đầu đi về tâm clan theo `beta`; các voi thường đi về voi dẫn đầu theo `alpha`; các index separation nhận route ngẫu nhiên mới.
4. Đánh giá từng candidate bằng `problem.route_length(route)` đúng một lần.
5. Cập nhật archive best-so-far toàn cục và archive matriarch riêng của clan từ mọi route đã đánh giá. Sau generation hoàn chỉnh, giữ matriarch tốt nhất từng đạt được trong từng clan; archive toàn cục được giữ trong clan sở hữu nó, chỉ đưa vào clan đầu nếu vì lý do nào đó chưa có trong quần thể.

Nếu voi dẫn đầu đồng thời là voi tệ nhất (ví dụ mọi chi phí bằng nhau), voi dẫn đầu được bảo vệ; separation chọn các voi tệ tiếp theo. Tie-break theo chi phí giảm dần rồi index tăng dần. Đây là điều chỉnh để không áp dụng hai vai trò xung đột lên cùng một thành viên trong cùng generation.

## Biểu diễn clan và tâm rời rạc

`Route` giữ nguyên quy ước domain: `tuple[int, ...]`, permutation `0..n-1`, `route[0] == 0`, không nối lại city `0` ở cuối. Mỗi clan cần lưu thành viên và chi phí song song, cùng thứ tự. Thiết kế `Clan` trong `clans.py`:

```python
@dataclass(frozen=True)
class Clan:
    members: tuple[Route, ...]
    costs: tuple[float, ...]
```

Invariant: clan không rỗng; `len(members) == len(costs)`; mọi route hợp lệ và mọi cost hữu hạn, không âm. `Clan.best_index()`, `Clan.worst_indices(count, protected_indices=())`, `Clan.center_index()` và `Clan.center()` trả kết quả xác định, không làm thay đổi clan tại chỗ. Việc tạo generation kế tiếp tạo `Clan` mới để routes và costs không thể lệch nhau khi thay voi.

Không có trung bình số học tự nhiên của các permutation. Tâm clan vì vậy là **medoid**: route trong chính clan có tổng khoảng cách Hamming nhỏ nhất tới các route còn lại. Hamming distance chỉ xét vị trí `1..n-1`, giữ city `0` cố định như `discrete_ops.hamming_distance`.

```text
center_index = argmin_i (sum_j hamming_distance(members[i], members[j]), costs[i], i)
center = members[center_index]
```

Tie-break lần lượt theo tổng khoảng cách nhỏ hơn, chi phí TSP nhỏ hơn, rồi index ban đầu nhỏ hơn. Cách này luôn trả về một route hợp lệ có sẵn trong clan, xác định khi chạy lại cùng input. Chi phí tính tâm là `O(m² n)` với `m` voi/clan và `n` thành phố; với kích thước clan mặc định, chưa cần cache.

Khoảng cách Hamming so thứ tự vị trí nên route đảo chiều có thể cách xa dù tương đương trong symmetric TSP. Đây là hạn chế đã chấp nhận cho baseline đơn giản và tương thích toán tử hiện có. Nếu chuyển sang khoảng cách cạnh/đảo chiều-aware, đó là một biến thể khác cần ghi thành quyết định riêng và benchmark riêng.

## Toán tử rời rạc

Các phép di chuyển dùng `_guided_swap(source, target, strength, rng)` trong `discrete_ops.py`:

- `strength == 0`: giữ nguyên source.
- `strength == 1`: trả target.
- `0 < strength < 1`: lấy số bước có giới hạn từ strength, một số ngẫu nhiên và số vị trí khác nhau; xáo thứ tự vị trí sai khác rồi swap city cần thiết về đúng vị trí.
- Không swap index `0`; output luôn là permutation hợp lệ. Các thao tác không sửa route đầu vào.

`move_toward_best(route, clan_leader, alpha, rng)` dùng cho voi thường. `update_matriarch(clan_leader, clan_center, beta, rng)` dùng cho voi dẫn đầu. Các helper trong `solver.py` không được tự viết lại luật guided swap; solver phải gọi các public operator này để test toán tử cũng bao phủ đúng đường chạy thật.

Separation trong `separation.py` thay các index được xếp hạng từ chi phí của clan cha bằng random permutation mới bắt đầu ở city `0`. Solver phải giữ nguyên index vai trò đã tính từ clan cha cho tới hết generation; không chọn lại voi tệ nhất từ chi phí candidate mới. Helper cần hỗ trợ index được bảo vệ (matriarch), để tránh tách đúng voi vừa được cập nhật theo `beta`. Sau khi đánh giá candidate, cập nhật member và cost cùng index. Archive best-so-far được bảo vệ khi commit generation theo config.

## Package boundaries

```text
src/ga_eho_tsp/algorithms/eho/
├── __init__.py       # public export: solve
├── clans.py          # Clan, best/worst member, medoid center
├── discrete_ops.py   # Hamming distance, guided swap, alpha/beta moves
├── separation.py     # thay các member tệ bằng random permutations
└── solver.py         # khởi tạo, generation loop, budget/stop/history/result
```

`clans.py`, `discrete_ops.py`, `separation.py` không phụ thuộc solver, GUI, CLI hoặc GA private internals. `solver.py` điều phối chúng và chỉ gọi shared domain để đánh giá route/validate result. Public API vẫn là:

```python
solve(problem, config, *, progress_callback=None, stop_requested=None) -> RunResult
```

## Quy tắc cho vòng lặp và kết quả

- Tạo `random.Random(config.seed)` một lần cho mỗi run và truyền cùng RNG cho initialization/operators.
- Đánh giá population khởi tạo đủ trước snapshot iteration 0; config đã bảo đảm evaluation budget tối thiểu đủ khởi tạo.
- Đếm mỗi lần gọi objective, kể cả route trùng và route separation; không tính lại route chỉ để ghi history.
- Archive best cập nhật sau từng lần evaluate. Population chỉ commit khi generation đầy đủ; nếu dừng giữa generation, trả archive tốt nhất đã thấy, giữ population commit gần nhất, và đánh dấu `metadata.partial_iteration`.
- `iterations_completed` chỉ tăng sau generation hoàn tất. History luôn có iteration 0 và snapshot cuối; `best_so_far` không tăng.
- Mọi callback nhận `IterationStat`, không nhận population có thể sửa. Solver không phụ thuộc Tkinter/Matplotlib và không thực hiện I/O.
- Reason dừng tuân theo shared architecture: `MAX_ITERATIONS`, `MAX_EVALUATIONS`, `TIME_LIMIT`, `CANCELLED`.

## Cấu trúc hiện tại và phần còn lại

`clans.py`, `discrete_ops.py`, `separation.py` và `solver.py` được nối thành solver EHO rời rạc: beta hướng matriarch về medoid, alpha hướng voi thường về matriarch, separation bảo vệ matriarch và archive từng clan giữ lại leader tốt nhất của clan. Archive toàn cục vẫn được trả về trong `RunResult`. Đây là thiết kế thích nghi cho hoán vị TSP, không phải phép biến đổi đại số tương đương EHO trên vector liên tục.

CLI, benchmark và GUI hiện đều đăng ký EHO. GUI cung cấp form EHO riêng; benchmark dùng chung loader/objective với GA để có thể so sánh trong cùng budget và seed. Muốn tuyên bố thuật toán đã được nghiệm thu đầy đủ vẫn cần chạy regression suite và benchmark đối chứng GA–EHO.

## Kiểm tra correctness và giới hạn còn lại

Để nghiệm thu core sau các thay đổi, cần chạy regression tests cho các nhóm sau:

1. Clan giữ đồng bộ member/cost; best/worst tie-break xác định; medoid đúng với tính tay và luôn là member hợp lệ.
2. Guided swap giữ permutation, cố định city `0`, không tăng Hamming distance tới target, có biên strength `0/1`, và không sửa input.
3. Separation thay đúng số member tệ nhất, giữ clan size và đồng bộ cost khi solver đánh giá replacement.
4. Solver dùng đúng `move_toward_best`, `update_matriarch`, `separate`; lưu matriarch tốt nhất theo clan; cùng seed cho route/history/counters giống nhau.
5. Objective cost khớp tính độc lập; evaluation count, generation cap, budget, timeout/cancel, partial iteration, history và archive best tuân shared architecture.
6. Chạy cases `3, 4, 6, 15, 26, 42, 48` thành phố; kiểm tra route hợp lệ ở mọi snapshot/result.

Tài liệu thiết kế không tự khẳng định các ca kiểm tra đã chạy.
