# Genetic Algorithm cho symmetric TSP

Owner: Trương Thành Đạt. Cài đặt mới trong `src/ga_eho_tsp/algorithms/ga/`, dựa trên thiết kế permutation và baseline mục 7; không copy các hàm lỗi từ legacy. Các ý tưởng được đối chiếu với nguồn legacy có ghi công; không tuyên bố mã cũ là công trình của nhóm.

Chromosome là tuple (0, …) không khép vòng. Fitness chính là tour length, **nhỏ hơn tốt hơn**, không dùng nghịch đảo làm objective. Mọi run dùng RNG riêng theo seed.

```text
validate problem/config; rng = Random(seed)
population = P random permutations
costs = evaluate population; archive = best; emit history(0)
for generation in 1..min(generations, max_iterations):
    check cooperative stop/time/evaluation cap
    next_population, next_costs = best E indices + saved costs
    until next_population has P individuals:
        select two parents, independently (with replacement between calls)
        with crossover_rate: OX, otherwise immutable parent routes
        for each child, respecting exact remaining slots and budget:
            with mutation_rate per individual: apply selected mutation
            validate + objective; increment evaluations; update archive
    commit only complete population; emit scheduled stats
emit final snapshot; return archive as RunResult
```

| Module/function | Input → output | Ngữ nghĩa / side effects |
|---|---|---|
| initialization.initialize | dimension, P, RNG → list[Route] | Shuffle tail mỗi cá thể; không ép unique vì n nhỏ có ít permutation |
| selection.select_parent | population, costs, RNG, method, tournament_size → Route | Read-only inputs, RNG tiến trạng thái; có thể chọn cùng parent ở các lần gọi |
| crossover.order_crossover | hai Route cùng dimension, RNG → hai Route | OX hai điểm, chỉ tail, không sửa parent |
| mutation.mutate | Route, rate, RNG, method → Route | Một Bernoulli/cá thể, không per-gene; không sửa parent |
| survivor.select_elites | population, costs, E → routes + costs | Chọn E index tốt nhất, tie ổn định, không gán điểm 0 |
| solver.solve | problem + GAConfig + callbacks → RunResult | Không GUI/I/O/global RNG; exception callback truyền ra |

Precondition operator: route/population đã hợp lệ, costs hữu hạn không âm cùng length; config solver bảo đảm method/rate/k/size. Các operator được thiết kế để gọi nội bộ sau validation; API công khai cho app là `solve`.

## Toán tử

- **Tournament default:** lấy k index khác nhau trong một tournament, trả index có cost nhỏ nhất. Hai lần chọn bố/mẹ là độc lập. k trong 2..P. Equal fitness vẫn hoạt động.
- **Rank:** sort theo cost, tie giữ thứ tự population, trọng số tuyến tính P,P−1,…,1. Khác công thức 1/rank legacy, là biến thể rank mới được ghi tên rõ trong snapshot và docs.
- **Roulette wheel:** scale cost trước, trọng số `1−cost/max_cost`. Tất cả cost 0 hoặc bằng nhau thì chọn đều bằng RNG, không thiên vị cá thể đầu. Cá thể tệ nhất có thể trọng số 0 khi costs khác nhau; đây là quy tắc biến đổi minimization, không thay objective.
- **OX:** chọn hai vị trí khác nhau trong tail và giữ đoạn gồm hai đầu của parent A. Duyệt parent B theo vòng bắt đầu sau đoạn cắt; bỏ city đã giữ; điền các slot trống cũng theo vòng. Ví dụ parents `(0,1,2,3,4,5,6)` và `(0,4,1,6,2,5,3)`, tail cuts 1..3 (0-based tail, inclusive) tạo con đầu `(0,6,2,3,4,5,1)`. Không phải prefix crossover có tên order của legacy. n=3 có thể OX giữ toàn tail, vẫn hợp lệ; mutation cung cấp biến đổi.
- **Inversion default:** đảo tail segment inclusive cả hai đầu; n=3 rate=1 đổi `(0,1,2)` thành `(0,2,1)`. Không mắc lỗi lát cắt 1 phần tử của legacy.
- **Swap:** đổi hai vị trí khác nhau ≥1 đúng một lần khi mutation được chọn.
- **Insertion:** lấy city tại i rồi chèn vào index j của list sau khi pop; i,j lấy độc lập và khác nhau từ tail, không chỉ kéo về bên trái.
- **Scramble:** shuffle tail segment inclusive bằng RNG. Có thể trả cùng route; rate=1 không có nghĩa bắt buộc route đổi.
- **Elitism:** giữ E cá thể theo index, có thể trùng giá trị route nếu population đã trùng. Không tạo bản sao lặp bằng cách sửa fitness. E=0 vẫn giữ global-best archive.

Full run evaluations = P + G(P−E), population lẻ không mất cá thể. Mỗi objective validate permutation và tính n cạnh O(n). Tournament O(k); OX/mutation O(n); sort elites O(P log P)/vòng; rank/roulette hiện xây weights mỗi lần chọn O(P log P)/O(P), cần profile riêng trước ablation lớn. Default tournament tổng gần O(G·P·(n+k+log P)); memory O(Pn + history length).

## Trạng thái nghiệm thu

GA P0 đã có default pipeline, cả 3 selection và 4 mutation, odd population, elitism/global archive, seed/history/evaluations, callback/cancel/time/evaluation/iteration budgets, CLI và JSON, benchmark GA nhiều seed CSV/JSON. PMX P1 **chưa có**; TSPLIB loader, NN initialization, adaptive mutation, local search/2-opt, GUI mới và EHO chưa triển khai. Config có fields local search theo schema nhưng reject khi bật, không giả vờ hỗ trợ.

Chi tiết dừng/partial/history ở `architecture.md`; số liệu và profiling thực ở `experiments.md`. Chưa có chứng cứ để kết luận nhanh hơn legacy hoặc GA tốt hơn EHO.
