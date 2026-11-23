# BỘ GIÁO DỤC VÀ ĐÀO TẠO
# ĐẠI HỌC KINH TẾ TP HỒ CHÍ MINH (UEH)
# TRƯỜNG CÔNG NGHỆ VÀ THIẾT KẾ

---

<div align="center">

![UEH CTD Logo](https://via.placeholder.com/200x200.png?text=College+of+Technology+and+Design)

# ĐỒ ÁN MÔN HỌC

## ỨNG DỤNG THUẬT TOÁN GENETIC ALGORITHM VÀ ELEPHANT HERDING OPTIMIZATION CHO BÀI TOÁN NGƯỜI DU LỊCH

### (Application of Genetic Algorithm and Elephant Herding Optimization for Traveling Salesman Problem - TSP)

---

**Học Phần:** Trí Tuệ Nhân Tạo (Artificial Intelligence)

**Danh Sách Nhóm:**

1. TRƯƠNG THÀNH ĐẠT - Trưởng nhóm
2. NGUYỄN TẤN KHIÊM  
3. NGUYỄN PHƯƠNG CHINH
4. LẠI THÀNH ĐẠT

**Chuyên Ngành:** CÔNG NGHỆ THÔNG TIN

**Khóa:** K50

**Giảng Viên Hướng Dẫn:** TS. Đặng Ngọc Hoàng Thành

**TP. Hồ Chí Minh, ngày 30 tháng 10 năm 2024**

</div>

---



**BỘ GIÁO DỤC VÀ ĐÀO TẠO ĐẠI HỌC KINH TẾ TP HỒ CHÍ MINH (UEH) TRƯỜNG CÔNG NGHỆ VÀ THIẾT KẾ** 



<!-- Start of picture text -->
College of<br>Technology<br>n ign<br>UNIveRsITY (274 Desig<br><!-- End of picture text -->

# **ĐỒ ÁN MÔN HỌC** 

**ĐỀ TÀI** 

**Ứng dụng Thuật toán Genetic Algorithm và Elephant Herding Optimization cho Bài toán Người Du Lịch (Traveling Salesman Problem - TSP)** 

**Học Phần: Trí Tuệ Nhân Tạo Danh Sách Nhóm** : 

**1.** TRƯƠNG THÀNH ĐẠT 

**2.** NGUYỄN TẤN KHIÊM 

**3.** NGUYỄN PHƯƠNG CHINH 

**4.** LẠI THÀNH ĐẠT 

**Chuyên Ngành** : CÔNG NGHỆ THÔNG TIN **Khóa** : K50 **Giảng Viên** : TS. Đặng Ngọc Hoàng Thành f TP. Hé Chi Minh , ngay 30thang 10 nam 20267 

## **MỤC LỤC** 

|**MỤC LỤC..................................................................................................................... 2**<br>|
|---|
|**CHƯƠNG 1. TỔNG QUAN.........................................................................................4**|
|1.1. Giới thiệu bài toán người du lịch....................................................................... 4|
|1.2. Phát biểu bài toán...............................................................................................5<br>|
|1.3. Độ phức tạp và lý do sử dụng thuật toán tìm kiếm............................................ 6<br>|
|1.4. Hướng tiếp cận giải quyết.................................................................................. 6|
|**CHƯƠNG 2. GIẢI THUẬT DI TRUYỀN................................................................. 8**|
|2.1. Giới thiệu về Genetic Algorithm........................................................................8|
|2.2. Cách áp dụng GA cho bài toán TSP...................................................................9|
|2.2.1. Luồng xử lý tổng quát................................................................................9|
|a) Random initialization (mặc định)............................................................ 10|
|b) Nearest-neighbor initialization (tùy chọn)...............................................11|
|c) Mixed initialization (tùy chọn).................................................................11|
|a) Tournament Selection (mặc định)............................................................12|
|b) Rank Selection (tùy chọn)........................................................................12|
|c) Roulette Wheel Selection (tùy chọn)....................................................... 12|
|a) Order Crossover - OX (mặc định)............................................................13|
|b) Partially Mapped Crossover - PMX (tùy chọn).......................................15<br>|
|2.2.5. Đột biến................................................................................................... 15|
|a) Inversion Mutation (mặc định)................................................................ 16|
|b) Swap Mutation (tùy chọn)....................................................................... 17|
|c) Insertion Mutation (tùy chọn).................................................................. 17|
|d) Scramble Mutation (tùy chọn)................................................................. 17|
|2.2.7. Điều kiện dừng và lịch sử........................................................................18|
|a) Stagnation Stopping................................................................................. 20|
|b) Adaptive Mutation................................................................................... 20|
|c) Bounded 2-opt Local Search....................................................................21<br>|
|2.2.9. Tổ chức mã nguồn................................................................................... 22|
|**CHƯƠNG 3. THUẬT TOÁN ELEPHANT HERDING OPTIMIZATION..........23**|
|3.1. Tổng quan về Elephant Herding Optimization................................................ 23|
|3.1.1. Khái niệm EHO....................................................................................... 23|
|3.1.2. Nguyên lý hành vi đàn voi.......................................................................23|
|3.1.3. Các thành phần chính của EHO...............................................................23|
|3.2. Áp dụng EHO cho bài toán TSP...................................................................... 24|
|3.2.1. Biểu diễn nghiệm và hàm mục tiêu...............................................................25|
|3.2.2. Phân chia quần thể thành các Clan................................................................25|
|3.2.3. Cập nhật Matriarch........................................................................................26|



|3.2.4. Di chuyển voi thường (Clan Updating Operator)......................................... 27|
|---|
|3.2.5. Tách đàn (Separating Operator).................................................................... 28|
|3.2.6. Cơ chế bảo tồn nghiệm tốt nhất (Elitism)..................................................... 29|
|3.3. Quy trình hoạt động của D-EHO......................................................................31<br>|
|3.3.1. Sơ đồ luồng thuật toán.............................................................................31|
|3.3.2. Giả mã (Pseudocode)...............................................................................31<br>|
|3.3.3. Giải thích quá trình cập nhật một thế hệ..................................................32|
|3.4. Triển khai thuật toán trong chương trình..........................................................32<br>|
|3.4.1. Cấu trúc các module................................................................................ 32<br>|
|3.4.2. Các tham số cấu hình...............................................................................34|
|3.4.3. Điều kiện dừng và quản lý đánh giá........................................................ 34|
|3.5. Nhận xét và giới hạn của D-EHO.................................................................... 35|
|3.5.1. Ưu điểm................................................................................................... 35|
|3.5.2. Hạn chế.................................................................................................... 35|
|3.5.3. Khả năng áp dụng cho TSP..................................................................... 36|
|**CHƯƠNG 3. CÁC KẾT QUẢ THỰC NGHIỆM.................................................... 37**|
|3.1. Thiết kế thực nghiệm........................................................................................37|
|3.1.1. Bộ dữ liệu................................................................................................ 37|
|3.1.2. Cấu hình thực nghiệm..............................................................................37|
|3.2. Kết quả so sánh toán tử trên bài 15 thành phố................................................. 38|
|3.3. Phân phối kết quả theo kích thước bài toán..................................................... 39|
|3.4. Khởi tạo nâng cao, Adaptive Mutation và 2-opt..............................................40|
|3.5. Benchmark trên bảy bộ dữ liệu........................................................................ 42|
|**CHƯƠNG 4. KẾT LUẬN.......................................................................................... 44**|
|4.1. Các kết quả đạt được........................................................................................44|
|4.2. Những hạn chế và hướng phát triển................................................................. 44<br>|
|**TÀI LIỆU THAM KHẢO..........................................................................................45**|
|**PHỤ LỤC.....................................................................................................................46**|



## **CHƯƠNG 1. TỔNG QUAN** 

### **1.1. Giới thiệu bài toán người du lịch** 

Bài toán người du lịch (Traveling Salesman Problem - TSP) là một trong những bài toán tối ưu tổ hợp được nghiên cứu nhiều nhất trong khoa học máy tính và toán học rời rạc. Bài toán mô tả tình huống một người cần đi thăm một tập thành phố, mỗi thành phố được thăm đúng một lần, bắt đầu và kết thúc tại cùng một điểm xuất phát. Mục tiêu là xác định thứ tự thăm sao cho tổng chi phí di chuyển của toàn bộ chuyến đi là nhỏ nhất. 

TSP có ứng dụng thực tiễn rộng rãi: lập lịch phân phối hàng hóa, định tuyến mạch in điện tử (PCB drilling), lập kế hoạch sản xuất, định tuyến robot công nghiệp và nhiều bài toán quy hoạch khác, trong đó mục tiêu là tìm chu trình ngắn nhất qua một tập điểm cho trước. 

Trong đồ án này, chi phí di chuyển giữa các thành phố được biểu diễn bằng ma trận khoảng cách đối xứng. Phần tử tại hàng i, cột j của ma trận chứa chi phí đi từ thành phố i đến thành phố j. Vì tính đối xứng, chi phí đi từ i đến j bằng chi phí đi từ j về i, tức là chúng ta đang giải **Symmetric TSP** . 



<!-- Start of picture text -->
2<br>1<br>1<br>Origin<br>1<br>7 5<br><——_——_®<br>3<br><!-- End of picture text -->

_Hình 1.1 - Ví dụ bài toán TSP với 5 thành phố_ 

Hình 1.1 minh họa một bài TSP nhỏ với 5 thành phố. Mỗi nút tròn biểu diễn một thành phố, các mũi tên thể hiện hành trình được chọn với khoảng cách tương ứng 

ghi trên mỗi cạnh. Mục tiêu là tìm chu trình đi qua tất cả 5 thành phố với tổng khoảng cách nhỏ nhất. 

### **1.2. Phát biểu bài toán** 

**Đầu vào:** Tập thành phố 𝑉= 0, 1, ..., 𝑛−1 và ma trận khoảng cách  kích thước 𝐷 𝑛× 𝑛, trong đó 𝐷𝑖𝑗 là chi phí đi từ thành phố  đến thành phố . 𝑖 𝑗 

**Điều kiện:** Ma trận  phải thỏa mãn: 𝐷 

- Vuông: kích thước 𝑛× 𝑛 với 𝑛≥3 

- Đường chéo bằng 0: 𝐷𝑖𝑖 = 0 

- Đối xứng: 𝐷𝑖𝑗 = 𝐷𝑗𝑖 

- Các phần tử hữu hạn và không âm 

**Biểu diễn nghiệm:** Một hành trình hợp lệ là hoán vị  của tất cả thành phố, với quy π ước π[0] = 0 (cố định thành phố 0 làm điểm xuất phát). Trong hệ thống, route được lưu dưới dạng tuple số nguyên 0-based, ví dụ (0, 3, 2, 1) cho bài toán 4 thành phố. 

**Hàm mục tiêu:** Chi phí của hành trình  được tính là: π 



Trong đó số hạng cuối 𝐷[π[𝑛−1], π[0]] là chi phí quay trở về thành phố xuất phát, tạo thành chu trình khép kín. Hàm này được cài đặt trong domain/objective.py thông qua route_length, sử dụng math.fsum để tích lũy chính xác: 

Python def route_length(route: Sequence[int], matrix: Matrix) -> float: """Tính từng cạnh và cạnh cuối về 0 đúng một lần; không sửa input.""" validate_route(route, len(matrix)) try: total = fsum(matrix[route[i]][route[(i+1) % len(route)]] for i in range(len(route))) except OverflowError as error: raise ValueError("Tổng khoảng cách vượt miền số hữu hạn.") from error if not isfinite(total): raise ValueError("Tổng khoảng cách vượt miền số hữu hạn.") return total * **Mục tiêu:** Tìm π sao cho 𝐿(π*) là nhỏ nhất trong tất cả các hoán vị hợp lệ: 

π* = arg min 𝐿(π) π 

Một nghiệm  được xem là hợp lệ khi thỏa mãn đồng thời ba điều kiện: π 

1. Có đúng  phần tử 𝑛 

2. Bắt đầu bằng thành phố 0 

3. Mỗi thành phố từ  đến 0 𝑛−1 xuất hiện đúng một lần 

### **1.3. Độ phức tạp và lý do sử dụng thuật toán tìm kiếm** 

TSP thuộc lớp bài toán NP-Hard. Số lượng hành trình phân biệt với  thành phố 𝑛 (khi cố định điểm xuất phát) là (𝑛−1)!. Với 𝑛= 10 đã có 9! = 362. 880 hoán 17 vị, với 𝑛= 20 con số này vượt 1, 2 × 10 . Liệt kê toàn bộ hành trình để tìm nghiệm tối ưu là điều không khả thi trong thực tế với các bài toán kích thước trung bình trở lên. 

Bảng dưới đây minh họa sự tăng trưởng bùng nổ của không gian tìm kiếm: 

|**Số thành phố ( )**<br>𝑛|**Số hành trình**<br>(𝑛−1)!|
|---|---|
|3|2|
|6|120|
|10|362.880|
|15|87.178.291.200|
|20|1, 2 × 10<br>17|
|26|≈1, 6 × 10<br>25|



Vì vậy, các phương pháp heuristic và metaheuristic, trong đó có Genetic Algorithm và Elephant Herding Optimization được dùng để tìm nghiệm đủ tốt trong thời gian hợp lý, thay vì nghiệm tối ưu tuyệt đối. 

### **1.4. Hướng tiếp cận giải quyết** 

Đồ án triển khai hai thuật toán metaheuristic để giải TSP: 

- **Genetic Algorithm (GA):** Mô phỏng quá trình tiến hóa tự nhiên, duy trì một quần thể gồm nhiều hành trình ứng viên, chọn lọc các cá thể tốt, kết hợp chúng để tạo thế hệ mới và áp dụng đột biến để khám phá vùng tìm kiếm mới. GA đã được triển khai đầy đủ trong dự án. 

- **Elephant Herding Optimization (EHO):** Mô phỏng hành vi đàn voi, chia quần thể thành các clan, cập nhật vị trí mỗi voi theo matriarch (cá thể tốt nhất trong clan) và tách các voi đực kém nhất khỏi clan. Phần EHO đang trong giai đoạn phát triển. 

Cả hai thuật toán dùng chung biểu diễn route, hàm mục tiêu TSPProblem.route_length, cơ chế seed và cấu trúc kết quả RunResult được định nghĩa trong domain/. 

## **CHƯƠNG 2. GIẢI THUẬT DI TRUYỀN** 

### **2.1. Giới thiệu về Genetic Algorithm** 

Genetic Algorithm (GA) là một lớp thuật toán tìm kiếm và tối ưu được Holland giới thiệu vào những năm 1970, lấy cảm hứng từ quá trình tiến hóa sinh học theo thuyết chọn lọc tự nhiên của Darwin. Thay vì chỉ duy trì một nghiệm duy nhất, GA duy trì một quần thể (population) gồm nhiều nghiệm ứng viên, gọi là cá thể (individual). Trong mỗi vòng lặp (generation), thuật toán: 

1. **Đánh giá** chất lượng (fitness) của từng cá thể 

2. **Chọn lọc** các cá thể tốt làm cha mẹ (selection) 

3. **Lai ghép** (crossover) để tạo cá thể con kế thừa đặc điểm của cha mẹ 

4. **Đột biến** (mutation) để duy trì sự đa dạng và khám phá vùng mới 

5. **Hình thành** quần thể thế hệ tiếp theo 

Ưu điểm của GA so với tìm kiếm cục bộ đơn giản là khả năng khám phá không gian tìm kiếm song song từ nhiều hướng khác nhau, giảm nguy cơ mắc kẹt tại nghiệm cục bộ. GA cũng linh hoạt vì không yêu cầu hàm mục tiêu có tính khả vi. 

Một điểm khác biệt quan trọng khi áp dụng GA cho TSP là biểu diễn cá thể. Biểu diễn bit nhị phân thông thường không phù hợp vì một hành trình TSP phải là hoán vị, không được phép lặp hoặc bỏ sót thành phố. Dự án dùng permutation representation: mỗi cá thể là một tuple chứa đầy đủ  thành phố, với quy ước thành 𝑛 phố 0 luôn đứng đầu. Các toán tử crossover và mutation chỉ thao tác trên phần tail (phần route từ vị trí 1 trở đi) để không làm mất tính hợp lệ của hoán vị. 

#### **Sơ đồ tổng quát của Genetic Algorithm:** 



### **2.2. Cách áp dụng GA cho bài toán TSP** 

## **2.2.1. Luồng xử lý tổng quát** 

Vòng lặp GA được cài đặt tập trung trong algorithms/ga/solver.py. Quy trình một lần chạy hoàn chỉnh gồm các bước chính như sau: 

1. **Kiểm tra đầu vào:** Xác nhận TSPProblem và GAConfig hợp lệ, bao gồm kiểm tra giới hạn tham số, ma trận khoảng cách và ngân sách tính toán. 

2. **Khởi tạo quần thể:** Tạo population_size route ban đầu theo phương thức đã chọn (ngẫu nhiên, nearest-neighbor hoặc mixed). Mỗi route là hoán vị hợp lệ với thành phố 0 đứng đầu. 

3. **Đánh giá khởi tạo:** Tính chi phí cho toàn bộ quần thể ban đầu bằng TSPProblem.route_length, đếm số lần đánh giá và lưu global best. 

4. **Ghi snapshot ban đầu (iteration 0):** IterationStat lưu best trong quần thể hiện tại, global best, mean fitness, số evaluations, thời gian và diversity. 

5. **Vòng lặp thế hệ:** Với mỗi thế hệ, kiểm tra điều kiện dừng, sao chép elites, chuẩn bị selection, chọn cha mẹ, lai ghép, đột biến, đánh giá con, áp dụng local search nếu được bật, cập nhật global best. 

6. **Commit thế hệ:** Chỉ commit khi quần thể mới đầy đủ population_size cá thể. Nếu dừng giữa thế hệ, các candidate đã được đánh giá vẫn được tính vào global best nhưng quần thể dở dang không được commit. 

7. **Trả kết quả:** RunResult chứa global best của toàn bộ lần chạy (không chỉ route tốt nhất trong quần thể cuối). 

#### **Pseudocode vòng lặp GA:** 

Python kiểm tra problem và config rng = Random(config.seed) population = khởi_tạo(population_size, rng) costs = [route_length(r) for r in population] best_route, best_distance = best(population, costs) ghi snapshot iteration=0 

for iteration in 1..min(generations, max_iterations): kiểm tra stop / time_limit / max_evaluations 

next_pop, next_costs = select_elites(population, costs, elite_count) selector = prepare_selection(population, costs, method, k) rate = effective_mutation_rate(config, stagnation, diversity) while len(next_pop) < population_size: kiểm tra stop 

p1, p2 = selector.pick(rng), selector.pick(rng) children = crossover(p1, p2, rng) if rng.random() < crossover_rate else (p1, p2) for child in children: child = mutate(child, rate, rng, mutation_method) cost = route_length(child)        # evaluations++ cập nhật best_route, best_distance if local_search_enabled: child, cost = improve(child, cost, ...) next_pop.append(child) commit: population, costs = next_pop, next_costs cập nhật stagnation, ghi history kiểm tra STAGNATION ghi snapshot cuối trả RunResult(best_route, best_distance, ...) 

#### **Sơ đồ kiến trúc module:** 



## **2.2.2. Khởi tạo quần thể và seed** 

Module algorithms/ga/initialization.py cung cấp ba phương thức khởi tạo: 

## **a) Random initialization (mặc định)** 

Mỗi route được sinh bằng cách tạo hoán vị ngẫu nhiên của  thành phố, sau đó xoay 𝑛 để thành phố 0 đứng đầu. Toàn bộ quá trình dùng rng riêng của lần chạy, không ảnh hưởng RNG toàn cục, đảm bảo tái lập kết quả khi giữ nguyên seed. 

Python def nearest_neighbor(problem: TSPProblem, start: int) -> Route: """Tham lam từ start, tie theo city nhỏ nhất; rotate để city 0 đứng đầu.""" remaining = set(range(problem.dimension)) remaining.remove(start) route = [start] 

while remaining: row = problem.distance_matrix[route[-1]] city = min(remaining, key=lambda candidate: (row[candidate], candidate)) route.append(city) remaining.remove(city) zero = route.index(0) return tuple(route[zero:] + route[:zero]) def initialize( dimension: int, population_size: int, rng: Random, *, problem: TSPProblem | None = None, method: str = "random", nn_seed_fraction: float = 0.25, ) -> list[Route]: """Random mặc định; NN đa start hoặc mixed floor(P×fraction), không ép unique.""" if method == "random": return [random_permutation(dimension, rng) for _ in range(population_size)] ... count = population_size if method == "nearest_neighbor" else int(population_size * nn_seed_fraction) routes: list[Route] = [] while len(routes) < count: starts = rng.sample(range(dimension), dimension) for start in starts[:count-len(routes)]: routes.append(nearest_neighbor(problem, start)) routes.extend(random_permutation(dimension, rng) for _ in range(population_size-count)) return routes 

## **b) Nearest-neighbor initialization (tùy chọn)** 

Thuật toán tham lam: bắt đầu từ một thành phố, tại mỗi bước chọn thành phố chưa thăm gần nhất (nếu bằng nhau thì chọn thành phố có chỉ số nhỏ hơn). Mỗi route NN được sinh từ một điểm bắt đầu khác nhau, tránh nhân bản một route duy nhất. 

## **c) Mixed initialization (tùy chọn)** 

Kết hợp một phần route NN (tỷ lệ nn_seed_fraction, mặc định 25%) và phần còn lại là random. Phương án này đặt một số nghiệm chất lượng tốt vào quần thể ban đầu trong khi vẫn giữ sự đa dạng. 

#### **Sơ đồ ba phương thức khởi tạo:** 



## **2.2.3. Chọn cha mẹ** 

Module algorithms/ga/selection.py cài đặt ba phương pháp selection, tất cả đều hỗ trợ minimization (chi phí nhỏ hơn = tốt hơn). Distribution của rank và roulette được chuẩn bị một lần mỗi thế hệ thông qua prepare_selection, rồi dùng nhiều lần để chọn cha mẹ, tránh tính lại và đảm bảo nhất quán trong một thế hệ. 

## **a) Tournament Selection (mặc định)** 

Lấy ngẫu nhiên tournament_size cá thể (mặc định 𝑘= 3), chọn cá thể có chi phí thấp nhất trong nhóm. Hai lần chọn cha mẹ độc lập nhau; cùng một route có thể được chọn hai lần. 

Python def pick(self, rng: Random) -> Route: if self.method == "tournament": indices = rng.sample(range(len(self.population)), self.tournament_size) return self.population[min(indices, key=lambda index: self.costs[index])] 

## **b) Rank Selection (tùy chọn)** 

Sắp xếp cá thể từ tốt đến kém, gán trọng số 𝑃, 𝑃−1, ..., 1 theo thứ hạng. Cách này làm giảm áp lực chọn lọc khi có vài cá thể vượt trội, giúp duy trì đa dạng quần thể. 

## **c) Roulette Wheel Selection (tùy chọn)** 

Chuyển chi phí thành trọng số bằng công thức weight_i = 1 - cost_i / max_cost. Cá thể có chi phí thấp hơn có trọng số cao hơn và xác suất được chọn lớn hơn. Trường 

hợp đặc biệt (tất cả chi phí bằng nhau hoặc max_cost = 0) được xử lý bằng cách chọn đều. 

#### **Sơ đồ ba phương pháp selection:** 



<!-- Start of picture text -->
Lay k ca thé<br>tournament ngau nhién<br>Chon min cost<br>Sp xép theo<br>Selection cost<br>Method i>} Trong séoy  P,A  P-1, >CaAG thé cha me<br>Chon theo trong<br>sé<br>weight_i=1-<br>cost_i/max<br>roulette_wheel———_—_—_—_—___» Chonon theosotheo trongtro<br>(xi ly all-zero<br>dc biét)<br><!-- End of picture text -->

## **2.2.4. Lai ghép permutation** 

Module algorithms/ga/crossover.py cài đặt hai toán tử lai ghép. Cả hai đều chỉ thao tác trên phần tail (vị trí 1 trở đi), không đổi vị trí thành phố 0, đảm bảo con sinh ra là permutation hợp lệ. 

#### **a) Order Crossover - OX (mặc định)** 

OX bảo tồn thứ tự tương đối của các thành phố từ cha mẹ. Thuật toán: 

1. Chọn ngẫu nhiên hai vị trí cắt left, right trên tail 

2. Sao chép đoạn [left:right] từ cha thứ nhất sang con ở cùng vị trí 

3. Duyệt cha thứ hai theo thứ tự vòng (bắt đầu ngay sau vị trí right), bỏ các thành phố đã có 

4. Điền các thành phố còn lại vào các vị trí trống của con theo thứ tự vòng 

Python 

def order_crossover(parent1: Route, parent2: Route, rng: Random) -> tuple[Route, Route]: 

"""OX hai điểm trên tail; fill vòng từ sau đoạn cắt; parent bất biến.""" 

a, b = parent1[1:], parent2[1:] left, right = sorted(rng.sample(range(len(a)), 2)) right += 1 def child(first: Route, second: Route) -> Route: result = [-1] * len(first) result[left:right] = first[left:right] used = set(first[left:right]) values = [city for city in second[right:] + second[:right] if city not in used] positions = list(range(right, len(first))) + list(range(left)) for position, value in zip(positions, values): result[position] = value return (0, *result) return child(a, b), child(b, a) 

Ví dụ minh họa OX: 

||**0**|**1**|**2**|**3**|**4**|**5**|**6**|
|---|---|---|---|---|---|---|---|
|**Cha 1**|0|1|2|3|4|5|6|
|**Cha 2**|0|4|1|6|2|5|3|
|**Cha 3**|0|6|2|3|4|5|1|



_(Đoạn giữ lại từ Cha 1: vị trí 1-2, điền từ Cha 2 theo thứ tự vòng)_ 

_Hình 2.1 - Minh họa toán tử Order Crossover (OX)_ 

#### **b) Partially Mapped Crossover - PMX (tùy chọn)** 

PMX dùng ánh xạ giữa đoạn của hai cha mẹ để giải quyết xung đột thành phố: 

1. Giữ đoạn [left:right] từ cha thứ nhất ở cùng vị trí trong con 

2. Với mỗi thành phố của cha thứ hai nằm ngoài đoạn, theo chuỗi ánh xạ cho đến khi tìm được thành phố chưa có trong đoạn giữ 

Python def partially_mapped_crossover( parent1: Route, parent2: Route, rng: Random ) -> tuple[Route, Route]: """PMX trên tail: giữ segment, giải collision bằng chuỗi ánh xạ A `→` B.""" first, second = parent1[1:], parent2[1:] left, right = sorted(rng.sample(range(len(first)), 2)) right += 1 def child(kept: Route, donor: Route) -> Route: result = list(donor) result[left:right] = kept[left:right] mapping = dict(zip(kept[left:right], donor[left:right])) for index in (*range(left), *range(right, len(kept))): city = donor[index] while city in mapping: city = mapping[city] result[index] = city return (0, *result) return child(first, second), child(second, first) 

## **2.2.5. Đột biến** 

Module algorithms/ga/mutation.py cài đặt bốn toán tử đột biến. Đột biến được áp dụng với một xác suất Bernoulli trên mỗi cá thể con, không phải trên từng thành phố, nên mutation_rate có cùng ý nghĩa giữa các phương pháp. Mọi toán tử đều giữ thành phố 0 đứng đầu và không làm thay đổi route cha (immutable parent). 

Python def mutate(route: Route, rate: float, rng: Random, method: str = "inversion") -> Route: """Một xác suất/cá thể; đảo đoạn gồm cả hai đầu, không sửa parent.""" if rng.random() >= rate: return tuple(route) result = list(route) i, j = rng.sample(range(1, len(route)), 2) if method == "swap": result[i], result[j] = result[j], result[i] elif method == "insertion": result.insert(j, result.pop(i)) else: i, j = sorted((i, j)) segment = result[i:j+1] if method == "inversion": segment.reverse() else:  # scramble rng.shuffle(segment) result[i:j+1] = segment return tuple(result) 

#### **a) Inversion Mutation (mặc định)** 

Chọn ngẫu nhiên hai vị trí trên tail, đảo ngược thứ tự của đoạn giữa hai vị trí đó (kể cả hai đầu). 

_Hình 2.2 - Minh họa toán tử Inversion Mutation_ 

Ví dụ Inversion: Route (0, 1, 2, 3, 4, 5, 6), chọn vị trí 2 và 5 → đảo đoạn [2, 3, 4, 5] → kết quả (0, 1, 5, 4, 3, 2, 6) 

#### **b) Swap Mutation (tùy chọn)** 

Chọn ngẫu nhiên hai vị trí khác nhau trên tail và hoán đổi hai thành phố tại hai vị trí đó. 

#### **c) Insertion Mutation (tùy chọn)** 

Lấy thành phố tại vị trí i ra khỏi route, rồi chèn vào vị trí j (vị trí mới sau khi pop). Thao tác này di chuyển một thành phố đến vị trí mới trong hành trình. 

#### **d) Scramble Mutation (tùy chọn)** 

Chọn ngẫu nhiên một đoạn trên tail rồi xáo trộn thứ tự các thành phố trong đoạn đó bằng Fisher-Yates shuffle. 

#### **Sơ đồ so sánh bốn phương pháp đột biến:** 



<!-- Start of picture text -->
Chon i, j ngau<br>nhién<br>Dao ngudc<br>route[i..j]<br>inversion<br>Chon i, j ngau<br>aep————_—_> Hoaneatdéihiénroute[i]5<br>= route[j]<br>Mutation q Route con<br>Method 4 d6t bién<br>Chon i, j ngau<br>» 5 nhién<br>bey > Pop route[i],<br>insert tai j<br>scramble<br>Chon i, j ngau<br>nhién<br>Shuffle<br>routefi..j]<br><!-- End of picture text -->

**2.2.6. Elitism và global best** 

Elitism là cơ chế bảo tồn elite_count cá thể tốt nhất của quần thể hiện tại, sao chép trực tiếp sang quần thể kế tiếp cùng với fitness đã biết (không đánh giá lại). Module algorithms/ga/survivor.py cài đặt việc này: 

Python def select_elites(population: list[Route], costs: list[float], count: int) -> tuple[list[Route], list[float]]: """Giữ count index tốt nhất, thứ tự tie ổn định; tái dùng fitness.""" indices = sorted(range(len(population)), key=lambda i: costs[i])[:count] return [population[i] for i in indices], [costs[i] for i in indices] 

Điểm quan trọng: fitness không được gán lại về 0 khi sao chép elites — điều đó sẽ làm sai thứ tự minimization. Kích thước quần thể luôn được duy trì đủ population_size cá thể ngay cả khi population_size là số lẻ. 

Global Best Archive là cơ chế riêng biệt với elitism. Mỗi lần một route con được đánh giá (kể cả trong phần route chưa commit), nếu chi phí nhỏ hơn global best hiện tại thì archive được cập nhật ngay lập tức. Kết quả cuối cùng là global best của toàn bộ lần chạy, không phải chỉ trong quần thể cuối. Đây là thiết kế quan trọng: ngay cả khi thuật toán bị dừng giữa một thế hệ, nghiệm tốt nhất từng gặp vẫn được giữ lại. 

Python def evaluate_candidate(route: tuple[int, ...]) -> float: nonlocal evaluations, best_route, best_distance cost = problem.route_length(route) evaluations += 1 if cost < best_distance: best_route, best_distance = route, cost return cost 

## **2.2.7. Điều kiện dừng và lịch sử** 

GA kiểm tra các điều kiện dừng tại các điểm an toàn (cooperative stopping), không phải hard real-time: 

|**Điều kiện dừng**|**stopping_reason**|**Mô tả**|
|---|---|---|
|Hết số generation|MAX_ITERATIONS|Đạt min(generations,<br>max_iterations) thế hệ<br>hoàn chỉnh|
|Hết ngân sách đánh giá|MAX_EVALUATIONS|Tổng lần gọi route_length<br>≥ max_evaluations|
|Hết thời gian|TIME_LIMIT|Thời gian thực tế ≥<br>time_limit_seconds|
|Yêu cầu dừng|CANCELLED|stop_requested() trả True|
|Trì trệ|STAGNATION|stagnation_patience thế hệ<br>liên tiếp không cải thiện<br>global best|



Lưu ý: max_evaluations phải đủ ít nhất cho quần thể ban đầu (tức ≥ population_size). Điều kiện STAGNATION chỉ hoạt động khi được bật tường minh trong cấu hình. 

#### **Cấu trúc lịch sử (RunResult và IterationStat):** 

Mỗi snapshot lịch sử (IterationStat) lưu: iteration, best_current (best trong quần thể đã commit), best_so_far (global best), mean_fitness, evaluations tích lũy, elapsed_seconds và population_diversity. record_history_every kiểm soát tần suất ghi snapshot trung gian. Luôn có snapshot iteration=0 (sau khởi tạo) và snapshot cuối (khi kết thúc). 

#### **Sơ đồ điều kiện dừng:** 



<!-- Start of picture text -->
Kiém tra<br>diéu kién ding<br>stop_requeste hong cé<br>evaluations >= max_eviteration >= cap<br>lapsed>=time limit tagnation >=_<br>CANCELLED TIME_LIMIT MAX_EVALUATIONS MAX_ITERATIONS STAGNATION C ey<br>a ~<br>( diing, tea<br>{. Rungesutt<br>\<br><!-- End of picture text -->

## **2.2.8. Các phương án nâng cao** 

Ngoài pipeline mặc định, dự án cài đặt thêm một số tính năng tùy chọn: 

#### **a) Stagnation Stopping** 

Dừng thuật toán sớm khi quần thể không cải thiện global best trong stagnation_patience thế hệ liên tiếp. Biến stagnation được reset về 0 mỗi khi global best cải thiện và tăng thêm 1 sau mỗi thế hệ đầy đủ không cải thiện. 

#### **b) Adaptive Mutation** 

Điều chỉnh mutation rate động theo mức trì trệ và diversity của quần thể. Module algorithms/ga/monitoring.py cài đặt hai hàm: 

Python def population_diversity(population: list[Route]) -> float: """(unique symmetric tours−1)/(P−1); route đảo chiều được coi tương đương.""" if len(population) <= 1: return 0.0 canonical = {min(route, (0, *route[:0:-1])) for route in population} return (len(canonical)-1) / (len(population)-1) 

def effective_mutation_rate(config: GAConfig, stagnation: int, diversity: float) -> float: """Tăng tuyến tính theo stagnation; diversity≤0.1 đặt pressure tối thiểu 0.5.""" if not config.adaptive_mutation: return config.mutation_rate base = min(config.adaptive_max_rate, max(config.adaptive_min_rate, config.mutation_rate)) pressure = min(1.0, stagnation / config.adaptive_patience) if diversity <= 0.1: pressure = max(pressure, 0.5) return base + (config.adaptive_max_rate - base) * pressure 

Khi diversity thấp (≤0. 1) hoặc stagnation cao, áp lực được tăng lên, mutation rate tăng theo để khám phá thêm. Tùy chọn này tắt mặc định để giữ baseline dễ so sánh. 

#### **c) Bounded 2-opt Local Search** 

Module algorithms/ga/local_search.py cài đặt tìm kiếm cục bộ 2-opt theo chiến lược first-improvement: với mỗi cặp (𝑖, 𝑗) theo thứ tự tăng dần, thử đảo đoạn route[i..j] và chấp nhận ngay nếu cải thiện chi phí, sau đó restart scan từ đầu. 

Python def improve( route: Route, cost: float, *, evaluate: Callable[[Route], float], should_stop: Callable[[], str | None], max_moves: int, max_probes: int, ) -> LocalSearchResult: """First improvement theo i,j tăng dần; restart sau move, giữ 0 và parent.""" probes, moves = 0, 0 while moves < max_moves and probes < max_probes: 

improved = False for left in range(1, len(route)-1): for right in range(left+1, len(route)): if should_stop() or probes >= max_probes: return LocalSearchResult(route, cost, probes, moves, ...) candidate = route[:left] + route[left:right+1][::-1] + route[right+1:] candidate_cost = evaluate(candidate)   # đây là full objective call probes += 1 if candidate_cost < cost: route, cost = candidate, candidate_cost moves += 1 improved = True break if improved: break if not improved: break return LocalSearchResult(route, cost, probes, moves, None) 

**Điểm quan trọng:** Mỗi probe 2-opt gọi một lần evaluate đầy đủ và được tính vào evaluations tổng. Điều này có nghĩa 2-opt cạnh tranh ngân sách evaluations với các thế hệ GA. 

## **2.2.9. Tổ chức mã nguồn** 

## **CHƯƠNG 3. THUẬT TOÁN ELEPHANT HERDING OPTIMIZATION** 

### **3.1. Tổng quan về Elephant Herding Optimization** 

### **3.1.1. Khái niệm EHO** 

Elephant Herding Optimization (EHO) là thuật toán tối ưu hóa lấy cảm hứng từ hành vi sống theo đàn của loài voi. Quần thể được chia thành nhiều nhóm nhỏ gọi là Clan, trong đó mỗi cá thể đại diện cho một lời giải và được đánh giá bằng hàm mục tiêu. Thuật toán sử dụng cơ chế cập nhật cá thể theo voi dẫn đầu (Matriarch) và cơ chế tách đàn (Separating Operator) để tìm kiếm lời giải tốt hơn. 

Đối với bài toán TSP, do lời giải được biểu diễn dưới dạng hoán vị các thành phố, nhóm sử dụng phiên bản Discrete EHO (D-EHO), điều chỉnh các phép cập nhật sang dạng rời rạc nhằm đảm bảo mỗi hành trình luôn hợp lệ. 

### **3.1.2. Nguyên lý hành vi đàn voi** 

Mỗi _Clan_ gồm một cá thể dẫn đầu gọi là _Matriarch_ . Các cá thể trong đàn cập nhật vị trí dựa trên Matriarch, trong khi Matriarch được điều chỉnh theo tâm của Clan. Bên cạnh đó, cá thể có fitness kém nhất sẽ được chọn để thực hiện cơ chế _Separation_ , tạo cá thể mới nhằm duy trì sự đa dạng của quần thể. Ba cơ chế này giúp thuật toán cân bằng giữa khai thác nghiệm tốt và khám phá các vùng nghiệm mới. 

### **3.1.3. Các thành phần chính của EHO** 

Thuật toán EHO mô phỏng hành vi sống theo đàn của voi, trong đó quần thể được chia thành 𝑁𝑐 clan, mỗi clan gồm 𝑚 cá thể. Các thành phần chính bao gồm: 

- Clan: Nhóm các cá thể voi trong quần thể. 

- Matriarch: Cá thể có nghiệm tốt nhất trong mỗi clan, đóng vai trò dẫn dắt. 

- Clan center: Tâm đại diện cho các cá thể trong clan. 

- Clan updating operator: Cập nhật cá thể dựa trên ảnh hưởng của matriarch và tâm clan. 

- Separating operator: Thay thế cá thể có nghiệm kém nhằm duy trì tính đa dạng của quần thể. 

#### **Cơ chế cập nhật của EHO liên tục** 

Vị trí voi thường được cập nhật dựa trên matriarch: 



Matriarch được cập nhật dựa trên tâm clan: 



Trong đó, α, β ∈[0, 1] là các hệ số điều chỉnh;  là số ngẫu nhiên trong khoảng 𝑟 [0, 1]. Cá thể có vị trí kém nhất được thay thế bằng vị trí mới trong miền tìm kiếm: 



#### **Điều chỉnh EHO cho bài toán TSP** 

Các công thức trên được thiết kế cho không gian liên tục. Trong khi đó, bài toán TSP biểu diễn nghiệm dưới dạng hoán vị thứ tự các thành phố. Vì vậy, không thể áp dụng trực tiếp phép cộng, trừ hoặc tính trung bình tọa độ vì có thể tạo ra tour không hợp lệ. 

Do đó, dự án sử dụng Discrete EHO (D-EHO), kế thừa cấu trúc clan, matriarch và cơ chế tách đàn, đồng thời thay đổi các phép cập nhật sang thao tác trên hoán vị để đảm bảo mỗi tour hợp lệ. 

Chất lượng mỗi nghiệm được đánh giá bằng tổng chiều dài tour: 



Với 𝑇𝑛+1 = 𝑇1, tour phải quay về thành phố xuất phát. Mục tiêu của thuật toán là tìm tour có tổng quãng đường ngắn nhất. 

### **3.2. Áp dụng EHO cho bài toán TSP** 

|**Thành phần EHO**|**Cách áp dụng trong D-EHO**|
|---|---|
|Cá thể|Một tour gồm thứ tự các thành phố, cố định thành phố 0 ở đầu|
|Clan|Nhóm gồm<br>tour<br>𝑚|
|Matriarch|Tour có tổng quãng đường ngắn nhất trong clan|
|Tâm clan|Tour medoid có tổng khoảng cách Hamming nhỏ nhất|
|Cập nhật<br>α|Dùng guided-swap đưa các tour về matriarch|
|Cập nhật<br>β|Dùng guided-swap đưa matriarch về tâm clan|



|Separation|Thay các tour kém nhất bằng hoán vị ngẫu nhiên hợp lệ|
|---|---|
|Elitism|Lưu nghiệm tốt nhất của từng clan và toàn quần thể|



### **3.2.1. Biểu diễn nghiệm và hàm mục tiêu** 

Với  thành phố, mỗi cá thể được biểu diễn bằng một tour: 𝑛 



Trong đó, thành phố 0 được cố định ở đầu và các thành phố còn lại được sắp xếp theo dạng hoán vị. 

Hàm mục tiêu là tối thiểu hóa tổng chiều dài tour: 



Trong đó,  là ma trận khoảng cách giữa các thành phố. Tour phải quay về thành phố 𝐷 xuất phát. Dữ liệu sử dụng ma trận khoảng cách đối xứng, hữu hạn và không âm, tương ứng với bài toán Symmetric TSP. 

### **3.2.2. Phân chia quần thể thành các Clan** 

Quần thể gồm 𝑁𝑐 clan, mỗi clan có 𝑚 tour. Mỗi tour được lưu cùng chi phí tương ứng để thuận tiện cho việc đánh giá và lựa chọn cá thể tốt nhất. 

Matriarch được xác định bằng tour có chi phí nhỏ nhất: 



Đoạn mã thực hiện việc lựa chọn Matriarch và xác định tâm clan: 

Python @dataclass(frozen=True) class Clan: members: tuple[Route, ...] costs: tuple[float, ...] def best_index(self) -> int: return min(range(self.size), key=lambda index: (self.costs[index], index)) 

def center(self) -> Route: return self.members[self.center_index()] 

Sơ đồ thao tác chính trên một clan: 



<!-- Start of picture text -->
Chon route cost<br>thdp nhat:<br>matriarch<br>Population: N_c Chia thanh N_c Ghép méi route Clan sn sang cho<br>mroute clan v6i cost EHO update<br>Tinh Hamming<br>medoid: center<br><!-- End of picture text -->

### **3.2.3. Cập nhật Matriarch** 

Do không thể tính trung bình trực tiếp trên các hoán vị, D-EHO sử dụng Hamming Medoid để xác định tâm clan. 

Khoảng cách Hamming giữa hai tour được tính bằng số vị trí khác nhau: 



Tâm clan là tour có tổng khoảng cách Hamming nhỏ nhất đến các tour còn lại: 



Nếu có nhiều tour cùng khoảng cách, ưu tiên tour có chi phí thấp hơn. 

Sau đó, matriarch được cập nhật về phía tâm clan bằng guided-swap với hệ số . β Luồng tính tâm clan: so sánh các route theo từng cặp, cộng khoảng cách của từng route, rồi chọn route có tổng nhỏ nhất; hòa thì ưu tiên cost và index: 



<!-- Start of picture text -->
So san tour cost<br>nanroute dannrongsachcian ennTinhStones Hammingng cp Cong astancembiroute cho Téng distancehat? nhs Duy >|rng J index Chon route medols<br><!-- End of picture text -->

Python def center_index(self) -> int: distance_totals = [0] * self.size for first in range(self.size): for second in range(first + 1, self.size): distance = hamming_distance(self.members[first], self.members[second]) distance_totals[first] += distance distance_totals[second] += distance return min( range(self.size), key=lambda index: (distance_totals[index], self.costs[index], index), ) 

### **3.2.4. Di chuyển voi thường (Clan Updating Operator)** 

Trong D-EHO, các cá thể voi thường được cập nhật bằng phép **Guided-Swap** , đưa route hiện tại tiến gần route Matriarch. Hệ số  điều khiển mức độ cập nhật. α 

Với route nguồn , route đích target, tập vị trí khác nhau được xác định: π 



<!-- Start of picture text -->
diff ={j | mj # target;, j > 1}<br><!-- End of picture text -->

Số lần hoán đổi được tính bằng: 



<!-- Start of picture text -->
k=|a-r-|diff\|<br><!-- End of picture text -->

Trong đó, 𝑟∼𝑈[0, 1) là số ngẫu nhiên và α ∈[0, 1] là hệ số cập nhật. 

Quá trình Guided-Swap thực hiện: 

1. Xác định các vị trí khác nhau giữa hai route. 

2. Xáo trộn danh sách vị trí khác nhau. 

3. Chọn vị trí cần cập nhật và hoán đổi thành phố hiện tại với thành phố tương ứng trong route đích. 

4. Lặp lại cho đến khi đủ số lần hoán đổi. 

Phép hoán đổi không tác động đến thành phố xuất phát (index 0), đồng thời đảm bảo route luôn là một hoán vị hợp lệ. Khi α = 0, route được giữ nguyên; khi α = 1, thuật toán trả về route đích theo xử lý biên của hàm. 

**Sơ đồ quy trình Guided-Swap:** 



Python diff = [i for i in range(1, n) if source[i] != target[i]] steps = floor(strength * rng.random() * len(diff)) if steps <= 0: return tuple(source) result = list(source) pos = [0] * n for idx, city in enumerate(result): pos[city] = idx rng.shuffle(diff) swaps_done = 0 for i in diff: if swaps_done >= steps: break desired_city = target[i] current_city = result[i] if current_city == desired_city: continue j = pos[desired_city] result[i], result[j] = desired_city, current_city pos[desired_city] = i pos[current_city] = j swaps_done += 1 

### **3.2.5. Tách đàn (Separating Operator)** 

#### **Mục đích** 

Toán tử tách đàn (Separating Operator) được sử dụng nhằm duy trì tính đa dạng của quần thể và hạn chế tình trạng hội tụ sớm vào nghiệm tối ưu cục bộ. Trong EHO, toán tử này tác động lên những cá thể có chất lượng kém nhất trong mỗi clan, đồng thời bảo vệ cá thể dẫn đầu (Matriarch) để giữ lại nghiệm tốt hiện tại. 

#### **Nguyên lý hoạt động** 

Khác với EHO truyền thống áp dụng trên không gian liên tục, bài toán TSP biểu diễn mỗi cá thể dưới dạng một hoán vị (permutation) các thành phố. Vì vậy, không thể sinh cá thể mới bằng cách lấy ngẫu nhiên tọa độ trong một khoảng biên như (LB) và (UB). 

Thay vào đó, thuật toán thực hiện các bước sau: 

1. Bảo vệ Matriarch: Loại bỏ chỉ số của cá thể Matriarch khỏi danh sách các cá thể có thể bị thay thế. 

2. Xác định cá thể kém nhất: Sắp xếp các cá thể còn lại trong clan theo cost giảm dần và chọn separation_count_per_clan cá thể có cost cao nhất. 

3. Giữ lại cá thể không bị tách: Các route không được chọn sẽ được giữ nguyên vị trí và giá trị. 

4. Tạo cá thể mới: Thay thế mỗi route được chọn bằng một hoán vị ngẫu nhiên hợp lệ được sinh bởi hàm random_permutation(n, rng). 

5. Tạo clan mới: Kết hợp các route được giữ lại và các route mới để hình thành clan candidate có kích thước không đổi. 

#### **Quy trình thực hiện** 



<!-- Start of picture text -->
itr nguyén route<br>khdng bi tach<br>Clan hién tai va Loal matriarch Chon s route cost Clan candidate<br>Knot danh sch co<br>cost thé tach cao nhat cong 9 kich thu<br>Tao s permutation<br>ngdu nhién hop Ie<br><!-- End of picture text -->

Python 

protected = set(protected_indices) 

eligible = [index for index in range(clan_size) if index not in protected] worst_indices = sorted(eligible, key=lambda i: (-costs[i], i))[:separation_count] for idx in worst_indices: 

new_clan[idx] = random_permutation(n, rng) 

### **3.2.6. Cơ chế bảo tồn nghiệm tốt nhất (Elitism)** 

#### **Mục đích** 

Cơ chế bảo tồn nghiệm tốt nhất (Elitism) được sử dụng nhằm đảm bảo các lời giải tốt nhất đã tìm được không bị mất đi trong quá trình tiến hóa của thuật toán EHO. Cơ chế này lưu trữ nghiệm tốt nhất của từng clan (Clan Archive) và nghiệm tốt nhất trên toàn bộ quần thể (Global Best), từ đó hạn chế việc chất lượng lời giải bị suy giảm qua các thế hệ. 

#### **Nguyên lý hoạt động** 

Trong implementation này, cơ chế Elitism được triển khai thông qua hai cấp độ lưu trữ: 

- **Clan Archive:** Lưu trữ route tốt nhất từng được tìm thấy của mỗi clan. Archive được khởi tạo bằng route tốt nhất ban đầu của clan tương ứng. 

- **Global Best:** Lưu trữ route có cost nhỏ nhất được tìm thấy trong toàn bộ quá trình chạy thuật toán, không phụ thuộc vào clan hay thế hệ. 

Quá trình cập nhật và bảo tồn nghiệm tốt nhất được thực hiện như sau: 

1. **Khởi tạo Archive:** Sau khi khởi tạo quần thể, route tốt nhất của mỗi clan được lưu vào Clan Archive. 

2. **Đánh giá candidate:** Mỗi khi một candidate được đánh giá, thuật toán so sánh cost của route với Clan Archive tương ứng. Nếu candidate có cost nhỏ hơn, archive của clan được cập nhật. 

3. **Cập nhật Global Best:** Candidate tiếp tục được so sánh với nghiệm tốt nhất toàn cục. Nếu có cost nhỏ hơn, Global Best được cập nhật. 

4. **Khôi phục nghiệm tốt nhất:** Sau khi một generation hoàn chỉnh, thuật toán kiểm tra xem route được lưu trong Clan Archive còn tồn tại trong clan hay không. Nếu route đã bị mất, thuật toán đưa route này trở lại clan bằng cách thay thế thành viên có cost lớn nhất, nhưng không thay thế Matriarch hiện tại. 

5. **Commit generation:** Sau khi hoàn tất quá trình bảo tồn, generation mới được xác nhận và trở thành trạng thái chính thức của quần thể. 

#### **Quy trình thực hiện** 



Python def _preserve_clan_best(clan: Clan, best_route: Route, best_distance: float) -> Clan: if best_route in clan.members: return clan leader_index = clan.best_index() replacement_index = clan.worst_indices(1, protected_indices=(leader_index,))[0] members = list(clan.members) costs = list(clan.costs) members[replacement_index] = best_route costs[replacement_index] = best_distance 

return Clan(tuple(members), tuple(costs)) 

### **3.3. Quy trình hoạt động của D-EHO** 

### **3.3.1. Sơ đồ luồng thuật toán** 



### **3.3.2. Giả mã (Pseudocode)** 

Python Input: TSP distance matrix D, clan_count N_c, elephants_per_clan m, alpha, beta, separation_count s, stopping limits Output: best valid tour and its distance Initialize N_c clans with m random valid tours each Evaluate all initial tours For each clan: archive its best tour Set global_best to the best initial tour While no stopping condition is met: Create an empty next_population For each clan: Select the lowest-cost tour as matriarch Compute the clan Hamming medoid Select up to s worst tours, excluding the matriarch For each member index i: If i is the matriarch: candidate = guided_swap(matriarch, medoid, beta) Else if i is selected for separation: candidate = random valid permutation Else: candidate = guided_swap(member[i], matriarch, alpha) Evaluate candidate once Update clan archive and global_best if improved Append candidate to next clan If every clan was completed: Restore archived clan best when needed If a full generation was completed: Commit next_population Else: 

Keep the last committed population and stop 

Return global_best and run metadata 

### **3.3.3. Giải thích quá trình cập nhật một thế hệ** 

Quá trình cập nhật một Generation gồm các bước: 

1. **Khởi tạo:** Tạo (N_c) clan, mỗi clan có (m) route ngẫu nhiên và đánh giá cost. 

2. **Xác định cá thể:** Chọn Matriarch có cost thấp nhất và tính Hamming Medoid cho từng clan. 

3. **Tách đàn:** Chọn tối đa (s) route có cost cao nhất, không bao gồm Matriarch. 

4. **Cập nhật cá thể:** Matriarch cập nhật theo Medoid với (\beta); cá thể Separation được thay bằng permutation ngẫu nhiên; các cá thể còn lại cập nhật theo Matriarch với (\alpha). 

5. **Đánh giá và bảo tồn:** Đánh giá từng candidate đúng một lần, cập nhật Clan Archive và Global Best nếu tìm được nghiệm tốt hơn. 

6. **Commit Generation:** Khôi phục Clan Archive nếu cần, sau đó chỉ commit khi tất cả clan hoàn thành. Nếu dừng giữa generation, giữ population đã commit gần nhất nhưng vẫn trả về Global Best tốt nhất đã tìm được. 

### **3.4. Triển khai thuật toán trong chương trình** 

### **3.4.1. Cấu trúc các module** 

Thuật toán EHO được triển khai thành các module riêng biệt, mỗi module đảm nhiệm một chức năng: 

|**Module**|**Trách nhiệm**|
|---|---|
|solver.py|Khởi tạo clan, điều khiển vòng lặp, cập nhật archive và trả kết quả|
|clans.py|Quản lý clan, chọn best/worst và tính Hamming Medoid|
|discrete_ops.py|Tình Hamming distance và thực hiện guided-swap|
|separation.py|Chọn route kém và sinh permutation mới|
|objective.py|kiểm tra route và tính tổng khoảng cách|



**Sơ đồ kết nối các thành phần chương trình:** 



<!-- Start of picture text -->
Clan selection and<br>medoid<br>Shared TSP<br>objective<br>CLI/ Benchmarkenenmart / EHO solver.solve Separatieparating<br>GUI operator<br>RunResult,<br>history, best route<br><!-- End of picture text -->

Khởi tạo quần thể trong solver.py: 

Python rng = Random(config.seed) clans: list[Clan] = [] for _ in range(config.clan_count): members = tuple( random_permutation(problem.dimension, rng) for _ in range(config.elephants_per_clan) ) costs = tuple(problem.route_length(route) for route in members) clans.append(Clan(members, costs)) 

Mỗi clan được khởi tạo bằng các route ngẫu nhiên hợp lệ, sau đó tính cost và đóng gói thành đối tượng Clan. 

Cập nhật cá thể: 

Python if index == leader_index: candidate = update_matriarch(route, center, config.beta, rng) elif index in separated: candidate = separated_members[index] else: candidate = move_toward_best(route, leader, config.alpha, rng) cost = problem.route_length(candidate) 

evaluations += 1 

Tùy vị trí và vai trò, mỗi cá thể được cập nhật bằng Matriarch Update, Separation hoặc Clan Update. Sau đó candidate được đánh giá và cập nhật nghiệm tốt nhất. 

### **3.4.2. Các tham số cấu hình** 

Các tham số được quản lý thông qua EHOConfig trong domain/models.py: 

|**Tham số**|**Giá trị mặc định**|**Ý nghĩa**|
|---|---|---|
|clan_count|Theo cấu hình|Số lượng clan|
|elephants_per_clan|Theo cấu hình|Số cá thể mỗi clan|
|alpha|0.7|Hệ số cập nhập cá thể|
|beta|0.3|Hệ số cập nhật Matriarch|
|separation_count_per_clan|1|Số cá thể tách mỗi clan|
|seed|Theo cấu hình|Giá trị khởi tạo ngẫu nhiên|
|iterations|Theo cấu hình|Số thế hệ chay|



Các điều kiện kiểm tra chính: 

- Mỗi clan có ít nhất 3 cá thể và có tối thiểu 2 clan. 

- alpha, beta thuộc khoảng [0, 1]. 

- Số cá thể separation phải nhỏ hơn kích thước clan. 

- Baseline sử dụng khởi tạo ngẫu nhiên và bật preserve_global_best. 

- Evaluation budget phải đủ để đánh giá quần thể ban đầu. 

### **3.4.3. Điều kiện dừng và quản lý đánh giá** 

Solver có thể dừng khi đạt giới hạn thế hệ, max_evaluations, time_limit_seconds hoặc callback yêu cầu dừng. max_evaluations phải đủ đánh giá population ban đầu; giới hạn thời gian nếu có phải dương. Dữ liệu đầu vào là symmetric TSP, có ít nhất 3 thành phố, ma trận hữu hạn, không âm, đối xứng và đường chéo bằng 0. 

Nếu chạy đủ G thế hệ và không dừng sớm, số objective evaluations là N_c * m * (G + 1): đánh giá population ban đầu một lần, cộng một lần cho mỗi candidate mỗi generation. Candidate trùng route vẫn được tính là một evaluation; khôi phục route archive không đánh giá lại vì cost đã lưu. Nếu budget/time dừng giữa generation, 

solver không commit generation dở dang; population giữ ở generation hoàn chỉnh gần nhất, còn global best giữ nghiệm tốt nhất đã đánh giá. 

Mỗi candidate chỉ được bắt đầu tạo khi chưa có yêu cầu dừng; sau đó solver đánh giá nó một lần và cập nhật nghiệm tốt nhất. Sơ đồ điều kiện dừng: 



Đoạn mã kiểm tra stop: 

Python def get_stop_reason() -> str | None: if stop_requested is not None and stop_requested(): return "CANCELLED" if (config.time_limit_seconds is not None and perf_counter() - start >= config.time_limit_seconds): return "TIME_LIMIT" if config.max_evaluations is not None and evaluations >= config.max_evaluations: return "MAX_EVALUATIONS" return None 

### **3.5. Nhận xét và giới hạn của D-EHO** 

### **3.5.1. Ưu điểm** 

D-EHO giữ các thành phần có ý nghĩa của EHO clan, matriarch, cập nhật clan và separation, đồng thời mọi thao tác đều tạo route hợp lệ mà không cần repair. Archive theo clan và global best hạn chế mất nghiệm tốt đã tìm thấy. Solver hỗ trợ seed, giới hạn số lần đánh giá và giới hạn thời gian để tổ chức các lần chạy lặp lại. 

### **3.5.2. Hạn chế** 

D-EHO thay phép toán vector của EHO liên tục bằng guided-swap, Hamming medoid và permutation ngẫu nhiên. Đây là thích nghi cho không gian hoán vị, không phải tương đương đại số với EHO liên tục. Hamming medoid xét vị trí thành phố, không trực tiếp tối ưu mức tương đồng cạnh của chu trình. Archive matriarch theo clan là cơ chế elitism bổ sung của implementation. Solver hiện chỉ hỗ trợ symmetric TSP; heuristic không bảo đảm tìm optimum toàn cục. 

Benchmark EHO ở trên dùng năm seed và dataset registry không có optimum đã xác minh. Vì vậy kết quả mô tả cấu hình được chạy, không chứng minh tối ưu. So sánh hiệu năng cần dùng cùng dataset, seed, evaluation budget và môi trường. 

### **3.5.3. Khả năng áp dụng cho TSP** 

Implementation phù hợp với phạm vi đề tài hiện tại: TSP đối xứng, có ít nhất ba thành phố và ma trận khoảng cách hữu hạn, không âm, đối xứng, đường chéo bằng 0. Việc cố định thành phố `0` ở đầu route loại bỏ các biểu diễn quay vòng tương đương mà vẫn giữ nguyên chu trình đóng. 

Để mở rộng sang TSP bất đối xứng, cần xác nhận lại các giả định của objective và đánh giá lại các toán tử trên chu trình có hướng. Với bài toán lớn hơn, có thể nghiên cứu toán tử ưu tiên bảo toàn cạnh hoặc kết hợp tìm kiếm cục bộ, nhưng cần kiểm tra bằng thí nghiệm mới thay vì suy rộng trực tiếp từ benchmark hiện có. 

D-EHO đã có thể dùng làm một solver rời rạc độc lập để minh họa và thực nghiệm EHO trên TSP đối xứng trong phạm vi dữ liệu của dự án. Bằng chứng hiện tại xác nhận tính hợp lệ và khả năng chạy của implementation; đánh giá chất lượng nghiệm tương đối với GA hoặc optimum vẫn cần thí nghiệm đối chứng bổ sung. 

## **CHƯƠNG 3. CÁC KẾT QUẢ THỰC NGHIỆM** 

### **3.1. Thiết kế thực nghiệm** 

### **3.1.1. Bộ dữ liệu** 

Dự án sử dụng bảy bộ dữ liệu ma trận khoảng cách đối xứng với quy mô từ nhỏ đến trung bình. Dữ liệu được lưu dưới dạng file văn bản, mỗi dòng là một hàng ma trận, các số cách nhau bởi khoảng trắng. 

|**Tên file**|**Số thành phố**|
|---|---|
|03Cities-6.txt|3|
|04Cities-189.txt|4|
|06Cities-1248.txt|6|
|15Cities-1194.txt|15|
|26Cities-937.txt|26|
|42Cities-699.txt|42|
|48Cities-33523.txt|48|



### **3.1.2. Cấu hình thực nghiệm** 

Thực nghiệm được tổ chức thành ba nhóm trong ba notebook Jupyter: 

Notebook 1-2 (so sánh toán tử): Bài 15 thành phố, quần thể 40, ngân sách 2.000 evaluations, 5 seed [11, 23, 37, 53, 71]. Mỗi lần thử nghiệm thay đổi đúng một tham số so với cấu hình cơ sở (OFAT - One Factor At a Time). 

Notebook 3 (phân phối kết quả): Sáu bộ dữ liệu (3-48 thành phố), quần thể 40, ngân sách 4.000 evaluations, 5 seed. Phân tích độ ổn định và phân phối kết quả theo kích thước bài toán. 

Notebook 4 (các biến thể nâng cao): Bốn bài toán (15, 26, 42, 48 thành phố), quần thể 40, ngân sách 4.000 evaluations, 5 seed, 6 biến thể: Control, PMX, Mixed 25%, NN, Adaptive, GA+2-opt. 

Cấu hình baseline: 

None population_size   = 80  (benchmark) / 40 (notebook) generations       = 2000 max_iterations    = 2000 

selection_method  = tournament (k=3) crossover_method  = ox crossover_rate    = 0.9 mutation_method   = inversion mutation_rate     = 0.15 elite_count       = 2 initialization    = random local_search      = disabled seed set          = [11, 23, 37, 53, 71] max_evaluations   = 6000 (benchmark) / 2000 hoặc 4000 (notebook) 

## **3.2. Kết quả so sánh toán tử trên bài 15 thành phố** 

Bảng dưới đây tổng hợp kết quả từ Notebook 1-2, so sánh cấu hình cơ sở với các biến thể thay đổi từng toán tử. Mỗi biến thể chạy với ngân sách 2.000 evaluations và 5 seed. 

|**Biến thể**|**Mean distance**|**Trung vị**|**Độ lệch chuẩn**|
|---|---|---|---|
|Cơ sở (tournament<br>+ OX + inversion)|1235.0|1225|43.86|
|Rank selection|1413.6|1402|81.79|
|Roulette selection|1400.8|1340|158.48|
|PMX thay OX|1275.4|1279|38.34|
|Swap mutation|1317.0|1289|113.40|
|Insertion mutation|1319.8|1287|68.16|
|Scramble mutation|1473.0|1391|152.78|



Trong điều kiện thực nghiệm này: 

- Cấu hình cơ sở (tournament + OX + inversion) cho kết quả trung bình tốt nhất 

- PMX cho trung vị cao hơn cơ sở một chút (1279 so với 1225) nhưng độ lệch chuẩn thấp hơn (38.34 so với 43.86), gợi ý kết quả ổn định hơn nhưng chưa tốt bằng 

- Rank và roulette selection cho kết quả kém hơn đáng kể trong cấu hình này; độ lệch chuẩn của roulette đặc biệt cao (158.48), cho thấy kết quả không ổn định 

- Scramble mutation cho kết quả kém nhất, có thể do phá vỡ cấu trúc hành trình quá mạnh 



<!-- Start of picture text -->
So sénh mean distance va dé léch chuan gitta cac bién thé toan tir<br>Co sé (tournament + OX + inversion)<br>Rank selection<br>Roulette selection<br>Or<br>sé<br>5 PMX thay OX<br>3a<br>Swap mutation<br>Insertion mutation<br>Scramble mutation<br>° 200 400 600 800 1000 1200» 1400—S 1600<br>Mean distance (don vi ma tran)<br><!-- End of picture text -->

_Hình 3.1 - Biểu đồ so sánh mean distance giữa các biến thể toán tử_ 

## **3.3. Phân phối kết quả theo kích thước bài toán** 

Notebook 3 khảo sát 6 bộ dữ liệu với ngân sách 4.000 evaluations/run. Với bài 3 và 6 thành phố, notebook còn kiểm chứng bằng cách liệt kê exhaustive tất cả hoán vị tail để xác minh hàm chi phí tính đúng. 

|**Số thành**<br>**phố**|**Min**|**Mean**|**Median**|**Max**|**Std**|**Tỷ lệ đạt**<br>**min quan**<br>**sát**|
|---|---|---|---|---|---|---|
|3|6|6|6|6|0|100%|
|6|1248|1248|1248|1248|0|100%|
|15|1194|1200.2|1194|1225|13.86|80%|
|26|969|1046|1034|1186|82.85|20%|
|42|1102|1151.6|1133|1211|49.75|20%|
|48|51215|55404.6|55339|59638|3031.79|20%|



Nhận xét: 

- Với các bài rất nhỏ (3 và 6 thành phố), GA tìm được nghiệm tốt nhất trong 100% lần chạy, kết quả ổn định hoàn toàn 

- Từ bài 15 thành phố trở đi, bắt đầu xuất hiện sự biến động; bài 15 đạt tỷ lệ 80% hit min quan sát 

- Từ bài 26 thành phố trở lên, tỷ lệ hit giảm còn 20% và độ lệch chuẩn tăng mạnh, phản ánh sự phức tạp tăng của không gian tìm kiếm 

- “Tỷ lệ đạt min quan sát” cho biết tần suất các run chạm vào kết quả tốt nhất trong mẫu, không phải xác suất tìm optimum toàn cục 



<!-- Start of picture text -->
Phan phdi két qua theo kich thudc bai todn<br>3 thanh phé 6 thanh phd 15 thanh phé-<br>°6<br>55 5<br>Bs 23 Ys<br>11<br>0° 0<br>1 di26tourthanh(don°  vipho ma tan) 16 di42 tourthanh (dan1248 vpho ma tn) 1195 1200'¢ dl130s48tourthanh (donaslo vipho mawis tran) 1200 1225<br>°°<br>55 5<br>ae Sa Sa<br>2: 3s Qs<br>22 3, 2<br>11<br>o° o<br>10001080.19 di tour (an vi~—=ai00 ma trbn) «1130 Heo aig 1 dai1s tour (donai60 vi ma tr}1801200 52000 1634000dal tour (danS600 vi matin)—s8000 60000<br><!-- End of picture text -->

_Hình 3.2 - Phân phối kết quả theo kích thước bài toán_ 

## **3.4. Khởi tạo nâng cao, Adaptive Mutation và 2-opt** 

Notebook 4 so sánh 6 biến thể trên 4 bài toán (15, 26, 42, 48 thành phố), ngân sách 4.000 evaluations, 5 seed. 

|**Số thành**<br>**phố**|**Control**|**PMX**|**Mixed**<br>**25%**|**NN**|**Adaptive**|**GA+2-op**<br>**t**|
|---|---|---|---|---|---|---|
|15|1200.2|1219.2|1194.0|1194.0|1228.0|1336.2|
|26|1046.0|1054.0|958.6|961.8|1016.4|1388.8|
|42|1151.6|1114.8|811.8|782.2|1112.4|1750.2|
|48|55404.6|55073.2|37222.2|36559.0|53912.2|81489.6|



#### **Phân tích kết quả:** 

**NN và Mixed initialization:** Cho kết quả tốt hơn rõ rệt khi bài toán lớn hơn. Tại bài 48 thành phố, mixed (37222.2) và NN (36559.0) thấp hơn đáng kể so với control (55404.6). Tuy nhiên, cần lưu ý rằng khởi tạo NN có thêm chi phí tính toán trong runtime (matrix lookups để xây dựng tour NN). 

**GA+2-opt:** Cho kết quả kém hơn control ở cả 4 bài trong cấu hình này. Lý do: mỗi probe 2-opt gọi một lần route_length đầy đủ và được tính vào max_evaluations. Tại bài 48 thành phố, 2-opt tiêu thụ trung bình 3163.4 trong 4000 evaluations cho các phép thử local search, chỉ commit được khoảng 20.6 thế hệ so với 104 thế hệ của control. Đây là đánh đổi quan trọng: local search cải thiện từng cá thể nhưng làm giảm số thế hệ được khám phá. 

**Adaptive Mutation:** Kết quả không nhất quán, tốt hơn control ở một số bài nhưng kém hơn ở bài khác trong cấu hình preset này. Tùy chọn vẫn tắt mặc định. 



<!-- Start of picture text -->
So sanh Mean Cost ctia 6 bién thé GA trén 4 bai toan TSP.<br>Bai todn 15 thanh phd Bai ton 26 thanh pho<br>1600<br>1400 13362 13088<br>=z 12002-12182 ago n94.0 1228.0 == 1400<br>pe 27°] roweo soss0<br>E 1000 E 000 osee oeng 1Oes<br>§ 200 § 00<br>% 600 600<br>§ 400 § 400<br>£ Es<br>200 200<br>°°<br>cot\MK age WN ative\e cpaoftt corel\ Kans WN aptave cz010<br>Bai toan 42 thanh phé Bai toan 48 thanh pho<br>2000<br>17502 arses.<br>31750 = 80000<br>E 1500 é<br>—$1250} 6 aise — == 60000 55404.6 55073.2 s39122<br>=§ 1000 ms yen &§ 0000 27222265590<br>% 750 8<br>3 00 3 20000<br>250°°<br>conts0l\pk xe 25% ww pdastN®e on42-0PEof contol\ Ped NN aahave ga2 0108<br><!-- End of picture text -->

_Hình 3.3 - So sánh 6 biến thể GA trên 4 bài toán_ 



<!-- Start of picture text -->
Dudng hdi tu GA (best-so-far) — Bai toan 48 thanh phd, Seed 11<br>—— Ngau nhién + OX<br>— PMx<br>120000 — Adaptive<br>— GA+2-opt<br>s — PMX + Mixed<br>2 — Mixed + Adaptive<br>*S 100000<br>a<br>3<br>oa<br>2<br>2 80000<br>2<br>5<br>2<br>=<br>8 60000<br>40000 aoe eee<br>C) 1000 2000 3000 4000 5000 6000<br>Cumulative evaluations ($6 lan danh gia tich lity)<br><!-- End of picture text -->

_Hình 3.4 - Đường hội tụ GA (convergence curve)_ 

## **3.5. Benchmark trên bảy bộ dữ liệu** 

Benchmark đầy đủ chạy 7 bộ dữ liệu × 5 seed = 35 lần chạy, mỗi lần dùng 6.000 evaluations, quần thể 80, cấu hình cơ sở. 

|**Số thành phố**|**Mean distance**|**Độ lệch chuẩn**|**Runtime trung**<br>**bình (giây)**|
|---|---|---|---|
|3|6|0|0.0440|
|4|189|0|0.0471|
|6|1248|0|0.0508|
|15|1200.2|13.86|0.0642|
|26|1056.4|72.84|0.0818|
|42|1166.2|26.28|0.1012|
|48|54194.4|3861.50|0.1154|



Tất cả 35 lần chạy hoàn thành hợp lệ (is_valid=True). Không có lần chạy nào thất bại. 

Nhận xét: 

- **Bài nhỏ (3, 4, 6 thành phố):** Kết quả hoàn toàn ổn định (độ lệch chuẩn 0); GA luôn tìm được cùng một nghiệm 

- **Bài lớn hơn:** Độ lệch chuẩn tăng theo kích thước bài, phản ánh tính ngẫu nhiên của GA 

- **Runtime:** Tăng tuyến tính theo kích thước bài, từ ~44ms (3 thành phố) đến ~115ms (48 thành phố) trên môi trường thực nghiệm. Runtime phụ thuộc phần cứng và không phải cam kết hiệu năng 

- **Gap với optimum:** Chưa có known optimum được xác minh cho các bài lớn trong registry, nên không thể tính phần trăm gap 



<!-- Start of picture text -->
Két qua Benchmark GA Baseline (5 seeds, 6000 evaluations)<br>Thdi gian thyc thi trung binh (6000 evaluations) D6 dai tour trung binh (Thang Logarit)<br>120 1026 mam | 3ai seiss.4<br>§ 10%<br>100 ms &<br>E. eagme i ie 17002 esga 862<br>2 em Et.<br>§ 60 sms § 189<br>3 tsome 72m 3<br>E 0 i<br>20 Zio] 6<br>Hy<br>:<br>° 28~ ooeS cee28 ceeoF oegst oe aHe ao? ae© ee8 oegstoe oer2° oH”<br>of i) x « wet os oe so x was rec<br>89 du igu (Dataset) 89 diligu (Dataset)<br><!-- End of picture text -->

_Hình 3.5 - Kết quả benchmark 35 lần chạy_ 

## **CHƯƠNG 4. KẾT LUẬN** 

### **4.1. Các kết quả đạt được** 

### **4.2. Những hạn chế và hướng phát triển** 

## **TÀI LIỆU THAM KHẢO** 

[1] J. H. Holland, _Adaptation in Natural and Artificial Systems_ , University of Michigan Press, Ann Arbor, MI, USA, 1975. 

[2] D. E. Goldberg, _Genetic Algorithms in Search, Optimization, and Machine Learning_ , Addison-Wesley, Reading, MA, USA, 1989. 

[3] D. L. Applegate, R. E. Bixby, V. Chvátal, and W. J. Cook, _The Traveling Salesman Problem: A Computational Study_ , Princeton University Press, Princeton, NJ, USA, 2006. 

[4] I. M. Oliver, D. J. Smith, and J. R. C. Holland, "A study of permutation crossover operators on the traveling salesman problem," in _Proc. 2nd Int. Conf. Genetic Algorithms_ , 1987, pp. 224–230. 

[5] G. Wang, S. Deb, and L. dos Santos Coelho, "Elephant herding optimization," in _Proc. 3rd Int. Symp. Computational and Business Intelligence (ISCBI)_ , Bali, Indonesia, 2015, pp. 1–5. 

[6] A. Slowik, Ed., _Swarm Intelligence Algorithms: A Tutorial_ , CRC Press, Boca Raton, FL, USA, 2020. 

[7] T. Stützle, "Local search algorithms for combinatorial problems," Ph.D. dissertation, Darmstadt University of Technology, 1998. 

## **PHỤ LỤC** 

**Link GitHub:** <u>https://github.com/datweb07/ga-eho-tsp</u> 

#### **Hướng dẫn cài đặt/sử dụng chương trình:** 

#### **1. Yêu cầu môi trường** 

|**Thành phần**|**Phiên bản**|
|---|---|
|Python|3.11 trở lên|
|Hệ điều hành|Windows 10/11, macOS, Linux|
|RAM|Tối thiểu 4GB|



#### **2. Cài đặt môi trường** 

Từ thư mục gốc repository, thực hiện các bước sau: 

#### **Bước 1: Tạo virtual environment** 

None python --version          # Kiểm tra Python >= 3.11 python -m venv .venv 

#### **Bước 2: Kích hoạt môi trường** 

Trên Windows (PowerShell): 

None .\.venv\Scripts\Activate.ps1 

Nếu PowerShell báo lỗi execution policy: 

None 

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser .\.venv\Scripts\Activate.ps1 

Trên macOS/Linux: 

Shell source .venv/bin/activate 

#### **Bước 3: Cài đặt thư viện** 

None python -m pip install -r requirements.txt 

#### **Bước 4: Cài đặt package ở chế độ editable (cần thiết để chạy notebook)** 

None python -m pip install -e . 

#### **Bước 5: Xử lý encoding trên Windows (nếu cần)** 

Nếu terminal Windows hiển thị lỗi ký tự tiếng Việt hoặc mũi tên, thiết lập encoding cho phiên làm việc: 

None $env:PYTHONIOENCODING = "utf-8" 

#### **3. Kiểm tra cài đặt** 

Chạy lệnh compile để kiểm tra toàn bộ source: 

None python -m compileall -q src 

Kiểm tra tất cả bộ dữ liệu: 

None python -m ga_eho_tsp.cli validate 

Lệnh này sẽ kiểm tra tất cả file trong thư mục data/, in ra thông báo hợp lệ cho từng ma trận (tên bài, số thành phố, tính đối xứng, đường chéo 0, giá trị hữu hạn). 

#### **4. Chạy giao diện GUI** 

None python -m ga_eho_tsp.gui 

Hoặc sử dụng script Demo: 

None python Demo.py 

Giao diện cho phép: 

1. Chọn bộ dữ liệu từ danh sách 

2. Điều chỉnh các tham số GA (population, generations, mutation rate, v.v.) 

3. Chọn selection/crossover/mutation method 

4. Chạy GA và xem tiến trình real-time 

5. Xem kết quả: distance, tour, đồ thị hội tụ 

|**Thành viên**|**Nhiệm vụ**|
|---|---|
|TrươngThành Đạt||
|Nguyễn Tấn Khiêm||
|Nguyễn PhươngChinh||
|Lại Thành Đạt||





---

## PHỤ LỤC THÊM: THÔNG TIN KỸ THUẬT CHI TIẾT

### A.1. Chi tiết kỹ thuật Genetic Algorithm

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

Đã có P1: PMX, NN/mixed, profile-guided OX/prepared selection, monitoring/stagnation, CLI/export/ablation. P2 có adaptive + bounded 2-opt opt-in. GUI GA dùng trực tiếp solver này; GUI và CLI cũng có lựa chọn EHO riêng, không phải thuật toán lai. Xem [gui_guide.md](gui_guide.md) và [algorithm_eho.md](algorithm_eho.md). **Chưa có TSPLIB loader**, 2-opt delta engine, restart, hybrid GA–EHO hoặc đóng gói executable. TSPLIB hoãn vì chưa có fixture chuẩn/đối chiếu rounding/provenance đủ để nghiệm thu. Số đo và giới hạn diễn giải ở experiments.md.

Final cleanup không sửa thuật toán/default/shared contract. Suite166regression đã chạy trước khi archive/xóa theo chỉ thị leader; các mô tả kiểm thử phía trên là bằng chứng đã thực hiện, không có suite pytest đi kèm repo bàn giao. Ba notebook mới ở Experiment/ dùng trực tiếp package hiện tại, Run All Quick Mode đã được nghiệm thu từ root và Experiment/ trên hai kernel; xem [thí nghiệm](experiments.md) và [hợp đồng](architecture.md) để biết kết quả và rủi ro do bỏ regression suite.


### A.2. Chi tiết kỹ thuật Elephant Herding Optimization  

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


### A.3. Chi tiết thực nghiệm và nghiệm thu

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


---

**HẾT**

