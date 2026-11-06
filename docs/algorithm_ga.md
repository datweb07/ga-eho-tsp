# GA P1 và P2 chọn lọc cho symmetric TSP

Owner: **Trương Thành Đạt**. Source chính thức được viết lại từ thiết kế permutation, không import source đàn anh. Tham chiếu/attribution và bản gốc đã bảo toàn ngoài project ở `source_attribution.md`. Core route là tuple `(0, …)` không khép vòng; fitness duy nhất là shared `TSPProblem.route_length`, minimize tour length.

## Pipeline và default

Default P0 được giữ: P80, G250, max_iterations250, tournament k3, OX rate0.9, inversion rate0.15, elites2, random-only, seed42. PMX, NN/mixed, stagnation, adaptive và 2-opt đều cần lựa chọn tường minh.

```text
validate problem/config; rng = Random(seed)
initialize population (random / multi-start NN / mixed)
evaluate P routes; archive best; history(0)
for generation = 1..min(generations,max_iterations):
    check stop/time/evaluation budget
    copy elite indices and saved scores
    prepare selection distribution once for committed population
    choose effective mutation rate (constant unless adaptive enabled)
    while next population is not full:
        select 2 parents; with crossover_rate: OX or PMX
        for child within remaining slots:
            check stop; mutate with one Bernoulli per individual
            shared objective, evaluations++, update global archive
            if 2-opt enabled:
                bounded first-improvement probes, each a FULL objective evaluation
                archive updated after every probe, even before generation commit
            append child and its final cost
    commit only full population, update stagnation and scheduled history
    optionally stop for stagnation
emit final snapshot; return global archive (not final-population-only best)
```

## Module contract

| Function | Input → output | Side effects |
|---|---|---|
| initialize | n,P,RNG; optional problem/method/fraction → list[Route] | Chỉ RNG tiến trạng thái; không sửa problem |
| nearest_neighbor | problem,start → Route | Read-only, tie city nhỏ nhất, rotate về 0 |
| prepare_selection / PreparedSelection.pick | population,costs,method,k → prepared distribution; RNG → Route | Không sửa population/costs; pick chỉ đổi RNG |
| select_parent | population,costs,RNG,method,k → Route | API P0 vẫn có; solver dùng prepared path |
| order_crossover / partially_mapped_crossover | 2 valid same-size Route,RNG → 2 Route | Không sửa parents; chỉ tail |
| mutate | Route,rate,RNG,method → Route | Bernoulli/cá thể; parent immutable |
| select_elites | population,costs,E → routes + saved costs | Chọn E index, stable tie; không gán fitness=0 |
| population_diversity | committed population → float [0,1] | Không RNG/objective calls |
| effective_mutation_rate | config,stagnation,diversity → bounded rate | Không RNG/objective calls |
| local_search.improve | valid route/cost + evaluate/stop callbacks + bounds → LocalSearchResult | Gọi evaluator cho từng full probe; không sửa parent |
| solve | problem,GAConfig,progress/stop callbacks → RunResult | Không GUI/I/O/global RNG; exception callback truyền ra |

Operator precondition: valid permutations cùng dimension, costs hữu hạn không âm tương ứng, k/rates/bounds đã qua GAConfig. Public app boundary là TSPProblem/GAConfig/solve; benchmark đối chiếu route và cost độc lập. Không dùng fast objective/cache hoặc bỏ validation public để lấy speedup.

## Selection, crossover, mutation

**Tournament:** lấy k index khác nhau, chọn cost nhỏ nhất, tie theo thứ tự sample. Hai parent picks độc lập, có thể chọn cùng route. **Rank:** stable sort ascending cost, weights P,P−1,…,1. **Roulette:** weights `1−cost/max_cost` (scale trước cộng), all-zero dùng weights đều; equal-positive cost fallback RNG choice đều. Không đổi objective thành weights. Cumulative weights/rank chỉ chuẩn bị một lần/generation; `rng.choices(cum_weights=...)` giữ cùng stream/kết quả P0.

**OX default:** chọn hai index tail khác nhau, giữ segment inclusive từ A. Duyệt B bắt đầu ngay sau segment rồi vòng về đầu, bỏ city đã giữ; điền slot trống cùng thứ tự vòng. Dùng slices/ranges thay modulo lặp thừa; không đổi cut draws/fill order. Ví dụ A=`(0,1,2,3,4,5,6)`, B=`(0,4,1,6,2,5,3)`, tail cuts1..3 → con đầu `(0,6,2,3,4,5,1)`.

**PMX:** giữ segment A[l:r] tại cùng vị trí; lập mapping `A_segment_city → B_segment_city`. Với city của B ngoài segment, theo mapping đến city không nằm trong segment A, rồi điền vị trí đó. Ví dụ A=`(0,1,2,3,4,5,6,7,8)`, B=`(0,3,7,5,1,6,8,2,4)`, tail cuts1..4 inclusive: city3 ngoài segment theo chuỗi `3→5→6`, con đầu `(0,6,2,3,4,5,8,7,1)`. Parent là permutation nên các chain từ ngoài segment không đi vào cycle đóng (cycle đóng không có nguồn ngoài); không repair ngẫu nhiên hoặc vòng thử vô hạn. Test exhaustive parents nhỏ/cuts biên, mapping chain và nhiều seed/n kiểm tra cả hai con.

**Mutation:** mọi phương pháp có đúng một xác suất/cá thể. Swap đổi hai vị trí ≥1 khác nhau; inversion đảo inclusive cả hai đầu; insertion pop i rồi insert j trên list sau pop; scramble shuffle inclusive segment bằng RNG. Rate0 giữ nguyên; rate1 áp dụng operator nhưng scramble có thể không đổi. n=3 inversion đổi `(0,1,2)` thành `(0,2,1)`; OX/PMX có thể giữ toàn tail khi n=3 nhưng vẫn hợp lệ. Không mutate parent in place.

**Elitism/global best:** giữ E index tốt nhất và score cũ (có thể trùng giá trị tour nếu population trùng), archive cập nhật sau mỗi objective, kể cả E=0 hoặc partial generation. Không mất cá thể khi P lẻ.

## Khởi tạo chuyên biệt P1

NN(start): lặp chọn city chưa thăm có `(distance,city_id)` nhỏ nhất; sau đủ city rotate city0 về đầu. Không gọi NN là tối ưu. Mỗi chu kỳ chọn permutation ngẫu nhiên của n điểm start bằng RNG; dùng từng start một lần trước khi lặp chu kỳ. Hai start có thể cho cùng chu trình sau normalize, nên **không hứa unique** và không nhân một NN tour đơn thành cả population.

`nearest_neighbor`: P NN tours đa start. `mixed`: floor(P×nn_seed_fraction) NN tours, phần còn lại random, fraction∈[0,1], default0.25. Fraction0 giữ đúng random stream; fraction1 tương đương NN. Chi phí tours luôn đánh giá lại qua shared objective và đếm P calls. Matrix lookups để xây NN không phải full objective calls nhưng có trong solver runtime. Mixed/NN là biến thể GA riêng khi benchmark với EHO sau này.

## Monitoring và adaptive P2

Diversity: canonical tour = min(route, reverse route khóa0); `(unique−1)/(P−1)`. Chỉ tính trên population commit, tại history snapshots; adaptive bật thì cần metric mỗi generation. Không làm objective evaluation thêm. Stagnation là số full generations liên tiếp không cải thiện archive, reset khi cải thiện. `stagnation_patience=None` mặc định; bật k≥1 thì reason STAGNATION khi đủ k full generations. Partial chưa commit không tăng counter.

Adaptive OFF giữ rate/RNG baseline. Khi ON, base=clamp(config.mutation_rate,min_rate,max_rate); pressure=min(1,stagnation/adaptive_patience), nếu diversity≤0.1 thì pressure≥0.5; effective=base+(max_rate−base)×pressure. Defaults min0.05/max0.5/patience20, bounds validate trong [0,1]. Khi cải thiện, pressure stagnation reset; diversity thấp vẫn có thể giữ áp lực. Metadata lưu mỗi attempted generation `{iteration,rate,completed}`, để partial không bị nhầm là full generation. Đây là policy thử nghiệm của nhóm, không khẳng định chuẩn tối ưu.

## Bounded 2-opt P2

Switch OFF mặc định, moves=0. Bật cần `local_search_max_moves>=1`, `local_search_max_probes>=1` (default20/offspring). Với child đã đánh giá, duyệt i=1..n−2, j=i+1..n−1 tăng dần, tạo route đảo inclusive i..j, tính **full** shared objective; chỉ chấp nhận strict improvement, restart scan sau move. Dừng khi đạt accepted moves, probe cap, không còn cải thiện hoặc cooperative stop/budget. Start0 không đổi.

Không dùng delta-cost trong bản này. Mọi probe, bao gồm probe tệ/đồng cost/bị reject, đều gọi objective và tăng **total evaluations**; không dùng cost check cuối thêm không đếm. Metadata `local_search_full_evaluations` đếm subset probes, `local_search_accepted_moves` đếm cải thiện. Label **GA+2-opt** trong CLI/RunResult/raw. Giữ archive ngay sau mỗi probe khi dừng giữa search; chỉ commit population đủ P. Tính đúng operator không đồng nghĩa preset này cải thiện chất lượng cùng budget: ablation hiện cho kết quả xấu hơn control ở 26/48 city, nên không bật mặc định.

## Độ phức tạp và giới hạn

Objective + validation O(n)/call. OX O(n); PMX mapping có tổng độ dài các chain rời nhau O(n) trên valid permutations, dict lookup trung bình O(1). Mutations O(n) do tuple/list copy. Tournament O(k)/pick; rank preparation O(P log P), roulette preparation O(P), weighted picks O(log P). Elites sort O(P log P)/generation. NN O(n²)/seed tour. Diversity O(Pn)/snapshot. Random/default gần O(G·P·(n+k+log P)), memory O(Pn+history). 2-opt tối đa B full O(n) probes/offspring, thêm O(G·P·B·n), move cap M và global evaluation budget cùng giới hạn; không hứa hard real-time.

P+G(P−E) evaluations đúng khi local search OFF và đủ G full generations. Local ON cộng actual full probes, partial dùng actual calls. Trong nghiệm thu, đã đo trực tiếp số lần TSPProblem.route_length được gọi bằng bộ assertions tạm ngoài repo. Khởi tạo atomic và hai iteration caps giữ nguyên; xem architecture.md.

Đã có P1: PMX, NN/mixed, profile-guided OX/prepared selection, monitoring/stagnation, CLI/export/ablation. P2 có adaptive + bounded 2-opt opt-in. GUI GA dùng trực tiếp solver này, xem [gui_guide.md](gui_guide.md). **Chưa có TSPLIB loader**, 2-opt delta engine, restart, EHO, hybrid hoặc đóng gói executable. TSPLIB hoãn vì chưa có fixture chuẩn/đối chiếu rounding/provenance đủ để nghiệm thu. Số đo và giới hạn diễn giải ở experiments.md.

Final cleanup không sửa thuật toán/default/shared contract. Suite166regression đã chạy trước khi archive/xóa theo chỉ thị leader; các mô tả kiểm thử phía trên là bằng chứng đã thực hiện, không có suite pytest đi kèm repo bàn giao. Ba notebook mới ở Experiment/ dùng trực tiếp package hiện tại, Run All Quick Mode đã được nghiệm thu từ root và Experiment/ trên hai kernel; xem [thí nghiệm](experiments.md) và [hợp đồng](architecture.md) để biết kết quả và rủi ro do bỏ regression suite.
