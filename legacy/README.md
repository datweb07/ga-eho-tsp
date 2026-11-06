# Bản tham chiếu được bảo toàn

Nguồn được nhóm cung cấp: [ThienNguyen3001/Travelling-Salesman-Genetic-AI-Final](https://github.com/ThienNguyen3001/Travelling-Salesman-Genetic-AI-Final).
`original_src/`, `original_demo/`, `original_experiments/` giữ code/notebook có sẵn trong workspace.
`original_scripts/` giữ hai script bổ sung trong workspace mới, chưa xác minh tác giả.
Các file được di chuyển bằng Move-Item, không sửa nội dung. Dữ liệu ở `../data/legacy/`.
Không import từ app mới; không coi đây là code nhóm tự viết. Chưa tìm thấy LICENSE trong bản local và danh sách root upstream đã xem ngày 05/11/2026; quyền phân phối chưa xác minh. Leader cần xin phép tác giả trước khi phân phối phần kế thừa.

Các đường dẫn tương đối gốc được giữ làm bằng chứng nên launcher/notebook đã archive không mặc nhiên chạy tại vị trí mới. Dùng script tái hiện có kiểm soát:

```powershell
python -m pip install -e '.[legacy]'
python experiments/scripts/audit_legacy.py
```

GUI cũ chưa được nghiệm thu tương tác; bản mới chưa triển khai GUI. Root `benchmark_all.py` là wrapper duy nhất được thay mới trong giai đoạn GA.
