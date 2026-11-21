# Phân tích chiến lược rời rạc hóa Elephant Herding Optimization (Discrete EHO) cho bài toán TSP

Tài liệu này giải quyết **Issue #5** (*Research & document discrete EHO adaptation strategies for TSP permutations*), phân tích cơ sở lý thuyết từ Chương 12 (*Elephant Herding Optimization*, tr. 149–162) trong giáo trình *Swarm Intelligence Algorithms: A Tutorial* (Meena, Yang & Slowik, 2020) và bài báo gốc (Wang, Deb & Coelho, 2015), từ đó lựa chọn và chuẩn hóa cơ chế rời rạc hóa phù hợp với hợp đồng TSP của dự án (`GUIDELINES.md`, `docs/algorithm_eho.md`).

---

## 1. EHO gốc trong không gian liên tục và rào cản với TSP

### 1.1. Ba quy tắc nền tảng và hệ phương trình gốc (Mục 12.2.1 & 12.2.2)

Trong EHO nguyên bản trên không gian thực $\mathbb{R}^D$, quần thể voi được chia thành $C$ bầy (**clan**) có kích thước cố định $n_c$, vận hành qua hai toán tử cốt lõi:

1. **Toán tử cập nhật bầy (Clan Updating Operator — Mục 12.2.1):**
   - Với **voi thường** $j$ trong clan $c$ ($p_{jc}^t \neq p_{\text{best}, c}$), vị trí cập nhật hướng về voi đầu đàn (**matriarch**) $p_{\text{best}, c}$:
     $$p_{jc}^{t+1} = p_{jc}^{t} + \alpha \times (p_{\text{best}, c} - p_{jc}^{t}) \times r \tag{12.1}$$
     trong đó $\alpha \in [0, 1]$ là hệ số ảnh hưởng của matriarch và $r \sim U(0, 1)$.
   - Với **voi đầu đàn (matriarch)** ($p_{jc}^t = p_{\text{best}, c}$), vị trí cập nhật theo tâm của cả clan $p_{\text{center}, c}$:
     $$p_{jc}^{t+1} = \beta \times p_{\text{center}, c}, \qquad p_{\text{center}, c} = \frac{1}{n_c} \sum_{j=1}^{n_c} p_{jc}^{t} \tag{12.2–12.3}$$
     trong đó $\beta \in [0, 1]$ là hệ số điều chỉnh ảnh hưởng của tâm clan.
2. **Toán tử tách bầy (Separating Operator — Mục 12.2.2):**
   - Với **voi có độ thích nghi tệ nhất** trong clan $c$, cá thể này rời bầy và được thay thế ngẫu nhiên trong miền tìm kiếm $[p_{\min, c}, p_{\max, c}]$:
     $$p_{\text{worst}, jc}^{t+1} = p_{\min, c} + \text{rand} \times (p_{\max, c} - p_{\min, c} + 1) \tag{12.4}$$
     với $\text{rand} \sim U(0, 1)$.

> **Lưu ý kỹ thuật từ Algorithm 11 & Listing 12.1–12.2 (Slowik, 2020):**
> - Trong các ví dụ số của sách (như hàm Rastrigin ở Mục 12.5), cập nhật matriarch theo Công thức (12.2) có thể làm nghiệm của matriarch **xấu đi tạm thời** để khám phá quanh tâm clan; do đó lời giải tốt nhất toàn cục `pbest` luôn được bảo toàn riêng ngoài quần thể (elitism/archive).
> - Trong Công thức (12.4), số hạng `+ 1` trong $(p_{\max, c} - p_{\min, c} + 1)$ là điểm đặc thù của công thức gốc có thể gây vượt cận $p_{\max, c}$ trong không gian liên tục nếu không cắt biên (clamping).

### 1.2. Vì sao không thể áp dụng trực tiếp lên TSP hoán vị?

Theo hợp đồng domain của dự án (`src/ga_eho_tsp/domain/objective.py`), mỗi lời giải TSP là một `Route = tuple[int, ...]` độ dài $n$ thỏa mãn:
- Là một **hoán vị** (song ánh) của tập $\{0, 1, \dots, n-1\}$.
- **Cố định đỉnh xuất phát:** `route[0] == 0` để loại bỏ $n$ phép xoay vòng tương đương.

Áp dụng trực tiếp các Công thức (12.1)–(12.4) thất bại vì 4 lý do:
1. **Phá vỡ ràng buộc song ánh:** Phép hiệu $(p_{\text{best}} - p_{jc}^t)$ và nhân vô hướng $\alpha \cdot r$ sinh ra số thực, số âm hoặc chỉ số thành phố trùng lặp/ngoài phạm vi $[0, n-1]$.
2. **Không tồn tại trung bình số học của hoán vị:** Tổng $\frac{1}{n_c} \sum p_{jc}^t$ không định nghĩa một tour hợp lệ.
3. **Không cần biên liên tục cho Separation:** Miền tìm kiếm của TSP là tập hoán vị hữu hạn $(n-1)!$ có `route[0] == 0`, không phải hộp chữ nhật $[p_{\min}, p_{\max}]^D$.
4. **Ràng buộc vị trí cố định `route[0] == 0`:** Mọi toán tử rời rạc phải chỉ tác động lên phần đuôi `route[1:]`.

---

## 2. Phân tích so sánh các chiến lược rời rạc hóa Clan Updating

Để chuyển hóa khái niệm *"di chuyển từ nghiệm `source` về phía nghiệm mục tiêu `target` với cường độ $\gamma \in [0, 1]$"* (trong đó $\gamma = \alpha$ cho voi thường và $\gamma = \beta$ cho matriarch), ba hướng tiếp cận chính được đánh giá cùng một hướng đối chiếu phụ (Random-Key):

### 2.1. Hướng 1: Guided Crossover (OX / PMX với tỉ lệ $\alpha$)

- **Cơ chế:** Xem phép di chuyển về `pbest` như một phép lai ghép Order Crossover (OX) hoặc Partially Mapped Crossover (PMX) giữa `current` và `pbest`, trong đó chiều dài đoạn gen lấy từ `pbest` tỉ lệ với $\alpha \cdot r$ (hoặc xác suất áp dụng crossover là $\alpha$).
- **Ưu điểm:**
  - Tận dụng trực tiếp các toán tử lai ghép bảo toàn hoán vị đã có sẵn ở nhánh GA (`order_crossover`, `partially_mapped_crossover`).
  - Bảo toàn tốt các đoạn cạnh liền kề (sub-tours) của `pbest` nhờ đặc tính giữ thứ tự tương đối của OX.
- **Nhược điểm:**
  - **Khó ánh xạ định lượng chính xác tham số $\alpha$:** Với OX/PMX hai điểm cắt truyền thống, kích thước đoạn cắt phân bố ngẫu nhiên; việc ép chiều dài đoạn theo $\alpha$ làm thay đổi bản chất toán tử và không đảm bảo tính đơn điệu giảm khoảng cách tới `pbest`.
  - **Nhòe ranh giới giữa GA và EHO:** Làm EHO trở thành một biến thể lai ghép kiểu GA có cấu trúc clan, giảm giá trị học thuật khi so sánh hai họ thuật toán độc lập (Tiến hóa vs. Bầy đàn) trong dự án.
  - **Phụ thuộc chéo không mong muốn:** Vi phạm nguyên tắc tách biệt module trong `docs/eho_handoff.md` (EHO không import GA private internals).

### 2.2. Hướng 2: $\alpha$-based Swap / Guided Swap *(Phương án được chọn)*

- **Cơ chế:**
  1. Đo độ sai khác giữa `source` và `target` trên phần đuôi `1..n-1` bằng khoảng cách Hamming:
     $$D = \{ i \in \{1, \dots, n-1\} \mid \text{source}[i] \neq \text{target}[i] \}, \qquad H(\text{source}, \text{target}) = |D|$$
  2. Tính số bước hoán đổi có định hướng:
     $$k = \lfloor \gamma \cdot r \cdot H(\text{source}, \text{target}) \rfloor, \qquad r \sim U(0, 1), \; \gamma \in \{\alpha, \beta\}$$
  3. Xáo trộn ngẫu nhiên tập chỉ số sai khác $D$, lần lượt duyệt từng vị trí $i \in D$ (tối đa $k$ lần swap thực tế): tìm vị trí hiện tại $j$ của thành phố `target[i]` trong `source` thông qua bảng tra cứu ngược `pos[city] = idx`, sau đó hoán đổi `result[i]` và `result[j]` và cập nhật `pos`.
- **Ưu điểm:**
  - **Ánh xạ trực quan, đơn điệu theo $\alpha, \beta$:** Số phép swap tỉ lệ trực tiếp với $\gamma \cdot r \cdot H$; tại biên $\gamma = 0$ giữ nguyên `source`, tại $\gamma = 1$ tiến thẳng về `target`.
  - **Luôn bảo toàn tính hợp lệ của hoán vị:** Mỗi phép swap là một phép thế sơ cấp trên tập $\{1, \dots, n-1\}$, tuyệt đối không tạo thành phố trùng/thiếu và không bao giờ chạm vào `index 0`.
  - **Đảm bảo tiến gần mục tiêu:** Mỗi bước swap đặt ít nhất 1 vị trí $i$ về đúng `target[i]` (và có thể vô tình khớp thêm vị trí $j$), nên $H(\text{next}, \text{target}) \le H(\text{source}, \text{target})$.
  - **Hiệu năng tuyến tính $O(n)$:** Nhờ mảng ánh xạ ngược `pos`, mỗi bước swap chỉ tốn $O(1)$ thay vì $O(n)$ tìm kiếm tuyến tính; toàn bộ toán tử chạy trong $O(n)$.
- **Nhược điểm:**
  - Mỗi phép swap theo vị trí có thể phá vỡ 2–4 cạnh đang tốt trong tour TSP nếu chỉ xét theo chỉ số vị trí.
  - Tính chất dựa trên Hamming chưa nhận diện tính đối xứng đảo chiều tour trong Symmetric TSP (phân tích chi tiết ở Mục 4.3).

### 2.3. Hướng 3: Insertion Guided

- **Cơ chế:** Trích xuất các cạnh $(u, v)$ xuất hiện trong `pbest` nhưng chưa có trong `current`, sau đó với xác suất $\alpha$, rút thành phố $v$ ra khỏi vị trí hiện tại trong `current` và chèn ngay sau $u$.
- **Ưu điểm:**
  - Tác động trực tiếp lên cấu trúc **cạnh (edges)** — yếu tố quyết định trực tiếp tổng độ dài tour TSP.
  - Phù hợp tốt với Symmetric TSP (có thể xét cạnh vô hướng $\{u, v\}$).
- **Nhược điểm:**
  - **Xung đột chuỗi chèn & chi phí sửa lỗi:** Chèn nhiều cạnh của `pbest` liên tiếp có thể tạo chu trình con (sub-tour) hoặc ghi đè cạnh vừa chèn trước đó, đòi hỏi bước repair phức tạp hoặc cấu trúc đồ thị trung gian.
  - **Chi phí thực thi cao hơn:** Thao tác pop/insert trên mảng tốn $O(n)$ cho mỗi lần chèn, dẫn đến $O(k \cdot n) = O(n^2)$ trong trường hợp xấu nhất nếu không dùng danh sách liên kết kép.
  - **Khó kiểm soát biên $\alpha = 1$:** Không dễ đảm bảo $\alpha = 1$ luôn hội tụ chính xác về `target` do thứ tự chèn ảnh hưởng lẫn nhau.

### 2.4. Đối chiếu phụ: Random-Key / Smallest Position Value (SPV)

- **Cơ chế:** Mã hóa mỗi voi là vector số thực $x \in \mathbb{R}^{n-1}$, chạy nguyên Công thức (12.1)–(12.4) rồi giải mã thành hoán vị bằng cách sắp xếp chỉ số theo thứ tự tăng dần của $x$.
- **Lý do loại bỏ:** Tốn $O(n \log n)$ sắp xếp cho mỗi lần giải mã; không gian biểu diễn dư thừa vô hạn (nhiều vector thực khác nhau ánh xạ về cùng một tour) gây nhiễu bước nhảy và tốn ngân sách đánh giá (`evaluations`) cho các nghiệm trùng lặp; đồng thời không tận dụng trực tiếp cấu trúc `Route` của domain dự án.

### 2.5. Bảng tổng hợp so sánh

| Tiêu chí | Guided Crossover (OX/PMX) | $\alpha$-based Guided Swap | Insertion Guided | Random-Key (SPV) |
| :--- | :--- | :--- | :--- | :--- |
| **Ánh xạ Công thức (12.1)–(12.2)** | Gián tiếp, khó kiểm soát $\alpha$ | **Trực tiếp**, tuyến tính theo $\gamma \cdot r \cdot H$ | Trung bình (theo xác suất cạnh) | Giữ nguyên công thức liên tục |
| **Biên $\gamma=0$ và $\gamma=1$** | Không tự nhiên | **Chính xác** (`0 -> source`, `1 -> target`) | Khó đảm bảo $\gamma=1$ | Phụ thuộc vào phân bố vector |
| **Bảo toàn hoán vị & `route[0]=0`** | Tốt | **Tuyệt đối** (mọi bước swap hợp lệ) | Cần kiểm soát tránh sub-tour | Tốt sau bước sort |
| **Độ phức tạp thời gian / bước** | $O(n)$ | **$O(n)$** (nhờ bảng `pos`) | $O(n^2)$ (trên mảng) | $O(n \log n)$ |
| **Độc lập với nhánh GA** | Thấp (trùng toán tử GA) | **Cao** (thuần túy bản sắc EHO) | Cao | Cao |
| **Dễ kiểm thử tính xác định & bất biến** | Trung bình | **Rất cao** ($H$ không tăng, unit test gọn) | Phức tạp | Khó kiểm soát nghiệm trùng |

---

## 3. Đề xuất lựa chọn (Recommendation) và đối chiếu triển khai

**Khuyến nghị chính thức:** Chọn **Hướng 2 — $\alpha$-based Guided Swap** làm toán tử di chuyển lõi cho Discrete EHO.

**Lý do quyết định (đã thống nhất giữa EHO1 và EHO2 trong `docs/algorithm_eho.md`):**
1. **Bảo toàn bản sắc thuật toán EHO:** Giữ nguyên ý nghĩa hình học của Công thức (12.1) và (12.2) — mỗi bước di chuyển thu hẹp khoảng cách giữa `source` và `target` tỉ lệ với cường độ $\alpha, \beta$ và yếu tố ngẫu nhiên $r$.
2. **An toàn hợp đồng domain và tốc độ $O(n)$:** Không bao giờ tạo tour lỗi, không cần bước repair, không sửa đổi input tại chỗ (immutable), và giữ cố định city `0`.
3. **Khả năng kiểm chứng toán học rõ ràng:** Cho phép viết các kiểm thử bất biến chặt chẽ (biên `0/1`, `hamming_distance` không tăng, tái lập hoàn toàn với `random.Random(seed)`).

**Ánh xạ trực tiếp vào mã nguồn dự án:**
- `src/ga_eho_tsp/algorithms/eho/discrete_ops.py`:
  - `hamming_distance(a, b)` — tính $H(a, b)$ trên `1..n-1`.
  - `_guided_swap(source, target, strength, rng)` — thực thi $k = \lfloor \text{strength} \cdot r \cdot H \rfloor$ phép swap trong $O(n)$.
  - `move_toward_best(current, pbest, alpha, rng)` — rời rạc hóa Công thức (12.1).
  - `update_matriarch(matriarch, clan_center, beta, rng)` — rời rạc hóa Công thức (12.2).

---

## 4. Tâm đàn rời rạc (Discrete Clan Center): Medoid vs. Best-Proxy

Trong Công thức (12.3), tâm clan $p_{\text{center}, c} = \frac{1}{n_c}\sum_{j=1}^{n_c} p_{jc}^t$ đóng vai trò **điểm đại diện cho toàn bộ thông tin phân bố của bầy** nhằm điều chỉnh matriarch ở Công thức (12.2). Với không gian hoán vị, có hai cách xấp xỉ phổ biến cần cân nhắc:

### 4.1. So sánh Hamming Medoid vs. Best-Proxy

| Tiêu chí | Hamming Medoid (`Clan.center()`) | Best-Proxy (lấy chính `matriarch` hoặc top-2) |
| :--- | :--- | :--- |
| **Định nghĩa** | $\arg\min_{i} \sum_{j=1}^{n_c} H(m_i, m_j)$ trong clan | Chọn nghiệm tốt nhất (hoặc tốt thứ hai) làm tâm |
| **Tác động lên Công thức (12.2)** | **Có nghĩa:** Matriarch di chuyển về nghiệm nằm ở "trung tâm đồng thuận" của cả clan, tạo khám phá có kiểm soát | **Suy biến:** Nếu lấy best làm tâm thì `source == target` $\Rightarrow$ matriarch đứng yên vĩnh viễn; nếu lấy top-2 thì chỉ dựa trên 1 cá thể, bỏ qua phần lớn clan |
| **Tính hợp lệ** | Luôn trả về một `Route` hợp lệ có sẵn trong clan | Luôn trả về một `Route` hợp lệ |
| **Tính xác định (Tie-break)** | Hoàn toàn xác định theo bộ `(sum_hamming, cost, index)` | Xác định theo `(cost, index)` |
| **Độ phức tạp** | $O(m^2 n)$ với $m$ = `elephants_per_clan` | $O(m)$ |

### 4.2. Quyết định lựa chọn: Hamming Medoid

Dự án chọn **Hamming Medoid** (đã cài đặt trong `Clan.center_index()` và `Clan.center()` tại `src/ga_eho_tsp/algorithms/eho/clans.py`):

$$\text{center\_index} = \arg\min_{i \in \{0, \dots, m-1\}} \left( \sum_{j=0}^{m-1} H(\text{members}[i], \text{members}[j]), \; \text{costs}[i], \; i \right)$$

- **Phân tích hiệu năng:** Với cấu hình mặc định của `EHOConfig` ($C = 4$ clans, $m = 20$ voi/clan, $n \le 48$ thành phố), số phép tính khoảng cách Hamming cho mỗi clan mỗi thế hệ chỉ là $\binom{20}{2} = 190$ cặp $\times 47 \approx 8{,}930$ phép so sánh nguyên — cực kỳ nhỏ (dưới 1 ms), hoàn toàn không gây nút cổ chai.
- **Lợi ích hội tụ:** Khi clan còn đa dạng, medoid khác với matriarch nên Công thức (12.2) tạo nhiễu loạn nhẹ quanh vùng đồng thuận của đàn. Khi clan dần hội tụ, medoid tiến sát matriarch nên biên độ dao động của matriarch tự động thu nhỏ.

### 4.3. Hạn chế đã nhận diện trên Symmetric TSP

Khoảng cách Hamming so sánh **chỉ số vị trí tuyệt đối**, nên trên Symmetric TSP hai tour đảo chiều như `(0, 1, 2, 3, 4, 5)` và `(0, 5, 4, 3, 2, 1)` có cùng tổng độ dài (`1248.0` trên `06Cities-1248.txt`) nhưng $H = 4$ (khác nhau tới 4/5 vị trí đuôi). Dự án chấp nhận hạn chế này cho **baseline D-EHO** để giữ tính nhất quán với `_guided_swap` và độ phức tạp thấp. Việc chuyển sang *Edge-distance Medoid* (đếm số cạnh vô hướng khác nhau) là hướng mở rộng hợp lý cho giai đoạn cải tiến sau khi hoàn tất benchmark baseline.

---

## 5. Ảnh hưởng của $\alpha$ và $\beta$ trong không gian rời rạc

Do số bước swap tuân theo quy luật rời rạc $k = \lfloor \gamma \cdot r \cdot H \rfloor$ (với $r \sim U(0, 1)$), giá trị kỳ vọng của số bước swap xấp xỉ:

$$\mathbb{E}[k] \approx \max\left(0, \; \frac{\gamma \cdot H}{2} - \frac{1}{2}\right)$$

### 5.1. Vai trò và các chế độ của $\alpha$ (Clan Updating — Voi thường)

| Miền giá trị $\alpha$ | Hành vi rời rạc của `move_toward_best` | Hệ quả lên tìm kiếm TSP |
| :--- | :--- | :--- |
| $\alpha = 0.0$ | $k = 0$, mọi voi thường **đứng yên** | Không có khai thác (exploitation); chỉ trông chờ vào toán tử separation. |
| $0 < \alpha \le 0.3$ | Số swap rất nhỏ (với $n$ nhỏ, `floor` thường cho $k = 0$) | Hội tụ quá chậm, khó lan truyền cấu trúc tốt từ matriarch. |
| $0.5 \le \alpha \le 0.8$ | Voi thường di chuyển dần về matriarch sau vài thế hệ | **Vùng cân bằng tốt**; mặc định dự án chọn **`alpha = 0.7`** để khai thác đủ mạnh mà vẫn tạo ra các tour trung gian đa dạng. |
| $\alpha = 1.0$ | Sao chép trực tiếp `pbest` ngay lập tức | Sụp đổ đa dạng quần thể (premature convergence) chỉ sau 1 thế hệ. |

### 5.2. Vai trò và các chế độ của $\beta$ (Matriarch Updating — Voi đầu đàn)

| Miền giá trị $\beta$ | Hành vi rời rạc của `update_matriarch` | Hệ quả lên tìm kiếm TSP |
| :--- | :--- | :--- |
| $\beta = 0.0$ | Matriarch không bao giờ đổi vị trí cho đến khi có voi khác vượt qua | Bảo thủ tuyệt đối, dễ kẹt cục bộ trong clan. |
| $0.1 \le \beta \le 0.4$ | Chỉ thực hiện 1 vài bước swap nhỏ khi matriarch còn cách xa medoid; khi gần medoid ($H$ nhỏ) tự động ổn định ($k = 0$) | **Vùng khuyến nghị**; mặc định dự án chọn **`beta = 0.3`** giúp matriarch khám phá lân cận hướng về tâm đàn mà không phá nát cấu trúc tour tốt. |
| $\beta \ge 0.7$ | Kéo mạnh matriarch về medoid (vốn thường có chi phí kém hơn matriarch) | Làm mất ổn định chất lượng đầu đàn, đòi hỏi phụ thuộc nặng vào archive. |

### 5.3. Phối hợp với cơ chế bảo toàn nghiệm tốt nhất (`preserve_global_best`)

Giống thiết kế bảo toàn `pbest` trong Listing 12.1–12.2 của Slowik (2020), `solver.py` duy trì archive `(best_route, best_distance)` được cập nhật ngay sau **mỗi lần gọi** `problem.route_length(candidate)`. Cuối mỗi thế hệ hoàn chỉnh, với `preserve_global_best = True` (mặc định bắt buộc của `EHOConfig`), nghiệm tốt nhất toàn cục được bảo toàn vào `clans[0]` (thay thế voi tệ nhất không phải leader), đảm bảo `best_so_far` luôn đơn điệu không tăng ngay cả khi matriarch di chuyển về medoid với chi phí tạm thời cao hơn.

---

## 6. Rời rạc hóa Toán tử tách bầy (Separating Operator — Mục 12.2.2)

Trong Công thức (12.4) liên tục, voi tệ nhất bị thay bằng một điểm ngẫu nhiên đều trong hộp biên $[p_{\min}, p_{\max}]$. Khi chuyển sang TSP hoán vị (`src/ga_eho_tsp/algorithms/eho/separation.py`):

1. **Ánh xạ trực tiếp sang không gian hoán vị:** Thay `separation_count_per_clan` cá thể có chi phí cao nhất trong mỗi clan bằng `random_permutation(n, rng)` (bắt đầu từ city `0`). Cách này giữ nguyên bản chất **tái tạo đa dạng toàn cục** của Công thức (12.4) đồng thời triệt tiêu hoàn toàn lỗi vượt cận `+ 1` của bản liên tục.
2. **Bảo vệ matriarch (`protected_indices=(leader_index,)`):** Trong trường hợp biên tất cả các voi trong clan có chi phí bằng nhau (ví dụ ở bài toán nhỏ $n = 3, 4$ hoặc khi clan đã hội tụ hoàn toàn), nếu không bảo vệ `leader_index`, phép tách có thể thay nhầm chính matriarch. Việc truyền `protected_indices=(leader_index,)` đảm bảo không áp dụng hai vai trò xung đột (`update_matriarch` và `separate`) lên cùng một cá thể trong cùng một thế hệ.
3. **Tính xác định (Deterministic tie-break):** Khi nhiều voi có cùng chi phí tệ nhất, thứ tự chọn tách được cố định theo `(-cost, index)` (chi phí giảm dần, sau đó chỉ số tăng dần), đảm bảo tái lập 100% với cùng `seed`.
4. **Cập nhật đồng bộ theo thế hệ:** Các vai trò (`leader_index`, `center`, `separated_indices`) được xác định **một lần duy nhất từ clan cha** trước khi sinh thế hệ mới, không xếp hạng lại giữa chừng; mỗi candidate sinh ra (bao gồm cả voi separation) được tính `problem.route_length` đúng 1 lần và ghi nhận đầy đủ vào bộ đếm `evaluations`.

---

## 7. Ví dụ minh họa từng bước (Step-by-Step Trace)

Tương tự phong cách minh họa số ở Mục 12.5 của Slowik (2020), xét 1 clan gồm $m = 4$ voi trên bộ dữ liệu thực của dự án **`data/06Cities-1248.txt`** ($n = 6$ thành phố) với tham số mặc định của `EHOConfig`: `alpha = 0.7`, `beta = 0.3`, `separation_count = 1`, `seed = 7`.

### Bước 1: Quần thể clan ban đầu và ma trận khoảng cách Hamming

| Cá thể | Route | Chi phí TSP (`route_length`) | Khoảng cách Hamming tới `[E0, E1, E2, E3]` | Tổng Hamming | Vai trò xác định |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **E0** | `(0, 1, 2, 3, 4, 5)` | **1248.0** | `[0, 5, 4, 2]` | 11 | **Matriarch (`leader = 0`)** |
| **E1** | `(0, 2, 1, 4, 5, 3)` | **2291.0** | `[5, 0, 2, 3]` | 10 | **Worst (`separated = 1`)** |
| **E2** | `(0, 2, 1, 3, 5, 4)` | 2286.0 | `[4, 2, 0, 2]` | 8 | Voi thường |
| **E3** | `(0, 2, 1, 3, 4, 5)` | 1847.0 | `[2, 3, 2, 0]` | **7** | **Medoid (`center = 3`)** & Voi thường |

### Bước 2: Cập nhật đồng bộ sang thế hệ kế tiếp (`Random(7)`)

| Cá thể | Toán tử áp dụng | Route mới | Chi phí mới | Thay đổi $H$ tới đích | Nhận xét hành vi |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **E0** | `update_matriarch(E0, E3, beta=0.3)` | `(0, 1, 2, 3, 4, 5)` | 1248.0 | $2 \to 2$ | $\lfloor 0.3 \cdot r \cdot 2 \rfloor = 0$: matriarch đã gần medoid nên tự ổn định. |
| **E1** | `separate(..., separation_count=1)` | `(0, 5, 1, 4, 2, 3)` | **1693.0** | — | Thoát khỏi nghiệm xấu `2291.0`, bổ sung cấu trúc cạnh mới cho clan. |
| **E2** | `move_toward_best(E2, E0, alpha=0.7)` | `(0, 1, 2, 3, 5, 4)` | **1687.0** | $4 \to 2$ | Tiến gần matriarch 2 vị trí, chi phí giảm mạnh (`-599.0`). |
| **E3** | `move_toward_best(E3, E0, alpha=0.7)` | `(0, 1, 2, 3, 4, 5)` | **1248.0** | $2 \to 0$ | Khai thác thành công cấu trúc của matriarch (`-599.0`). |

> **Kiểm chứng tái lập:** Toàn bộ số liệu trên được xác minh trực tiếp bằng các hàm `Clan`, `move_toward_best`, `update_matriarch`, và `separate` trong package `ga_eho_tsp.algorithms.eho` trên file `data/06Cities-1248.txt` với `Random(7)`.

---

## 8. Tài liệu tham khảo

1. Wang, G.-G., Deb, S., & Coelho, L. d. S. (2015). *Elephant herding optimization*. In *2015 3rd International Symposium on Computational and Business Intelligence (ISCBI)* (pp. 1–5). IEEE. DOI: `10.1109/ISCBI.2015.8`.
2. Meena, N. K., Yang, J., & Slowik, A. (2020). *Chapter 12: Elephant Herding Optimization*. In A. Slowik (Ed.), *Swarm Intelligence Algorithms: A Tutorial* (pp. 149–162). CRC Press. ISBN: `978-1-138-38449-1`.
3. Tài liệu thiết kế và hợp đồng nội bộ dự án: `GUIDELINES.md`, `docs/algorithm_eho.md`, `docs/eho_handoff.md`.
