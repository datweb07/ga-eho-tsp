# Nguồn tham khảo và khả năng phục hồi

Nguồn code ban đầu do nhóm cung cấp: [ThienNguyen3001/Travelling-Salesman-Genetic-AI-Final](https://github.com/ThienNguyen3001/Travelling-Salesman-Genetic-AI-Final). README upstream đã được kiểm tra ở audit trước ghi nhóm Nguyễn Ngọc Thiện, Nguyễn Minh Nhựt, Nguyễn Trọng Hưởng, Trần Viết Gia Huy. Tác giả hai script benchmark/visualization bổ sung trong workspace chưa xác minh. Không có xác nhận giấy phép/quyền phân phối code hoặc7ma trận; không gán license mới lên nội dung kế thừa.

GA chính thức trong src/ga_eho_tsp được viết lại từ thiết kế permutation và được kiểm thử; không runtime import source đàn anh. Không trình bày source tham chiếu như thành quả tự viết của nhóm. Nhóm cần review, hiểu và giải thích implementation trước khi nộp theo yêu cầu giảng viên “cài đặt lại từ đầu”.

Ba notebook hiện tại được viết mới theo các chủ đề tham chiếu: operators/sensitivity, distribution/stability, challenging cases. Bản gốc37/20/43cells có API/import cũ và notebook4 có vòng chạy tới target; không sao chép code/kết luận/ảnh cũ làm kết quả mới. Notebook mới17/13/13cells dùng public package, seed/budget hữu hạn, bảng/plot chạy thật và best-observed thay cho optimum chưa biết.

7matrix ở data/legacy giữ nguyên byte; SHA256 ở [data README](../data/README.md). Nguồn dataset gốc, cách ánh xạ từng file và optimum chưa đối chiếu đầy đủ; hậu tố tên chỉ là hint. Hai instance nhỏ3/6city được enumeration kiểm chứng offline trong notebook3, không biến thành solver thứ ba hoặc bằng chứng optimum cho bài khác. Registry known_optimum vẫn None.

## Backup ngoài repository

Final cleanup ngày06/11/2026 đã lưu **working tree thực**, kể cả thay đổi chưa commit/untracked, tests, config, raw results và notebooks tham chiếu có thể lấy từ Git, vào:

`C:/Users/THANH DAT/.codex/visualizations/2026/11/05/01a1ac43-7b68-7e63-8442-c7ebf03dd47f/ga-final-handoff/before-cleanup.zip`

SHA256 archive: `2fed13de13d86da5d5ce2b3e1ace56ff7751a98a45de0b40750ac797cc2790b9`.

ZIP chứa467file của working tree (loại .git/.venv/cache), SHA256 từng path trong snapshot_manifest.json, cộng ba notebook original lấy bằng git show vào _reference_original_notebooks/. Đã chạy testzip và đối chiếu hash từng entry trước xóa. Git status đầu phiên, working_tree.patch và staged.patch được lưu cùng thư mục ngoài repo; không reset/commit/push. HEAD ở thời điểm backup: `e6dfb233a0f5dbe55a17e8b9c8812ee602d63d20`, branch main.

Bằng chứng QA release, executed notebooks ở hai kernel, log166tests, post-cleanup assertions, môi trường và batch benchmark mới được lưu cùng thư mục ngoài repo; raw benchmark được archive vào release-evidence.zip trước khi xóa outputs. Khi đổi máy cần mang backup riêng nếu muốn phục hồi tests hoặc điều tra số liệu cũ; app/notebook không phụ thuộc vào đường dẫn backup này. Không khôi phục đè toàn repo đang có thay đổi, chỉ trích xuất phần cần vào một thư mục khác để review.

Các audit/manifest/prompt ngắn hạn, tests và reports đã được loại khỏi cây bàn giao theo chỉ thị leader sau backup. Những lỗi lịch sử quan trọng (elitism lặp, uniform no-op, mất best, roulette ties, route/import thiếu contract) có bằng chứng trong bản backup; không gán lại chúng là bug hiện tại đã được tái hiện ở release này. Tài liệu chạy hiện hành chỉ ở README, architecture, algorithm_ga và experiments.
