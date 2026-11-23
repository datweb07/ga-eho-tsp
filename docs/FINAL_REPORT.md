# ĐỒ ÁN MÔN HỌC: TRÍ TUỆ NHÂN TẠO

## ỨNG DỤNG THUẬT TOÁN GENETIC ALGORITHM VÀ ELEPHANT HERDING OPTIMIZATION CHO BÀI TOÁN NGƯỜI DU LỊCH (TSP)

**Nhóm thực hiện:**
- TRƯƠNG THÀNH ĐẠT
- NGUYỄN TẤN KHIÊM  
- NGUYỄN PHƯƠNG CHINH
- LẠI THÀNH ĐẠT

**Giảng viên hướng dẫn:** TS. Đặng Ngọc Hoàng Thành

---

## MỤC LỤC

1. [TỔNG QUAN](#chương-1-tổng-quan)
2. [GIẢI THUẬT DI TRUYỀN (GA)](#chương-2-giải-thuật-di-truyền)
3. [THUẬT TOÁN ELEPHANT HERDING OPTIMIZATION (EHO)](#chương-3-thuật-toán-elephant-herding-optimization)
4. [KẾT QUẢ THỰC NGHIỆM](#chương-4-kết-quả-thực-nghiệm)
5. [KẾT LUẬN](#chương-5-kết-luận)

---

## CHƯƠNG 1. TỔNG QUAN

### 1.1. Giới thiệu bài toán người du lịch

Bài toán người du lịch (Traveling Salesman Problem - TSP) là một trong những bài toán tối ưu tổ hợp được nghiên cứu nhiều nhất trong khoa học máy tính và toán học rời rạc. Bài toán mô tả tình huống một người cần đi thăm một tập thành phố, mỗi thành phố được thăm đúng một lần, bắt đầu và kết thúc tại cùng một điểm xuất phát. Mục tiêu là xác định thứ tự thăm sao cho tổng chi phí di chuyển của toàn bộ chuyến đi là nhỏ nhất.

TSP có ứng dụng thực tiễn rộng rãi:
- Lập lịch phân phối hàng hóa
- Định tuyến mạch in điện tử (PCB drilling)
- Lập kế hoạch sản xuất
- Định tuyến robot công nghiệp
- Nhiều bài toán quy hoạch khác

### 1.2. Phát biểu bài toán

**Đầu vào:**
- Tập thành phố: V = {0, 1, ..., n-1}
- Ma trận khoảng cách D kích thước n × n
- D[i][j]: chi phí đi từ thành phố i đến thành phố j

**Điều kiện ma trận D:**
- Vuông: kích thước n × n với n ≥ 3
- Đường chéo bằng 0: D[i][i] = 0
- Đối xứng: D[i][j] = D[j][i] (Symmetric TSP)
- Các phần tử hữu hạn và không âm

**Biểu diễn nghiệm:**
- Một hành trình hợp lệ là hoán vị π của tất cả thành phố
- Quy ước: π[0] = 0 (cố định thành phố 0 làm điểm xuất phát)
- Route được lưu dưới dạng tuple số nguyên 0-based

**Hàm mục tiêu:**

Chi phí của hành trình π:

```
L(π) = Σ(k=0 to n-2) D[π[k], π[k+1]] + D[π[n-1], π[0]]
```

Số hạng cuối là chi phí quay về thành phố xuất phát, tạo thành chu trình khép kín.

**Mục tiêu:** Tìm π* sao cho L(π*) là nhỏ nhất:

```
π* = argmin L(π)
```

### 1.3. Độ phức tạp và lý do sử dụng thuật toán tìm kiếm

TSP thuộc lớp bài toán NP-Hard. Số lượng hành trình phân biệt với n thành phố (khi cố định điểm xuất phát) là (n-1)!.

| Số thành phố (n) | Số hành trình (n-1)! |
|------------------|----------------------|
| 3 | 2 |
| 6 | 120 |
| 10 | 362,880 |
| 15 | 87,178,291,200 |
| 20 | 1.2 × 10¹⁷ |
| 26 | ≈ 1.6 × 10²⁵ |

Liệt kê toàn bộ hành trình để tìm nghiệm tối ưu là điều không khả thi trong thực tế với các bài toán kích thước trung bình trở lên. Vì vậy, các phương pháp heuristic và metaheuristic (Genetic Algorithm và Elephant Herding Optimization) được sử dụng để tìm nghiệm đủ tốt trong thời gian hợp lý.

### 1.4. Hướng tiếp cận giải quyết

Đồ án triển khai hai thuật toán metaheuristic:

**1. Genetic Algorithm (GA):**
- Mô phỏng quá trình tiến hóa tự nhiên
- Duy trì quần thể gồm nhiều hành trình ứng viên
- Chọn lọc các cá thể tốt, kết hợp chúng để tạo thế hệ mới
- Áp dụng đột biến để khám phá vùng tìm kiếm mới

**2. Elephant Herding Optimization (EHO):**
- Mô phỏng hành vi đàn voi
- Chia quần thể thành các clan
- Cập nhật vị trí mỗi voi theo matriarch (cá thể tốt nhất trong clan)
- Tách các voi đực kém nhất khỏi clan

---

## CHƯƠNG 2. GIẢI THUẬT DI TRUYỀN

### 2.1. Giới thiệu về Genetic Algorithm

Genetic Algorithm (GA) là thuật toán tìm kiếm và tối ưu được Holland giới thiệu vào những năm 1970, lấy cảm hứng từ quá trình tiến hóa sinh học theo thuyết chọn lọc tự nhiên của Darwin.

**Quy trình GA:**
1. Đánh giá chất lượng (fitness) của từng cá thể
2. Chọn lọc các cá thể tốt làm cha mẹ (selection)
3. Lai ghép (crossover) để tạo cá thể con kế thừa đặc điểm
4. Đột biến (mutation) để duy trì đa dạng và khám phá vùng mới
5. Hình thành quần thể thế hệ tiếp theo

**Biểu diễn cho TSP:**
- Mỗi cá thể là một tuple chứa đầy đủ n thành phố
- Quy ước thành phố 0 luôn đứng đầu
- Các toán tử chỉ thao tác trên phần tail (từ vị trí 1 trở đi)
- Đảm bảo không làm mất tính hợp lệ của hoán vị

### 2.2. Cách áp dụng GA cho bài toán TSP

#### 2.2.1. Luồng xử lý tổng quát

```python
# Pseudocode vòng lặp GA
kiểm tra problem và config
rng = Random(config.seed)
population = khởi_tạo(population_size, rng)
costs = [route_length(r) for r in population]
best_route, best_distance = best(population, costs)
ghi snapshot iteration=0

for iteration in 1..min(generations, max_iterations):
    kiểm tra stop / time_limit / max_evaluations
    
    next_pop, next_costs = select_elites(population, costs, elite_count)
    selector = prepare_selection(population, costs, method, k)
    rate = effective_mutation_rate(config, stagnation, diversity)
    
    while len(next_pop) < population_size:
        kiểm tra stop
        p1, p2 = selector.pick(rng), selector.pick(rng)
        children = crossover(p1, p2, rng) if rng.random() < crossover_rate else (p1, p2)
        for child in children:
            child = mutate(child, rate, rng, mutation_method)
            cost = route_length(child)  # evaluations++
            cập nhật best_route, best_distance
            if local_search_enabled:
                child, cost = improve(child, cost, ...)
            next_pop.append(child)
    
    commit: population, costs = next_pop, next_costs
    cập nhật stagnation, ghi history
    kiểm tra STAGNATION

ghi snapshot cuối
trả RunResult(best_route, best_distance, ...)
```

#### 2.2.2. Khởi tạo quần thể

**a) Random initialization (mặc định):**
- Mỗi route được sinh bằng cách tạo hoán vị ngẫu nhiên
- Xoay để thành phố 0 đứng đầu
- Dùng rng riêng để đảm bảo tái lập kết quả

**b) Nearest-neighbor initialization:**
- Thuật toán tham lam: chọn thành phố chưa thăm gần nhất
- Nếu bằng nhau thì chọn thành phố có chỉ số nhỏ hơn
- Mỗi route NN được sinh từ điểm bắt đầu khác nhau

**c) Mixed initialization:**
- Kết hợp một phần route NN (25% mặc định)
- Phần còn lại là random
- Đặt nghiệm chất lượng tốt vào quần thể ban đầu

#### 2.2.3. Chọn cha mẹ (Selection)

**a) Tournament Selection (mặc định):**
- Lấy ngẫu nhiên k cá thể (k=3 mặc định)
- Chọn cá thể có chi phí thấp nhất
- Hai lần chọn cha mẹ độc lập nhau

**b) Rank Selection:**
- Sắp xếp cá thể từ tốt đến kém
- Gán trọng số P, P-1, ..., 1 theo thứ hạng
- Làm giảm áp lực chọn lọc, duy trì đa dạng

**c) Roulette Wheel Selection:**
- Chuyển chi phí thành trọng số: weight_i = 1 - cost_i / max_cost
- Cá thể chi phí thấp có xác suất được chọn lớn hơn

#### 2.2.4. Lai ghép (Crossover)

**a) Order Crossover - OX (mặc định):**
- Bảo tồn thứ tự tương đối của các thành phố
- Chọn ngẫu nhiên hai vị trí cắt left, right trên tail
- Sao chép đoạn [left:right] từ cha thứ nhất
- Điền các thành phố còn lại theo thứ tự từ cha thứ hai

```python
def order_crossover(parent1, parent2, rng):
    a, b = parent1[1:], parent2[1:]
    left, right = sorted(rng.sample(range(len(a)), 2))
    right += 1
    
    def child(first, second):
        result = [-1] * len(first)
        result[left:right] = first[left:right]
        used = set(first[left:right])
        values = [city for city in second[right:] + second[:right] if city not in used]
        positions = list(range(right, len(first))) + list(range(left))
        for position, value in zip(positions, values):
            result[position] = value
        return (0, *result)
    
    return child(a, b), child(b, a)
```

**b) Partially Mapped Crossover - PMX:**
- Giữ đoạn [left:right] từ cha thứ nhất
- Dùng ánh xạ giữa đoạn của hai cha mẹ để giải quyết xung đột

#### 2.2.5. Đột biến (Mutation)

**a) Inversion Mutation (mặc định):**
- Chọn ngẫu nhiên hai vị trí trên tail
- Đảo ngược thứ tự của đoạn giữa hai vị trí đó

**b) Swap Mutation:**
- Chọn ngẫu nhiên hai vị trí khác nhau
- Hoán đổi hai thành phố tại hai vị trí đó

**c) Insertion Mutation:**
- Lấy thành phố tại vị trí i ra khỏi route
- Chèn vào vị trí j

**d) Scramble Mutation:**
- Chọn ngẫu nhiên một đoạn trên tail
- Xáo trộn thứ tự các thành phố trong đoạn đó

```python
def mutate(route, rate, rng, method="inversion"):
    if rng.random() >= rate:
        return tuple(route)
    
    result = list(route)
    i, j = rng.sample(range(1, len(route)), 2)
    
    if method == "swap":
        result[i], result[j] = result[j], result[i]
    elif method == "insertion":
        result.insert(j, result.pop(i))
    else:
        i, j = sorted((i, j))
        segment = result[i:j+1]
        if method == "inversion":
            segment.reverse()
        else:  # scramble
            rng.shuffle(segment)
        result[i:j+1] = segment
    
    return tuple(result)
```

#### 2.2.6. Elitism và Global Best

**Elitism:**
- Bảo tồn elite_count cá thể tốt nhất
- Sao chép trực tiếp sang quần thể kế tiếp
- Không đánh giá lại (tái dùng fitness đã biết)

**Global Best Archive:**
- Mỗi lần route con được đánh giá
- Nếu chi phí nhỏ hơn global best hiện tại
- Archive được cập nhật ngay lập tức
- Kết quả cuối cùng là global best của toàn bộ lần chạy

#### 2.2.7. Điều kiện dừng

| Điều kiện | stopping_reason | Mô tả |
|-----------|----------------|-------|
| Hết số generation | MAX_ITERATIONS | Đạt min(generations, max_iterations) thế hệ hoàn chỉnh |
| Hết ngân sách đánh giá | MAX_EVALUATIONS | Tổng lần gọi route_length ≥ max_evaluations |
| Hết thời gian | TIME_LIMIT | Thời gian thực tế ≥ time_limit_seconds |
| Yêu cầu dừng | CANCELLED | stop_requested() trả True |
| Trì trệ | STAGNATION | stagnation_patience thế hệ liên tiếp không cải thiện |

#### 2.2.8. Các phương án nâng cao

**a) Stagnation Stopping:**
- Dừng thuật toán sớm khi không cải thiện
- Reset về 0 mỗi khi global best cải thiện

**b) Adaptive Mutation:**
- Điều chỉnh mutation rate động theo mức trì trệ và diversity
- Tăng tuyến tính theo stagnation
- Diversity ≤ 0.1 đặt pressure tối thiểu 0.5

**c) Bounded 2-opt Local Search:**
- Tìm kiếm cục bộ 2-opt theo chiến lược first-improvement
- Với mỗi cặp (i,j), thử đảo đoạn route[i..j]
- Chấp nhận ngay nếu cải thiện chi phí
- Mỗi probe 2-opt gọi một lần route_length đầy đủ

---

## CHƯƠNG 3. THUẬT TOÁN ELEPHANT HERDING OPTIMIZATION

### 3.1. Tổng quan về Elephant Herding Optimization

#### 3.1.1. Khái niệm EHO

Elephant Herding Optimization (EHO) là thuật toán tối ưu hóa lấy cảm hứng từ hành vi sống theo đàn của loài voi. Quần thể được chia thành nhiều nhóm nhỏ gọi là Clan, trong đó mỗi cá thể đại diện cho một lời giải và được đánh giá bằng hàm mục tiêu.

#### 3.1.2. Nguyên lý hành vi đàn voi

- Mỗi Clan gồm một cá thể dẫn đầu gọi là Matriarch
- Các cá thể trong đàn cập nhật vị trí dựa trên Matriarch
- Matriarch được điều chỉnh theo tâm của Clan
- Cá thể có fitness kém nhất thực hiện cơ chế Separation
- Ba cơ chế này cân bằng khai thác nghiệm tốt và khám phá vùng mới

#### 3.1.3. Các thành phần chính

**Thành phần EHO:**
- **Clan:** Nhóm các cá thể voi trong quần thể
- **Matriarch:** Cá thể có nghiệm tốt nhất trong mỗi clan
- **Clan center:** Tâm đại diện cho các cá thể trong clan
- **Clan updating operator:** Cập nhật cá thể dựa trên matriarch và tâm clan
- **Separating operator:** Thay thế cá thể kém để duy trì đa dạng

**Công thức EHO liên tục:**

Vị trí voi thường:
```
p(t+1)[i,c] = p(t)[i,c] + αr(p(t)[best,c] - p(t)[i,c])
```

Matriarch:
```
p(t+1)[best,c] = βp(t)[center,c]
p(t)[center,c] = (1/m)Σp(t)[i,c]
```

Separation:
```
p(t+1)[worst,c] = pmin,c + r(pmax,c - pmin,c + 1)
```

### 3.2. Áp dụng EHO cho bài toán TSP

| Thành phần EHO | Cách áp dụng trong D-EHO |
|----------------|--------------------------|
| Cá thể | Một tour gồm thứ tự các thành phố, cố định thành phố 0 ở đầu |
| Clan | Nhóm gồm m tour |
| Matriarch | Tour có tổng quãng đường ngắn nhất trong clan |
| Tâm clan | Tour medoid có tổng khoảng cách Hamming nhỏ nhất |
| Cập nhật α | Dùng guided-swap đưa các tour về matriarch |
| Cập nhật β | Dùng guided-swap đưa matriarch về tâm clan |
| Separation | Thay các tour kém nhất bằng hoán vị ngẫu nhiên hợp lệ |
| Elitism | Lưu nghiệm tốt nhất của từng clan và toàn quần thể |

#### 3.2.1. Biểu diễn nghiệm và hàm mục tiêu

Tour được biểu diễn:
```
π = (0, π₁, π₂, ..., πₙ₋₁)
```

Hàm mục tiêu:
```
L(π) = Σ(i=0 to n-2) D[πᵢ, πᵢ₊₁] + D[πₙ₋₁, π₀]
```

#### 3.2.2. Phân chia quần thể thành các Clan

```python
@dataclass(frozen=True)
class Clan:
    members: tuple[Route, ...]
    costs: tuple[float, ...]
    
    def best_index(self) -> int:
        return min(range(self.size), 
                  key=lambda index: (self.costs[index], index))
    
    def center(self) -> Route:
        return self.members[self.center_index()]
```

Matriarch được xác định:
```
T[best,c] = argmin L(Tᵢ) for Tᵢ ∈ Clanc
```

#### 3.2.3. Cập nhật Matriarch

**Khoảng cách Hamming:**
```
dH(π, σ) = Σ(j=1 to n-1) [πⱼ ≠ σⱼ]
```

**Tâm clan (Hamming Medoid):**
```
T[center,c] = argmin Σ dH(π, σ) for π,σ ∈ Clanc
```

Nếu có nhiều tour cùng khoảng cách, ưu tiên tour có chi phí thấp hơn.

```python
def center_index(self) -> int:
    distance_totals = [0] * self.size
    for first in range(self.size):
        for second in range(first + 1, self.size):
            distance = hamming_distance(self.members[first], 
                                       self.members[second])
            distance_totals[first] += distance
            distance_totals[second] += distance
    
    return min(range(self.size),
              key=lambda index: (distance_totals[index], 
                               self.costs[index], index))
```

#### 3.2.4. Di chuyển voi thường (Clan Updating Operator)

Các cá thể voi thường được cập nhật bằng **Guided-Swap**, đưa route hiện tại tiến gần route Matriarch.

**Xác định số lần hoán đổi:**
```
diff = {j | πⱼ ≠ targetⱼ, j ≥ 1}
k = ⌊α · r · |diff|⌋
```

Trong đó: r ~ U[0,1), α ∈ [0,1] là hệ số cập nhật.

**Quy trình Guided-Swap:**
1. Xác định các vị trí khác nhau giữa hai route
2. Xáo trộn danh sách vị trí khác nhau
3. Chọn vị trí cần cập nhật và hoán đổi thành phố
4. Lặp lại cho đến khi đủ số lần hoán đổi

```python
def guided_swap(source, target, strength, rng):
    n = len(source)
    diff = [i for i in range(1, n) if source[i] != target[i]]
    steps = floor(strength * rng.random() * len(diff))
    
    if steps <= 0:
        return tuple(source)
    
    result = list(source)
    pos = [0] * n
    for idx, city in enumerate(result):
        pos[city] = idx
    
    rng.shuffle(diff)
    swaps_done = 0
    
    for i in diff:
        if swaps_done >= steps:
            break
        desired_city = target[i]
        current_city = result[i]
        if current_city == desired_city:
            continue
        j = pos[desired_city]
        result[i], result[j] = desired_city, current_city
        pos[desired_city] = i
        pos[current_city] = j
        swaps_done += 1
    
    return tuple(result)
```

#### 3.2.5. Tách đàn (Separating Operator)

**Mục đích:** Duy trì tính đa dạng của quần thể và hạn chế hội tụ sớm vào nghiệm tối ưu cục bộ.

**Quy trình:**
1. Bảo vệ Matriarch: Loại bỏ chỉ số của cá thể Matriarch khỏi danh sách có thể bị thay thế
2. Xác định cá thể kém nhất: Chọn separation_count_per_clan cá thể có cost cao nhất
3. Giữ lại cá thể không bị tách
4. Tạo cá thể mới: Thay thế bằng hoán vị ngẫu nhiên hợp lệ
5. Tạo clan mới: Kết hợp routes được giữ lại và routes mới

```python
protected = set(protected_indices)
eligible = [index for index in range(clan_size) if index not in protected]
worst_indices = sorted(eligible, 
                      key=lambda i: (-costs[i], i))[:separation_count]

for idx in worst_indices:
    new_clan[idx] = random_permutation(n, rng)
```

#### 3.2.6. Cơ chế bảo tồn nghiệm tốt nhất (Elitism)

**Hai cấp độ lưu trữ:**
- **Clan Archive:** Lưu trữ route tốt nhất từng được tìm thấy của mỗi clan
- **Global Best:** Lưu trữ route có cost nhỏ nhất trong toàn bộ quá trình chạy

**Quá trình cập nhật:**
1. Khởi tạo Archive: Sau khi khởi tạo quần thể, route tốt nhất của mỗi clan được lưu vào Clan Archive
2. Đánh giá candidate: So sánh cost của route với Clan Archive
3. Cập nhật Global Best: Candidate được so sánh với nghiệm tốt nhất toàn cục
4. Khôi phục nghiệm tốt nhất: Nếu route Archive bị mất, đưa route này trở lại clan
5. Commit generation: Generation mới trở thành trạng thái chính thức

```python
def _preserve_clan_best(clan, best_route, best_distance):
    if best_route in clan.members:
        return clan
    
    leader_index = clan.best_index()
    replacement_index = clan.worst_indices(1, 
                                          protected_indices=(leader_index,))[0]
    
    members = list(clan.members)
    costs = list(clan.costs)
    members[replacement_index] = best_route
    costs[replacement_index] = best_distance
    
    return Clan(tuple(members), tuple(costs))
```

### 3.3. Quy trình hoạt động của D-EHO

#### 3.3.1. Pseudocode

```
Input: TSP distance matrix D, clan_count N_c, elephants_per_clan m,
       alpha, beta, separation_count s, stopping limits
Output: best valid tour and its distance

Initialize N_c clans with m random valid tours each
Evaluate all initial tours
For each clan: archive its best tour
Set global_best to the best initial tour

While no stopping condition is met:
    Create an empty next_population
    For each clan:
        Select the lowest-cost tour as matriarch
        Compute the clan Hamming medoid
        Select up to s worst tours, excluding the matriarch
        
        For each member index i:
            If i is the matriarch:
                candidate = guided_swap(matriarch, medoid, beta)
            Else if i is selected for separation:
                candidate = random valid permutation
            Else:
                candidate = guided_swap(member[i], matriarch, alpha)
            
            Evaluate candidate once
            Update clan archive and global_best if improved
            Append candidate to next clan
    
    If every clan was completed:
        Restore archived clan best when needed
    
    If a full generation was completed:
        Commit next_population
    Else:
        Keep the last committed population and stop

Return global_best and run metadata
```

### 3.4. Triển khai thuật toán trong chương trình

#### 3.4.1. Cấu trúc các module

| Module | Trách nhiệm |
|--------|-------------|
| solver.py | Khởi tạo clan, điều khiển vòng lặp, cập nhật archive và trả kết quả |
| clans.py | Quản lý clan, chọn best/worst và tính Hamming Medoid |
| discrete_ops.py | Tính Hamming distance và thực hiện guided-swap |
| separation.py | Chọn route kém và sinh permutation mới |
| objective.py | Kiểm tra route và tính tổng khoảng cách |

#### 3.4.2. Các tham số cấu hình

| Tham số | Giá trị mặc định | Ý nghĩa |
|---------|------------------|---------|
| clan_count | Theo cấu hình | Số lượng clan |
| elephants_per_clan | Theo cấu hình | Số cá thể mỗi clan |
| alpha | 0.7 | Hệ số cập nhật cá thể |
| beta | 0.3 | Hệ số cập nhật Matriarch |
| separation_count_per_clan | 1 | Số cá thể tách mỗi clan |
| seed | Theo cấu hình | Giá trị khởi tạo ngẫu nhiên |
| iterations | Theo cấu hình | Số thế hệ chạy |

**Điều kiện kiểm tra:**
- Mỗi clan có ít nhất 3 cá thể và có tối thiểu 2 clan
- alpha, beta thuộc khoảng [0, 1]
- Số cá thể separation phải nhỏ hơn kích thước clan
- Evaluation budget phải đủ để đánh giá quần thể ban đầu

#### 3.4.3. Điều kiện dừng

Solver có thể dừng khi:
- Đạt giới hạn thế hệ (iterations)
- Đạt max_evaluations
- Đạt time_limit_seconds
- Callback yêu cầu dừng

Nếu chạy đủ G thế hệ, số objective evaluations là:
```
N_c × m × (G + 1)
```

### 3.5. Nhận xét và giới hạn của D-EHO

#### 3.5.1. Ưu điểm

- Giữ các thành phần có ý nghĩa của EHO (clan, matriarch, cập nhật clan và separation)
- Mọi thao tác đều tạo route hợp lệ mà không cần repair
- Archive theo clan và global best hạn chế mất nghiệm tốt
- Hỗ trợ seed, giới hạn số lần đánh giá và giới hạn thời gian

#### 3.5.2. Hạn chế

- Thay phép toán vector bằng guided-swap, Hamming medoid và permutation ngẫu nhiên
- Không phải tương đương đại số với EHO liên tục
- Hamming medoid xét vị trí thành phố, không trực tiếp tối ưu mức tương đồng cạnh
- Chỉ hỗ trợ symmetric TSP
- Heuristic không bảo đảm tìm optimum toàn cục

#### 3.5.3. Khả năng áp dụng cho TSP

Implementation phù hợp với phạm vi đề tài hiện tại:
- TSP đối xứng, có ít nhất ba thành phố
- Ma trận khoảng cách hữu hạn, không âm, đối xứng, đường chéo bằng 0
- Cố định thành phố 0 ở đầu route loại bỏ các biểu diễn quay vòng tương đương

D-EHO đã có thể dùng làm solver rời rạc độc lập để minh họa và thực nghiệm EHO trên TSP đối xứng trong phạm vi dữ liệu của dự án.

---

## CHƯƠNG 4. KẾT QUẢ THỰC NGHIỆM

### 4.1. Thiết kế thực nghiệm

#### 4.1.1. Bộ dữ liệu

Dự án sử dụng bảy bộ dữ liệu ma trận khoảng cách đối xứng với quy mô từ nhỏ đến trung bình:

| Tên file | Số thành phố |
|----------|--------------|
| 03Cities-6.txt | 3 |
| 04Cities-189.txt | 4 |
| 06Cities-1248.txt | 6 |
| 15Cities-1194.txt | 15 |
| 26Cities-937.txt | 26 |
| 42Cities-699.txt | 42 |
| 48Cities-33523.txt | 48 |

#### 4.1.2. Cấu hình thực nghiệm

**Thực nghiệm được tổ chức thành ba nhóm:**

**Experiment 1-2 (so sánh toán tử):**
- Bài 15 thành phố, quần thể 40
- Ngân sách 2,000 evaluations
- 5 seed [11, 23, 37, 53, 71]
- OFAT (One Factor At a Time)

**Experiment 3 (phân phối kết quả):**
- Sáu bộ dữ liệu (3-48 thành phố)
- Quần thể 40, ngân sách 4,000 evaluations
- 5 seed

**Experiment 4 (các biến thể nâng cao):**
- Bốn bài toán (15, 26, 42, 48 thành phố)
- Quần thể 40, ngân sách 4,000 evaluations
- 5 seed, 6 biến thể

**Cấu hình baseline:**
```
population_size = 40
generations = 2000
max_iterations = 2000
selection_method = tournament (k=3)
crossover_method = ox
crossover_rate = 0.9
mutation_method = inversion
mutation_rate = 0.15
elite_count = 2
initialization = random
local_search = disabled
seed set = [11, 23, 37, 53, 71]
max_evaluations = 2000 hoặc 4000
```

### 4.2. Kết quả so sánh toán tử trên bài 15 thành phố

| Biến thể | Mean distance | Trung vị | Độ lệch chuẩn |
|----------|---------------|----------|---------------|
| Cơ sở (tournament + OX + inversion) | 1235.0 | 1225 | 43.86 |
| Rank selection | 1413.6 | 1402 | 81.79 |
| Roulette selection | 1400.8 | 1340 | 158.48 |
| PMX thay OX | 1275.4 | 1279 | 38.34 |
| Swap mutation | 1317.0 | 1289 | 113.40 |
| Insertion mutation | 1319.8 | 1287 | 68.16 |
| Scramble mutation | 1473.0 | 1391 | 152.78 |

**Nhận xét:**
- Cấu hình cơ sở (tournament + OX + inversion) cho kết quả trung bình tốt nhất
- PMX cho trung vị cao hơn cơ sở một chút nhưng độ lệch chuẩn thấp hơn, gợi ý kết quả ổn định hơn
- Rank và roulette selection cho kết quả kém hơn đáng kể; độ lệch chuẩn của roulette đặc biệt cao
- Scramble mutation cho kết quả kém nhất, có thể do phá vỡ cấu trúc hành trình quá mạnh

### 4.3. Phân phối kết quả theo kích thước bài toán

| Số thành phố | Min | Mean | Median | Max | Std | Tỷ lệ đạt min quan sát |
|--------------|-----|------|--------|-----|-----|------------------------|
| 3 | 6 | 6 | 6 | 6 | 0 | 100% |
| 6 | 1248 | 1248 | 1248 | 1248 | 0 | 100% |
| 15 | 1194 | 1200.2 | 1194 | 1225 | 13.86 | 80% |
| 26 | 969 | 1046 | 1034 | 1186 | 82.85 | 20% |
| 42 | 1102 | 1151.6 | 1133 | 1211 | 49.75 | 20% |
| 48 | 51215 | 55404.6 | 55339 | 59638 | 3031.79 | 20% |

**Nhận xét:**
- Với các bài rất nhỏ (3 và 6 thành phố), GA tìm được nghiệm tốt nhất trong 100% lần chạy
- Từ bài 15 thành phố trở đi, bắt đầu xuất hiện sự biến động
- Từ bài 26 thành phố trở lên, tỷ lệ hit giảm còn 20% và độ lệch chuẩn tăng mạnh
- "Tỷ lệ đạt min quan sát" không phải xác suất tìm optimum toàn cục

### 4.4. Khởi tạo nâng cao, Adaptive Mutation và 2-opt

| Số thành phố | Control | PMX | Mixed 25% | NN | Adaptive | GA+2-opt |
|--------------|---------|-----|-----------|-----|----------|----------|
| 15 | 1200.2 | 1219.2 | 1194.0 | 1194.0 | 1228.0 | 1336.2 |
| 26 | 1046.0 | 1054.0 | 958.6 | 961.8 | 1016.4 | 1388.8 |
| 42 | 1151.6 | 1114.8 | 811.8 | 782.2 | 1112.4 | 1750.2 |
| 48 | 55404.6 | 55073.2 | 37222.2 | 36559.0 | 53912.2 | 81489.6 |

**Phân tích kết quả:**

**NN và Mixed initialization:**
- Cho kết quả tốt hơn rõ rệt khi bài toán lớn hơn
- Tại bài 48 thành phố: mixed (37222.2) và NN (36559.0) thấp hơn đáng kể so với control (55404.6)
- Khởi tạo NN có thêm chi phí tính toán trong runtime

**GA+2-opt:**
- Cho kết quả kém hơn control ở cả 4 bài
- Lý do: mỗi probe 2-opt gọi một lần route_length đầy đủ
- Tại bài 48 thành phố: 2-opt tiêu thụ trung bình 3163.4 trong 4000 evaluations
- Chỉ commit được khoảng 20.6 thế hệ so với 104 thế hệ của control
- Đánh đổi: local search cải thiện từng cá thể nhưng làm giảm số thế hệ được khám phá

**Adaptive Mutation:**
- Kết quả không nhất quán
- Tốt hơn control ở một số bài nhưng kém hơn ở bài khác
- Tùy chọn vẫn tắt mặc định

### 4.5. Benchmark trên bảy bộ dữ liệu

Benchmark đầy đủ: 7 bộ dữ liệu × 5 seed = 35 lần chạy
- Mỗi lần: 6,000 evaluations, quần thể 80, cấu hình cơ sở

| Số thành phố | Mean distance | Độ lệch chuẩn | Runtime trung bình (giây) |
|--------------|---------------|---------------|---------------------------|
| 3 | 6 | 0 | 0.0440 |
| 4 | 189 | 0 | 0.0471 |
| 6 | 1248 | 0 | 0.0508 |
| 15 | 1200.2 | 13.86 | 0.0642 |
| 26 | 1056.4 | 72.84 | 0.0818 |
| 42 | 1166.2 | 26.28 | 0.1012 |
| 48 | 54194.4 | 3861.50 | 0.1154 |

**Nhận xét:**
- Tất cả 35 lần chạy hoàn thành hợp lệ (is_valid=True)
- Bài nhỏ (3, 4, 6 thành phố): Kết quả hoàn toàn ổn định (độ lệch chuẩn 0)
- Bài lớn hơn: Độ lệch chuẩn tăng theo kích thước bài
- Runtime: Tăng tuyến tính từ ~44ms (3 thành phố) đến ~115ms (48 thành phố)
- Chưa có known optimum được xác minh cho các bài lớn

---

## CHƯƠNG 5. KẾT LUẬN

### 5.1. Các kết quả đạt được

Đồ án đã triển khai thành công hai thuật toán metaheuristic cho bài toán TSP:

**1. Genetic Algorithm (GA):**
- Cài đặt đầy đủ với nhiều biến thể toán tử
- Hỗ trợ 3 phương pháp selection: Tournament, Rank, Roulette Wheel
- Hỗ trợ 2 phương pháp crossover: Order Crossover (OX), Partially Mapped Crossover (PMX)
- Hỗ trợ 4 phương pháp mutation: Inversion, Swap, Insertion, Scramble
- Hỗ trợ 3 phương pháp khởi tạo: Random, Nearest-Neighbor, Mixed
- Cài đặt Elitism, Global Best Archive, Adaptive Mutation, Bounded 2-opt Local Search
- Hỗ trợ điều kiện dừng linh hoạt: generations, max_evaluations, time_limit, stagnation

**2. Discrete Elephant Herding Optimization (D-EHO):**
- Điều chỉnh EHO cho không gian hoán vị
- Cài đặt Guided-Swap để cập nhật vị trí rời rạc
- Tính Hamming Medoid làm tâm clan
- Cơ chế Separation với permutation ngẫu nhiên
- Elitism hai cấp: Clan Archive và Global Best

**3. Kết quả thực nghiệm:**
- Benchmark trên 7 bộ dữ liệu với 35 lần chạy hoàn thành hợp lệ
- So sánh hiệu quả của các toán tử GA
- Phân tích ảnh hưởng của tham số
- Đánh giá các phương án nâng cao

**4. Giao diện và công cụ:**
- GUI Tkinter cho phép thử nghiệm dễ dàng
- CLI hỗ trợ validate dữ liệu và chạy benchmark
- Jupyter notebooks cho phân tích chi tiết

### 5.2. Những hạn chế và hướng phát triển

**Hạn chế hiện tại:**

1. **Về thuật toán:**
   - Chỉ hỗ trợ Symmetric TSP
   - Không bảo đảm tìm optimum toàn cục
   - D-EHO chưa có so sánh trực tiếp với GA trong cùng điều kiện

2. **Về dữ liệu:**
   - Chưa có known optimum được xác minh cho các bài lớn
   - Bộ dữ liệu giới hạn (tối đa 48 thành phố)

3. **Về thực nghiệm:**
   - GA+2-opt cần cân bằng lại evaluation budget
   - Adaptive Mutation cần điều chỉnh tham số
   - Chưa có so sánh với các solver khác (OR-Tools, Concorde)

**Hướng phát triển:**

1. **Mở rộng bài toán:**
   - Hỗ trợ Asymmetric TSP
   - Hỗ trợ TSP with Time Windows
   - Hỗ trợ Multiple TSP

2. **Cải tiến thuật toán:**
   - Hybrid GA-EHO kết hợp ưu điểm của cả hai
   - Tích hợp thêm local search hiệu quả (Lin-Kernighan, 3-opt)
   - Parallel/Distributed GA để tăng tốc

3. **Thực nghiệm nâng cao:**
   - So sánh với TSPLIB benchmark instances
   - So sánh với các solver state-of-the-art
   - Phân tích chi tiết complexity và convergence rate

4. **Công cụ:**
   - Visualization tool cho evolution process
   - Auto-tuning tham số bằng Bayesian Optimization
   - Web interface để demo online

---

## TÀI LIỆU THAM KHẢO

[1] J. H. Holland, *Adaptation in Natural and Artificial Systems*, University of Michigan Press, Ann Arbor, MI, USA, 1975.

[2] D. E. Goldberg, *Genetic Algorithms in Search, Optimization, and Machine Learning*, Addison-Wesley, Reading, MA, USA, 1989.

[3] D. L. Applegate, R. E. Bixby, V. Chvátal, and W. J. Cook, *The Traveling Salesman Problem: A Computational Study*, Princeton University Press, Princeton, NJ, USA, 2006.

[4] I. M. Oliver, D. J. Smith, and J. R. C. Holland, "A study of permutation crossover operators on the traveling salesman problem," in *Proc. 2nd Int. Conf. Genetic Algorithms*, 1987, pp. 224–230.

[5] G. Wang, S. Deb, and L. dos Santos Coelho, "Elephant herding optimization," in *Proc. 3rd Int. Symp. Computational and Business Intelligence (ISCBI)*, Bali, Indonesia, 2015, pp. 1–5.

[6] A. Slowik, Ed., *Swarm Intelligence Algorithms: A Tutorial*, CRC Press, Boca Raton, FL, USA, 2020.

[7] T. Stützle, "Local search algorithms for combinatorial problems," Ph.D. dissertation, Darmstadt University of Technology, 1998.

---

## PHỤ LỤC

### A. Hướng dẫn cài đặt

#### Yêu cầu môi trường
- Python 3.11 trở lên
- Hệ điều hành: Windows 10/11, macOS, Linux
- RAM: Tối thiểu 4GB

#### Cài đặt môi trường

**Bước 1: Tạo virtual environment**
```bash
python --version  # Kiểm tra Python >= 3.11
python -m venv .venv
```

**Bước 2: Kích hoạt môi trường**

Windows (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

**Bước 3: Cài đặt thư viện**
```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

#### Chạy chương trình

**Giao diện GUI:**
```bash
python -m ga_eho_tsp.gui
```

**Hoặc sử dụng script Demo:**
```bash
python Demo.py
```

**Kiểm tra dữ liệu:**
```bash
python -m ga_eho_tsp.cli validate
```

### B. Cấu trúc repository

```
ga-eho-tsp/
├── data/                    # Bộ dữ liệu TSP
├── src/ga_eho_tsp/         # Source code chính
│   ├── algorithms/         # GA và EHO implementation
│   │   ├── ga/            # Genetic Algorithm
│   │   └── eho/           # Elephant Herding Optimization
│   ├── domain/            # Models và objective functions
│   ├── experiments/       # Benchmark utilities
│   ├── gui/              # Tkinter GUI
│   └── cli.py            # Command-line interface
├── Experiment/            # Jupyter notebooks
├── docs/                 # Documentation
├── tests/                # Unit tests
└── Demo.py              # Demo script
```

### C. Phân công công việc nhóm

| Thành viên | Nhiệm vụ |
|------------|----------|
| Trương Thành Đạt | Triển khai GA core algorithms, GUI, tổng hợp báo cáo |
| Nguyễn Tấn Khiêm | Triển khai EHO algorithms, experiments |
| Nguyễn Phương Chinh | Data processing, validation, documentation |
| Lại Thành Đạt | Testing, benchmarking, visualization |
