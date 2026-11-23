# Nội dung báo cáo đồ án - Genetic Algorithm và Discrete EHO cho TSP

> **Phạm vi tài liệu:** Trình bày mô hình TSP, hai solver GA và Discrete EHO (D-EHO), cách triển khai, thí nghiệm, kết quả và giới hạn. GA và EHO là hai thuật toán độc lập; chương trình chưa kết hợp chúng thành một thuật toán lai.

> **Rà soát gần nhất:** 2026-11-23, source commit `4cb9947`. Benchmark được chạy lại cho GA và EHO: mỗi thuật toán có 35 lần chạy trên 7 bộ dữ liệu × 5 seed, tối đa 6.000 objective evaluations/run; 35/35 lượt của mỗi thuật toán trả kết quả hợp lệ. `compileall` thành công; pytest chưa chạy được vì môi trường `.venv` không có module `pytest`.

---

## Trạng thái triển khai và kiểm tra

| Hạng mục | Trạng thái | Ghi chú |
|---|---|---|
| GA package | ✅ | Solver, initialization, selection, crossover, mutation, local search, monitoring và survivor |
| EHO package | ✅ | Clan, Hamming medoid, guided-swap, separation và archive theo clan/toàn cục |
| Shared domain và data loader | ✅ | Dùng chung TSP objective; 7 ma trận dữ liệu |
| CLI và benchmark | ✅ | Hỗ trợ chạy GA/EHO và benchmark nhiều seed |
| GUI | ✅ | Chọn GA hoặc EHO, mỗi lần chạy dùng một solver |
| GA benchmark | ✅ | 35/35 lượt hợp lệ, 6.000 evaluations/run |
| EHO benchmark | ✅ | 35/35 lượt hợp lệ, 6.000 evaluations/run |
| `pytest -q` | ⚠️ Chưa chạy | Project `.venv` thiếu `pytest`; không báo suite pass |

## Đề tài

**Ứng dụng thuật toán Genetic Algorithm và Elephant Herding Optimization cho bài toán người du lịch (Traveling Salesman Problem - TSP)**

### Phạm vi thuật toán

GA và D-EHO dùng chung biểu diễn route, hàm mục tiêu và cơ chế đánh giá nhưng giữ hai vòng lặp solver riêng. Nội dung dưới đây mô tả implementation hiện tại và không xem hai thuật toán là một solver lai.

GA nằm trong `src/ga_eho_tsp/algorithms/ga/`, D-EHO nằm trong `src/ga_eho_tsp/algorithms/eho/`, và cả hai dùng mô hình chung ở `src/ga_eho_tsp/domain/`.

# CHƯƠNG 1. TỔNG QUAN

## 1.1. Giới thiệu bài toán người du lịch

Bài toán người du lịch, thường được gọi là Traveling Salesman Problem (TSP), mô tả tình huống một người cần đi qua một tập thành phố. Mỗi thành phố phải được thăm đúng một lần, người đi bắt đầu từ một thành phố xác định, sau đó quay lại thành phố xuất phát. Mục tiêu là chọn thứ tự ghé thăm sao cho tổng chi phí của cả chuyến đi nhỏ nhất.

Trong đồ án này, chi phí giữa hai thành phố được lưu thành ma trận khoảng cách. Ma trận có một hàng và một cột cho mỗi thành phố. Phần tử ở hàng `i`, cột `j` biểu diễn chi phí đi từ thành phố `i` đến thành phố `j`. Phiên bản hiện tại tập trung vào symmetric TSP: chi phí đi từ `i` đến `j` bằng chi phí đi ngược từ `j` về `i`. Đây là một bài toán tổ hợp vì số thứ tự có thể ghé thăm tăng rất nhanh khi số thành phố tăng. Do đó, việc liệt kê tất cả hành trình để tìm đáp án tốt nhất chỉ phù hợp với các bài rất nhỏ.

## 1.2. Phát biểu bài toán

Gọi tập thành phố là `V = {0, 1, ..., n-1}` và ma trận khoảng cách là `D`. Một hành trình hợp lệ là hoán vị `π` của toàn bộ các thành phố, trong đó `π[0] = 0`. Chi phí của hành trình là tổng chi phí đi giữa hai thành phố liên tiếp, cộng thêm cạnh quay từ thành phố cuối về thành phố 0:

```text
L(π) = D[π[0], π[1]] + D[π[1], π[2]] + ...
       + D[π[n-2], π[n-1]] + D[π[n-1], π[0]]
```

Mục tiêu là tìm hành trình có `L(π)` nhỏ nhất. Trong chương trình, route được lưu dưới dạng tuple 0-based, ví dụ `(0, 3, 2, 1)`. Route lõi không lặp lại thành phố 0 ở cuối; hàm mục tiêu tự tính cạnh quay về đầu. Khi trình bày cho người dùng, CLI hoặc GUI có thể thêm thành phố 0 ở cuối để biểu diễn hành trình khép kín.

Một nghiệm phải thỏa mãn đồng thời ba điều kiện: có đúng `n` phần tử, bắt đầu bằng 0, và mỗi số từ 0 đến `n-1` xuất hiện đúng một lần. Việc kiểm tra các điều kiện này giúp loại các chuỗi không phải hành trình, chẳng hạn route bị thiếu thành phố, có thành phố lặp hoặc làm thay đổi điểm xuất phát.

Ma trận đầu vào được kiểm tra là ma trận vuông có ít nhất ba thành phố, các chi phí hữu hạn và không âm, đường chéo bằng 0, đồng thời đối xứng. Dữ liệu của repository là các ma trận văn bản, mỗi dòng chứa một hàng số cách nhau bằng khoảng trắng và không có dòng tiêu đề. Những số trong tên file dữ liệu chỉ được xem là gợi ý của nguồn ban đầu; chúng chưa được xác minh độc lập như optimum chính thức.

## 1.3. Hướng tiếp cận giải quyết

GA mô phỏng quá trình tiến hóa để tìm kiếm nghiệm tốt. Thay vì chỉ duy trì một hành trình, thuật toán giữ một quần thể gồm nhiều hành trình. Mỗi vòng lặp chọn các hành trình cha, kết hợp một phần thứ tự của chúng để tạo hành trình con, áp dụng đột biến để thay đổi một đoạn, sau đó hình thành quần thể kế tiếp.

Trong đồ án, một cá thể chính là một route hợp lệ của TSP. Chất lượng của cá thể được đo trực tiếp bằng tổng độ dài hành trình. Vì bài toán cần tối thiểu hóa, route có tổng chi phí nhỏ hơn được xem là tốt hơn. Cùng một hàm mục tiêu `TSPProblem.route_length` được dùng trong toàn bộ GA; route không có một công thức fitness riêng khác với công thức dùng để báo cáo kết quả.

EHO cũng được áp dụng cho cùng bài toán, nhưng lời giải TSP là hoán vị chứ không phải vector số thực. Vì vậy implementation dùng Discrete EHO (D-EHO): giữ cấu trúc clan và các vai trò của EHO, đồng thời thay phép cập nhật tọa độ bằng toán tử trên hoán vị. Hai solver dùng chung objective nhưng vận hành độc lập.

GA là phương pháp tìm kiếm ngẫu nhiên có định hướng, nên một lần chạy không đảm bảo tìm được optimum toàn cục. Seed được truyền rõ ràng để có thể lặp lại cùng một cấu hình. Kết quả thí nghiệm vì vậy cần được đọc cùng số seed, số lần đánh giá hàm mục tiêu, thời gian chạy và cách chọn cấu hình, thay vì chỉ nhìn vào một route tốt nhất.

# CHƯƠNG 2. GIẢI THUẬT DI TRUYỀN

## 2.1. Giới thiệu về Genetic Algorithm

Genetic Algorithm là một thuật toán tối ưu lấy cảm hứng từ chọn lọc tự nhiên. Thuật toán bắt đầu với một tập nghiệm ứng viên, đánh giá chất lượng từng nghiệm, sau đó dùng các nghiệm tốt để tạo thế hệ tiếp theo. Qua nhiều vòng lặp, các nghiệm tốt có cơ hội được giữ lại hoặc truyền một phần cấu trúc sang các nghiệm mới.

Với bài toán TSP, việc biểu diễn bằng chuỗi bit thông thường không thuận tiện vì một hành trình cần là hoán vị, không được lặp hoặc bỏ thành phố. Do đó, repository dùng permutation representation: mỗi route chứa đầy đủ các thành phố đúng một lần và khóa thành phố 0 ở vị trí đầu. Các toán tử lai ghép và đột biến đều chỉ thao tác trên phần route sau thành phố 0 để giữ bất biến này.

Các tham số GA có ảnh hưởng đến sự cân bằng giữa khai thác nghiệm hiện có và tìm kiếm vùng mới. Quần thể lớn hơn thường giữ được nhiều phương án hơn nhưng cần nhiều lượt đánh giá. Mutation rate cao tạo thay đổi thường xuyên hơn nhưng có thể phá vỡ cấu trúc tốt. Crossover rate quyết định tần suất ghép cặp cha mẹ. Elitism giữ một số nghiệm tốt nhất để chúng không bị mất ở thế hệ sau. Các tham số này cần được so sánh dưới cùng điều kiện tính toán trước khi kết luận cấu hình nào tốt hơn.

## 2.2. Cách áp dụng GA cho TSP trong repository

### 2.2.1. Luồng xử lý tổng quát

Quy trình của một lần chạy GA gồm các bước sau:

1. Kiểm tra `TSPProblem` và `GAConfig`, bao gồm giới hạn tham số, ma trận và ngân sách tính toán.
2. Khởi tạo quần thể route. Mặc định, mỗi route được sinh ngẫu nhiên và chuẩn hóa để thành phố 0 luôn đứng đầu.
3. Tính độ dài cho từng route bằng shared objective, đếm số lần đánh giá và lưu best route toàn cục.
4. Ghi snapshot ban đầu vào lịch sử. Snapshot chứa best hiện tại, best toàn lịch sử, trung bình chi phí, số evaluations, thời gian và diversity.
5. Tạo quần thể kế tiếp bằng cách sao chép elites, chuẩn bị selection, chọn cha mẹ, lai ghép, đột biến và đánh giá con.
6. Chỉ commit một thế hệ khi quần thể mới đã đầy đủ. Nếu dừng giữa thế hệ do cancellation, time limit hoặc evaluation budget, các ứng viên đã được đánh giá vẫn được xét vào global best nhưng quần thể dở dang không được commit.
7. Kiểm tra điều kiện dừng, ghi snapshot cuối và trả `RunResult` chứa route tốt nhất của toàn bộ lần chạy, không chỉ route tốt nhất trong quần thể cuối.

Pseudocode dưới đây mô tả đường chạy mặc định. Các tùy chọn như PMX, khởi tạo nearest-neighbor, adaptive mutation và 2-opt chỉ được bật khi người dùng chọn rõ ràng.

```text
kiểm tra bài toán và cấu hình
tạo RNG riêng từ seed
tạo P route ngẫu nhiên
đánh giá P route; lưu global best và history ở iteration 0

cho mỗi iteration trong giới hạn cấu hình:
    kiểm tra stop request, time limit và evaluation budget
    giữ lại E cá thể tốt nhất cùng chi phí đã biết
    chuẩn bị phương pháp selection cho quần thể hiện tại
    khi quần thể kế tiếp chưa đủ P cá thể:
        chọn hai cha mẹ
        với xác suất crossover_rate, áp dụng OX (mặc định)
        với từng con cần thêm:
            áp dụng inversion mutation với xác suất mutation_rate
            đánh giá bằng TSPProblem.route_length
            cập nhật global best nếu tốt hơn
            thêm con vào quần thể kế tiếp
    nếu thế hệ đầy đủ thì commit, cập nhật stagnation và ghi history

trả global best và RunResult
```

### 2.2.2. Khởi tạo quần thể và seed

Mặc định, GA dùng random initialization. Các hoán vị được tạo bằng RNG của lần chạy, không sử dụng bộ sinh số ngẫu nhiên toàn cục. Do vậy, khi giữ nguyên dữ liệu, cấu hình và seed, route, distance, số evaluations và lịch sử số học có thể tái lập; thời gian thực tế có thể thay đổi giữa các lần chạy.

Repository cũng có hai phương án khởi tạo opt-in. `nearest_neighbor` tạo route tham lam từ nhiều điểm bắt đầu khác nhau: ở mỗi bước chọn thành phố chưa thăm có cạnh gần nhất, nếu bằng nhau thì chọn mã thành phố nhỏ hơn. `mixed` đặt một tỷ lệ route nearest-neighbor vào quần thể, phần còn lại là route ngẫu nhiên. Đây là biến thể khởi tạo của GA, không phải solver thứ ba, và kết quả không được gọi là nghiệm tối ưu chỉ vì bắt đầu bằng một heuristic.

### 2.2.3. Chọn cha mẹ

Selection quyết định cá thể nào có cơ hội làm cha mẹ. Bài toán dùng minimization, nên chi phí nhỏ hơn phải có lợi thế. Ba phương pháp hiện có là:

- **Tournament:** lấy ngẫu nhiên một nhóm `k` cá thể khác nhau và chọn cá thể có chi phí thấp nhất trong nhóm. Đây là lựa chọn mặc định.
- **Rank:** sắp thứ tự cá thể từ tốt đến kém và gán trọng số theo thứ hạng. Cách này làm selection ít nhạy với chênh lệch thô về độ dài route.
- **Roulette wheel:** biến chi phí thành trọng số chọn phù hợp với minimization. Trường hợp các chi phí bằng nhau hoặc trọng số bằng 0 được xử lý bằng lựa chọn đều thay vì chia cho 0 hoặc tạo phân phối không hợp lệ.

Trong mỗi thế hệ, phân phối rank/roulette được chuẩn bị một lần rồi dùng nhiều lần để lấy cha mẹ. Việc chuẩn bị không thay đổi population hoặc chi phí đã tính. Hai lượt chọn cha mẹ là độc lập, nên cùng một route có thể được chọn hai lần.

### 2.2.4. Lai ghép permutation

**Order Crossover (OX)** là phương pháp mặc định. OX chọn một đoạn liên tiếp trên phần đuôi của route cha thứ nhất và giữ nguyên đoạn đó ở cùng vị trí trong con. Sau đó, thuật toán duyệt route cha còn lại theo thứ tự vòng, bỏ các thành phố đã có trong đoạn giữ lại và điền vào các vị trí trống. Nhờ vậy, con vẫn là permutation hợp lệ và giữ được thông tin thứ tự từ cả hai cha mẹ.

**Partially Mapped Crossover (PMX)** là một lựa chọn khác. PMX giữ một đoạn của cha thứ nhất, rồi dùng ánh xạ giữa đoạn của hai cha mẹ để xử lý thành phố bị trùng ở ngoài đoạn. Cả OX và PMX chỉ thao tác trên tail, không đổi vị trí thành phố 0. Hai toán tử không sửa route cha tại chỗ và dùng RNG được truyền vào.

### 2.2.5. Đột biến

Mutation được áp dụng với một xác suất trên mỗi cá thể con. Điều này giúp tham số mutation rate có cùng ý nghĩa giữa các phương pháp. Bốn phương pháp hiện có là:

- **Inversion:** đảo ngược thứ tự một đoạn liên tiếp. Đây là mutation mặc định.
- **Swap:** đổi chỗ hai thành phố ở hai vị trí khác nhau.
- **Insertion:** lấy một thành phố ra và chèn vào vị trí khác.
- **Scramble:** xáo trộn thứ tự bên trong một đoạn.

Mọi thao tác đều giữ thành phố 0 đứng đầu và không làm thay đổi route cha. Nếu mutation rate bằng 0 thì route con được giữ nguyên; nếu bằng 1 thì toán tử được áp dụng cho từng route con, dù một số thao tác scramble có thể tình cờ tạo lại cùng thứ tự.

### 2.2.6. Elitism và global best

Elitism sao chép `elite_count` route tốt nhất sang quần thể kế tiếp và giữ lại fitness đã tính. Điểm số không bị gán về 0, vì cách đó sẽ làm sai thứ tự minimization và có thể chọn lặp sai cá thể. Kích thước quần thể được lấp theo số slot còn thiếu, vì vậy cấu hình có population size lẻ không làm giảm kích thước thế hệ.

Song song với population hiện tại, solver duy trì global best. Mỗi route được đánh giá đều có cơ hội cập nhật archive này. Kết quả cuối do đó vẫn giữ route tốt nhất đã gặp, ngay cả khi route ấy không còn nằm trong quần thể cuối hoặc thuật toán bị dừng giữa một thế hệ. Đây là điểm quan trọng để kết quả không xấu đi chỉ vì một thế hệ mới có các con kém hơn.

### 2.2.7. Điều kiện dừng và lịch sử

GA dừng khi đạt số generations hoặc `max_iterations` nhỏ hơn, hết `max_evaluations`, hết time limit, nhận yêu cầu cancellation, hoặc đạt `stagnation_patience` nếu cấu hình bật điều kiện trì trệ. Việc khởi tạo được đánh giá đầy đủ trước khi bắt đầu các thế hệ, nên `max_evaluations` phải đủ cho population ban đầu. Time limit và cancellation được kiểm tra tại các điểm an toàn giữa các lượt đánh giá; chúng là cơ chế dừng hợp tác, không phải bảo đảm hard real-time.

`RunResult` lưu thuật toán, tên bài toán, best route, best distance, số iteration hoàn tất, số evaluations, elapsed time, seed, history, cấu hình đã dùng, stopping reason, trạng thái hợp lệ và metadata. `IterationStat` lưu iteration, best trong population đã commit, best toàn cục, fitness trung bình, evaluations tích lũy, thời gian và population diversity. History có snapshot ban đầu và snapshot cuối; `record_history_every` điều khiển tần suất ghi các mốc trung gian.

Callback progress nhận một snapshot read-only. Callback stop được kiểm tra trong solver. Solver không phụ thuộc GUI, không thực hiện I/O trong vòng lặp và không dùng RNG toàn cục. CLI, benchmark và GUI gọi cùng API solver; vì vậy phần trình bày không thay đổi logic tối ưu.

### 2.2.8. Các phương án nâng cao đã chọn

GA có thêm một số lựa chọn ngoài đường mặc định:

- **Stagnation stopping:** dừng sau số thế hệ đầy đủ liên tiếp không cải thiện global best đã cấu hình.
- **Adaptive mutation:** điều chỉnh mutation rate theo mức trì trệ và diversity; tùy chọn này tắt mặc định để giữ hành vi baseline.
- **Bounded 2-opt:** thử các phép đảo đoạn theo first-improvement với giới hạn số move, số probe và evaluation budget. Mỗi probe tính lại toàn bộ objective và được tính vào evaluation count, do đó không bị xem như thao tác miễn phí.
- **PMX và nearest-neighbor/mixed initialization:** cho phép so sánh các lựa chọn GA mà không thay shared objective hoặc route representation.

2-opt được xem là thành phần local search hỗ trợ GA, không được giới thiệu thành thuật toán tối ưu chính thứ ba. Kết quả thí nghiệm hiện tại không cho thấy 2-opt luôn có lợi dưới cùng budget; vì vậy nó vẫn là tùy chọn và không được bật trong cấu hình mặc định.

### 2.2.9. Tổ chức mã nguồn

| Module | Vai trò |
|---|---|
| `domain/models.py` | Schema `TSPProblem`, `GAConfig`, `RunResult`, `IterationStat` và kiểm tra cấu hình |
| `domain/objective.py` | Kiểm tra ma trận/route và tính chi phí chu trình |
| `data/matrix_loader.py` | Đọc ma trận khoảng trắng thành `TSPProblem` |
| `data/registry.py` | Khai báo tên các bộ dữ liệu và để `known_optimum=None` khi chưa xác minh |
| `algorithms/ga/initialization.py` | Random, nearest-neighbor và mixed initialization |
| `algorithms/ga/selection.py` | Tournament, rank và roulette selection |
| `algorithms/ga/crossover.py` | OX và PMX |
| `algorithms/ga/mutation.py` | Inversion, swap, insertion và scramble |
| `algorithms/ga/survivor.py` | Elitism và xây dựng phần quần thể sống sót |
| `algorithms/ga/monitoring.py` | Diversity và mutation rate thích nghi |
| `algorithms/ga/local_search.py` | Bounded 2-opt opt-in |
| `algorithms/ga/solver.py` | Vòng lặp GA, global best, history, stop và kết quả |
| `algorithms/eho/clans.py` | Clan, xếp hạng member và Hamming medoid |
| `algorithms/eho/discrete_ops.py` | Hamming distance, guided-swap, alpha/beta update |
| `algorithms/eho/separation.py` | Separation bằng permutation mới hợp lệ |
| `algorithms/eho/solver.py` | Vòng lặp D-EHO, archive theo clan/toàn cục, stop và kết quả |
| `cli.py` | Lệnh validate, solve GA/EHO và benchmark nhiều seed |
| `experiments/benchmark.py` | Chạy lặp, kiểm tra kết quả và xuất summary/CSV/JSON |
| `gui/` | Form Tkinter, chọn GA/EHO và điều phối solver trong worker |

GA và EHO dùng chung `TSPProblem`, objective và `RunResult`; các module EHO không gọi nội bộ GA. Giao diện cho phép chọn một solver cho mỗi lần chạy, chưa có thuật toán kết hợp GA–EHO.

# CHƯƠNG 3. THUẬT TOÁN ELEPHANT HERDING OPTIMIZATION

## 3.1. Tổng quan về Elephant Herding Optimization

Elephant Herding Optimization (EHO) là thuật toán quần thể lấy cảm hứng từ hành vi sống theo đàn của voi. Quần thể được chia thành các clan; mỗi clan có một matriarch dẫn dắt, các voi thường cập nhật lời giải theo matriarch, và một số voi có chi phí cao nhất được separation để duy trì khám phá.

### 3.1.1. Khái niệm và nguyên lý

Trong EHO liên tục, vị trí voi thường được cập nhật theo matriarch:

```text
p[i,c]^(t+1) = p[i,c]^t + alpha * r * (p[best,c]^t - p[i,c]^t)
```

Matriarch cập nhật theo tâm clan, còn cá thể được separation được tạo lại trong miền tìm kiếm. Trong các công thức này, `alpha` và `beta` điều khiển mức ảnh hưởng; `r` là số ngẫu nhiên trong `[0,1)`.

Tutorial về swarm intelligence trình bày các công thức EHO liên tục ở trang in 150–154. Những công thức đó dùng vector số thực. Vì route TSP là hoán vị, không thể cộng/trừ trực tiếp các route hoặc lấy trung bình số học mà vẫn giữ được nghiệm hợp lệ. Dự án do đó dùng D-EHO, một phép thích nghi rời rạc cho không gian hoán vị, không tuyên bố tương đương đại số với EHO liên tục.

### 3.1.2. Các thành phần chính

- **Clan:** nhóm các route cùng tiến hóa.
- **Matriarch:** route có tổng chi phí thấp nhất trong clan.
- **Tâm clan:** route đại diện cho clan; trong D-EHO là Hamming medoid.
- **Clan updating:** cập nhật matriarch và đưa các voi thường về phía matriarch.
- **Separating:** thay các route tệ nhất bằng route ngẫu nhiên hợp lệ.
- **Elitism:** lưu nghiệm tốt nhất theo clan và toàn cục qua các thế hệ.

## 3.2. Áp dụng EHO cho bài toán TSP

### 3.2.1. Biểu diễn nghiệm và hàm mục tiêu

Mỗi cá thể là route `pi = (0, pi_1, ..., pi_(n-1))`, trong đó phần sau city `0` là hoán vị của các thành phố còn lại. Độ dài chu trình tính cả cạnh quay về điểm đầu:

```text
L(pi) = sum(i=0..n-2) D[pi_i, pi_(i+1)] + D[pi_(n-1), pi_0]
```

Shared objective kiểm tra route hợp lệ rồi tính `L(pi)`. Dữ liệu hiện tại là symmetric TSP với ma trận hữu hạn, không âm, đối xứng và đường chéo bằng 0.

### 3.2.2. Phân chia quần thể thành Clan

Quần thể gồm `N_c` clan, mỗi clan có `m` route. `Clan(members, costs)` giữ route và chi phí khớp theo cùng index. Matriarch được chọn bằng chi phí tour nhỏ nhất. Mọi clan được tạo thành đối tượng bất biến để route và cost không lệch nhau khi cập nhật.

### 3.2.3. Tâm clan và cập nhật Matriarch

Do không có trung bình tự nhiên của các hoán vị, tâm clan được chọn là route trong clan có tổng Hamming distance nhỏ nhất tới các route khác:

```text
d_H(pi, sigma) = sum(j=1..n-1) [pi_j != sigma_j]
center_c = argmin(pi in clan_c) sum(sigma in clan_c) d_H(pi, sigma)
```

Nếu hòa, chọn route có tour cost thấp hơn rồi chọn index nhỏ hơn. Matriarch được dịch về phía medoid bằng guided-swap với `beta`.

### 3.2.4. Di chuyển voi thường (Clan Updating Operator)

Với route nguồn `pi`, route đích `target` và strength `s` (`alpha` hoặc `beta`), D-EHO tìm các vị trí sai khác ở index từ 1 trở đi. Số swap tối đa được lấy theo:

```text
k = floor(s * r * |diff|),   r ~ U[0,1)
```

Toán tử xáo thứ tự các vị trí sai khác rồi đưa thành phố đích về vị trí tương ứng bằng swap. `s=0` giữ nguyên route; `s=1` trả route đích; các giá trị giữa hai biên chỉ thực hiện một phần các swap. Route đầu vào không bị sửa và city `0` luôn giữ ở đầu.

### 3.2.5. Tách đàn (Separating Operator)

Solver chọn `separation_count_per_clan` route có chi phí cao nhất trong clan cha, bảo vệ matriarch và thay các route được chọn bằng permutation ngẫu nhiên hợp lệ. Vai trò separation được xác định từ clan cha và giữ cố định trong generation đó.

### 3.2.6. Bảo tồn nghiệm tốt nhất (Elitism)

Solver khởi tạo archive tốt nhất cho từng clan và global best từ quần thể ban đầu. Mỗi candidate được đánh giá đúng một lần; nếu tốt hơn, route cập nhật archive tương ứng. Sau generation hoàn chỉnh, nếu archive clan không còn trong clan thì solver thay member tệ nhất bằng route lưu trữ, đồng thời giữ matriarch hiện tại. Nếu dừng giữa generation, population chưa hoàn chỉnh không được commit nhưng global best vẫn giữ nghiệm tốt nhất đã đánh giá.

## 3.3. Quy trình hoạt động của D-EHO

```text
Khởi tạo N_c clan, mỗi clan m route hợp lệ; tính objective cho quần thể
Khởi tạo clan archive và global best
Lặp đến khi đạt giới hạn thế hệ/evaluations/thời gian hoặc bị hủy:
    Với mỗi clan:
        Chọn matriarch và tính Hamming medoid từ clan hiện tại
        Chọn các index separation, không chọn matriarch
        Với từng voi:
            matriarch -> guided-swap về medoid theo beta
            voi separation -> route permutation ngẫu nhiên
            voi thường -> guided-swap về matriarch theo alpha
            tính objective một lần; cập nhật archive clan/global
        nếu đủ member: khôi phục archive clan khi cần
    nếu tất cả clan hoàn chỉnh: commit population mới
    nếu dừng giữa generation: không commit population dở dang
Trả global best và RunResult
```

### Cập nhật một voi trong `solver.py`

```python
if index == leader_index:
    candidate = update_matriarch(route, center, config.beta, rng)
elif index in separated:
    candidate = separated_members[index]
else:
    candidate = move_toward_best(route, leader, config.alpha, rng)

cost = problem.route_length(candidate)
evaluations += 1
if cost < best_distance:
    best_route, best_distance = candidate, cost
```

## 3.4. Triển khai và kiểm tra D-EHO

### 3.4.1. Module

`clans.py` lưu clan và tính medoid; `discrete_ops.py` triển khai Hamming distance và guided-swap; `separation.py` tạo route separation; `solver.py` điều phối khởi tạo, vòng lặp, stop, archive và `RunResult`. EHO dùng `EHOConfig` ở `domain/models.py` và `TSPProblem.route_length` ở shared domain. CLI, GUI và benchmark đều gọi cùng public solver.

### 3.4.2. Tham số và điều kiện

- `clan_count >= 2`; `elephants_per_clan >= 3`.
- `iterations` và `max_iterations` là số nguyên dương; số thế hệ tối đa lấy giá trị nhỏ hơn.
- `alpha, beta ∈ [0,1]`; mặc định lần lượt là `0.7` và `0.3`.
- `0 <= separation_count_per_clan < elephants_per_clan`; matriarch không bị separation.
- Baseline yêu cầu `initialization_method='random'` và `preserve_global_best=True`.
- `max_evaluations` nếu có phải đủ đánh giá quần thể ban đầu; time limit nếu có phải dương; seed không âm.
- Bài toán hiện tại là symmetric TSP có ít nhất 3 thành phố.

### 3.4.3. Điều kiện dừng và số lần đánh giá

Solver dừng khi đạt giới hạn thế hệ, evaluation budget, time limit hoặc nhận yêu cầu hủy. Nếu chạy đủ `G` thế hệ, số lần đánh giá là `N_c * m * (G + 1)`: một quần thể ban đầu cộng `G` thế hệ. Route trùng vẫn được tính nếu objective được gọi. Khi dừng giữa generation, chỉ trả nghiệm tốt nhất đã thấy; quần thể dở dang không được commit.

### 3.4.4. Benchmark EHO

Benchmark được chạy lại từ commit `4cb9947` trên Python 3.11.9, Windows 10: 4 clan × 20 voi, `alpha=0.7`, `beta=0.3`, một route separation mỗi clan, ngân sách 6.000 objective evaluations/run, năm seed `[11, 23, 37, 53, 71]`. Cả 35/35 lượt đều hợp lệ. Bảng ghi trung bình, độ lệch chuẩn mẫu, min–max và thời gian trung bình; thời gian phụ thuộc môi trường.

| Thành phố | Distance trung bình | Độ lệch chuẩn mẫu | Min–max | Evaluations/run | Runtime TB (s) |
|---:|---:|---:|---:|---:|---:|
| 3 | 6.0 | 0.00 | 6–6 | 6000 | 0.2084 |
| 4 | 189.0 | 0.00 | 189–189 | 6000 | 0.2190 |
| 6 | 1248.0 | 0.00 | 1248–1248 | 6000 | 0.2461 |
| 15 | 1668.8 | 90.97 | 1539–1796 | 6000 | 0.3340 |
| 26 | 1672.8 | 114.35 | 1509–1825 | 6000 | 0.4753 |
| 42 | 2015.2 | 55.00 | 1961–2107 | 6000 | 0.6211 |
| 48 | 103202.6 | 2035.52 | 100054–104711 | 6000 | 0.6793 |

Không có known optimum được xác minh cho các dataset này trong registry, nên bảng là kết quả quan sát, không phải khoảng cách tới optimum.

## 3.5. Nhận xét và giới hạn D-EHO

**Ưu điểm.** Các toán tử hoạt động trực tiếp trên route hoán vị và giữ nghiệm hợp lệ mà không cần repair. Clan archive và global best bảo tồn nghiệm tốt đã tìm thấy. Seed và evaluation budget giúp lặp lại, giới hạn các lần chạy.

**Hạn chế.** Guided-swap, Hamming medoid và separation ngẫu nhiên là phép thích nghi cho TSP, không phải phép biến đổi đại số tương đương EHO liên tục. Hamming medoid đo khác biệt theo vị trí thành phố chứ không theo cạnh của chu trình. EHO là heuristic nên không đảm bảo optimum toàn cục. Kết quả hiện tại dùng một cấu hình và năm seed; chưa đủ để suy rộng thứ hạng thuật toán.

**Phạm vi áp dụng.** Implementation phù hợp với symmetric TSP có ma trận hữu hạn, không âm, đối xứng, đường chéo bằng 0 và ít nhất ba thành phố. Mở rộng sang TSP bất đối xứng hoặc bài lớn cần điều chỉnh toán tử và kiểm tra bằng thí nghiệm mới.

# CHƯƠNG 4. CÁC KẾT QUẢ THỰC NGHIỆM

## 4.1. Thiết kế thí nghiệm

Repository có bảy ma trận gồm 3, 4, 6, 15, 26, 42 và 48 thành phố. Notebook khảo sát riêng các toán tử GA, độ phân tán qua nhiều seed, khởi tạo, adaptive mutation và 2-opt. Benchmark mới chạy GA và D-EHO độc lập trên cùng bảy ma trận, cùng năm seed `[11, 23, 37, 53, 71]` và giới hạn 6.000 objective evaluations cho mỗi lượt. Mỗi thuật toán có 35 lượt hợp lệ.

Các bảng thí nghiệm notebook giữ cấu hình và mục tiêu riêng của từng phép thử; không gộp kết quả chạy khác budget thành một so sánh trực tiếp. Các bảng benchmark ở Mục 4.5 mới là phép so sánh GA–D-EHO có cùng bộ dữ liệu, seed và ngân sách đánh giá. Runtime chỉ mô tả môi trường lần chạy, không phải bảo đảm tốc độ trên máy khác. Không có known optimum đã xác minh cho các ma trận này, vì vậy không kết luận optimum hoặc relative gap.

## 4.2. Kết quả so sánh operator trên bài 15 thành phố

Bảng chép lại thí nghiệm GA trong notebook với population 40, hai elites, tối đa 2.000 evaluations và năm seed. Độ lệch chuẩn là sample standard deviation.

| Biến thể | Distance trung bình | Trung vị | Độ lệch chuẩn mẫu |
|---|---:|---:|---:|
| GA mặc định (tournament + OX + inversion) | 1235.0 | 1225 | 43.86 |
| Rank selection | 1413.6 | 1402 | 81.79 |
| Roulette selection | 1400.8 | 1340 | 158.48 |
| PMX thay OX | 1275.4 | 1279 | 38.34 |
| Swap mutation | 1317.0 | 1289 | 113.40 |
| Insertion mutation | 1319.8 | 1287 | 68.16 |
| Scramble mutation | 1473.0 | 1391 | 152.78 |

Trong cấu hình và mẫu seed này, GA mặc định có mean thấp nhất trong các biến thể được thử. Năm seed chưa đủ để kết luận thứ hạng sẽ giữ nguyên trên dữ liệu hoặc cấu hình khác.

## 4.3. Độ phân tán kết quả trong notebook GA

Bảng sau tóm tắt thí nghiệm notebook đã lưu, dùng năm seed cho từng dataset. “Best observed” là kết quả tốt nhất trong mẫu, không phải optimum đã chứng minh.

| Số thành phố | Min | Mean | Median | Max | Độ lệch chuẩn mẫu | Tỷ lệ đạt min quan sát |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 6 | 6 | 6 | 6 | 0 | 100% |
| 6 | 1248 | 1248 | 1248 | 1248 | 0 | 100% |
| 15 | 1194 | 1200.2 | 1194 | 1225 | 13.86 | 80% |
| 26 | 969 | 1046 | 1034 | 1186 | 82.85 | 20% |
| 42 | 1102 | 1151.6 | 1133 | 1211 | 49.75 | 20% |
| 48 | 51215 | 55404.6 | 55339 | 59638 | 3031.79 | 20% |

Các bài nhỏ cho kết quả ổn định trong mẫu. Ở các bài lớn hơn, kết quả thay đổi theo seed. Tỷ lệ đạt min chỉ cho biết số lượt chạm min của mẫu hiện tại. Thí nghiệm liệt kê hoán vị trên bài nhỏ để kiểm tra độc lập giá trị route; phép liệt kê này không phải solver của ứng dụng.

## 4.4. Khởi tạo, adaptive mutation và 2-opt

Trong thí nghiệm notebook trên các bài 15, 26, 42 và 48 thành phố, mixed initialization và nearest-neighbor có mean thấp hơn control ở các mẫu đã lưu. Ví dụ trên bài 48, control mean là 55.404,6; mixed là 37.222,2; nearest-neighbor là 36.559,0. Đây là quan sát theo preset và seed của notebook, không phải bảo đảm tổng quát.

2-opt có mean kém control trong preset được ghi nhận. Trên bài 48, phép thử local search dùng trung bình 3.163,4/4.000 evaluations và chỉ commit khoảng 20,6 thế hệ, so với khoảng 104 thế hệ của control. Ngân sách cho các probe local search làm giảm ngân sách tạo thế hệ. Adaptive mutation cũng chỉ được đánh giá trong các preset và seed đã lưu, và không bật mặc định.

## 4.5. Benchmark GA và D-EHO trên bảy ma trận

Mỗi thuật toán được chạy năm seed trên mỗi dataset, tối đa 6.000 objective evaluations/run. Cả GA và D-EHO đều có 35/35 lượt hợp lệ. Runtime trung bình được đo trên cùng máy trong lần benchmark này.

| Thành phố | GA mean | GA SD | GA runtime (s) | D-EHO mean | D-EHO SD | D-EHO runtime (s) |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 6 | 0 | 0.0354 | 6 | 0 | 0.2084 |
| 4 | 189 | 0 | 0.0376 | 189 | 0 | 0.2190 |
| 6 | 1248 | 0 | 0.0401 | 1248 | 0 | 0.2461 |
| 15 | 1200.2 | 13.86 | 0.0510 | 1668.8 | 90.97 | 0.3340 |
| 26 | 1056.4 | 72.84 | 0.0661 | 1672.8 | 114.35 | 0.4753 |
| 42 | 1166.2 | 26.28 | 0.0862 | 2015.2 | 55.00 | 0.6211 |
| 48 | 54194.4 | 3861.50 | 0.0941 | 103202.6 | 2035.52 | 0.6793 |

Trong cấu hình thử này, GA có mean thấp hơn D-EHO ở các bài 15, 26, 42 và 48 thành phố; ba trường hợp nhỏ có cùng mean. Đây chỉ là kết quả của một bộ cấu hình, năm seed và ngân sách đã nêu. D-EHO có runtime cao hơn trong lần đo này; không nên khái quát sang phần cứng khác. Chi phí của các ma trận có thang khác nhau, nên chỉ so sánh GA với D-EHO trong cùng một hàng, không so mean giữa các dataset.

## 4.6. Kiểm tra mã nguồn và khả năng tái lập

Lần rà soát được thực hiện trên commit `4cb9947` bằng Python 3.11.9 trên Windows 10.

- `python -m compileall -q src`: thành công.
- Benchmark GA và D-EHO: mỗi thuật toán hoàn tất 35/35 lượt, mỗi lượt tối đa 6.000 evaluations.
- Repository có kiểm thử trong `tests/`, nhưng `pytest` chưa chạy được vì môi trường `.venv` hiện thiếu module `pytest`. Vì vậy không ghi nhận kết quả pass/fail cho test suite.
- Các giá trị benchmark là best-of-run theo ngân sách, không chứng minh nghiệm tối ưu toàn cục.

# CHƯƠNG 5. KẾT LUẬN

## 5.1. Kết quả đạt được

Repository hiện triển khai hai solver độc lập cho symmetric TSP: Genetic Algorithm và Discrete Elephant Herding Optimization. Chúng dùng chung biểu diễn route permutation, kiểm tra đầu vào và hàm mục tiêu tính tổng chi phí chu trình; mỗi thuật toán có vòng lặp và tham số riêng. CLI và GUI cho phép chọn GA hoặc EHO cho từng lượt chạy, nhưng chưa ghép hai thuật toán thành một solver lai.

GA cung cấp selection, crossover, mutation, nhiều cách khởi tạo, elitism và các điều kiện dừng. D-EHO có clan, matriarch, Hamming medoid, guided-swap, separation, archive nghiệm tốt và các giới hạn chạy. Benchmark cùng budget cho thấy GA có mean thấp hơn trên bốn bài lớn trong mẫu này; điều đó chưa đủ để tuyên bố GA luôn tốt hơn D-EHO.

## 5.2. Hạn chế và hướng phát triển

1. **Kiểm thử tự động:** test source có trong repository, nhưng cần cài `pytest` vào môi trường để chạy lại suite và báo cáo kết quả.
2. **Độ tin cậy thống kê:** benchmark hiện dùng năm seed và một cấu hình cho mỗi solver. Nên tăng số seed, thử nhiều cấu hình và báo cáo phân bố.
3. **Nghiệm tham chiếu:** các tên file gợi ý chi phí nhưng không thay thế known optimum có nguồn kiểm chứng. Chỉ báo cáo optimality gap khi có reference đáng tin cậy.
4. **Phạm vi TSP:** dữ liệu hiện dùng symmetric TSP. TSP bất đối xứng cần kiểm tra hợp đồng dữ liệu và đánh giá lại toán tử.
5. **Giới hạn D-EHO:** Hamming medoid đo khác biệt theo vị trí, không theo cạnh chu trình; guided-swap và separation là phép thích nghi rời rạc chứ không tương đương đại số với công thức EHO liên tục. EHO vẫn là heuristic, không bảo đảm optimum toàn cục.
6. **Chi phí tính toán:** D-EHO có runtime cao hơn GA trong batch hiện tại; cần profiling và thử nghiệm thêm trước khi chọn cấu hình triển khai.

Tóm lại, mã nguồn đáp ứng phạm vi đề tài ở mức có hai thuật toán TSP chạy được và benchmark được. Kết luận về thuật toán nào ưu việt hơn cần thêm thử nghiệm có kiểm soát và known optimum cho các bộ dữ liệu phù hợp.

# TÀI LIỆU THAM KHẢO

1. Holland, J. H. *Adaptation in Natural and Artificial Systems*. University of Michigan Press, 1975. Tài liệu nền tảng về cơ chế thích nghi và giải thuật di truyền.
2. Goldberg, D. E. *Genetic Algorithms in Search, Optimization, and Machine Learning*. Addison-Wesley, 1989. Tài liệu nhập môn về biểu diễn, selection, crossover và mutation trong GA.
3. Applegate, D. L., Bixby, R. E., Chvátal, V., và Cook, W. J. *The Traveling Salesman Problem: A Computational Study*. Princeton University Press, 2006. Tài liệu chuyên sâu về mô hình và phương pháp giải TSP.
4. Slowik, A. (Ed.). *Swarm Intelligence Algorithms: A Tutorial*. CRC Press, 2020, chương Elephant Herding Optimization, tr. in 150–161. Dùng làm nguồn mô tả thuật toán EHO nền; các toán tử rời rạc cho TSP được đối chiếu riêng với implementation của dự án.
5. Nhóm dự án, `docs/algorithm_ga.md`, `docs/experiments.md`, `docs/architecture.md`, `docs/source_attribution.md` và source trong `src/ga_eho_tsp/`. Các tài liệu này mô tả implementation, kết quả đã ghi nhận, hợp đồng dữ liệu và giới hạn hiện tại của repository.
6. File `AI FINAL PROJECT (1).docx` do người dùng cung cấp. Tài liệu được dùng để đối chiếu nội dung báo cáo hiện tại; nội dung trong báo cáo này được cập nhật theo source code của repository.

# PHỤ LỤC A. CÀI ĐẶT VÀ SỬ DỤNG GA

## A.1. Cài môi trường

Từ thư mục gốc repository, sử dụng Python 3.11 trở lên:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Nếu PowerShell chặn activate script, có thể gọi trực tiếp `.\.venv\Scripts\python.exe` thay cho `python`. Trên terminal Windows gặp lỗi không in được tiếng Việt hoặc mũi tên, thử đặt encoding cho phiên terminal:

```powershell
$env:PYTHONIOENCODING = "utf-8"
```

## A.2. Kiểm tra dataset

```powershell
python -m ga_eho_tsp.cli validate --dataset data/06Cities-1248.txt
```

Thông báo thành công cho biết tên bài toán, dimension, tính đối xứng, đường chéo 0 và tính hữu hạn. Nếu file sai định dạng hoặc ma trận không hợp lệ, CLI trả lỗi thay vì tự sửa dữ liệu.

## A.3. Chạy GA

```powershell
python -m ga_eho_tsp.cli solve `
  --algorithm ga `
  --dataset data/15Cities-1194.txt `
  --seed 42
```

CLI in thuật toán, distance, tour đóng vòng, seed, số iteration, evaluations, runtime và stopping reason. Với cấu hình mặc định, population là 80, generations/max iterations là 250, tournament size là 3, crossover là OX với rate 0.9, mutation là inversion với rate 0.15 và elitism giữ 2 cá thể. Có thể cung cấp thêm flags để chọn selection/crossover/mutation khác, initialization, evaluation/time budget, stagnation, adaptive mutation hoặc 2-opt. Các giá trị được kiểm tra qua `GAConfig`.

Ví dụ chọn PMX và mixed initialization, giới hạn 6.000 evaluations:

```powershell
python -m ga_eho_tsp.cli solve `
  --algorithm ga `
  --dataset data/48Cities-33523.txt `
  --seed 42 `
  --crossover-method pmx `
  --initialization-method mixed `
  --max-evaluations 6000 `
  --json outputs/ga-pmx.json
```

JSON lưu route lõi 0-based chưa lặp city 0 ở cuối. Giá trị distance đã gồm cạnh quay từ thành phố cuối về thành phố xuất phát.

## A.4. Chạy benchmark và kiểm tra lại

```powershell
python -m ga_eho_tsp.cli benchmark --config examples/ga_benchmark.json
```

Config ví dụ chạy bảy ma trận với năm seed và tối đa 6.000 evaluations mỗi run. Summary, CSV và JSON được ghi vào `outputs/benchmarks/ga-example/`. Dữ liệu output có thể được thay thế khi chạy lại cùng cấu hình; cần đổi `output_dir` nếu muốn giữ các batch khác nhau.

Repository có test trong `tests/`. Môi trường `.venv` của lần rà soát thiếu `pytest`; cài dependency này rồi mới chạy được suite:

```powershell
python -m pytest -q
```

Kết quả kiểm tra source và benchmark hiện tại được tóm tắt ở Mục 4.5–4.6.


# PHỤ LỤC B. CÀI ĐẶT VÀ SỬ DỤNG D-EHO

## B.1. Chạy EHO trên một dataset

```powershell
python -m ga_eho_tsp.cli solve `
  --algorithm eho `
  --dataset data/15Cities-1194.txt `
  --seed 42 `
  --max-evaluations 6000
```

Tham số chính gồm `--clan-count`, `--elephants-per-clan`, `--alpha`, `--beta` và `--separation-count`. Có thể thêm `--json` để lưu kết quả.

## B.2. Chạy benchmark EHO

```powershell
python -m ga_eho_tsp.cli benchmark --config examples/eho_benchmark.json
```

Cấu hình mẫu chạy bảy ma trận với năm seed và tối đa 6.000 evaluations mỗi lượt. Benchmark ghi summary, CSV và JSON trong thư mục output đã cấu hình. Đổi `output_dir` nếu cần giữ nhiều batch benchmark.
