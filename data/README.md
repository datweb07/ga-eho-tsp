# Dữ liệu legacy

Ma trận explicit whitespace, không header, city 0-based ở core.
Nguồn trực tiếp: bộ code nhóm đưa vào workspace, tham chiếu ThienNguyen3001/Travelling-Salesman-Genetic-AI-Final.
Các file được chuyển nguyên byte từ data/ sang data/legacy/. Chưa xác minh quyền phân phối hoặc ánh xạ từng file với nguồn dataset gốc.
Hậu tố tên chỉ là hint; registry known_optimum=None. Xem docs/audit_legacy.md về nguồn/giấy phép và kiểm chứng exhaustive 3/4/6 city.

Tất cả 7 file đã qua dimension, square, symmetry, diagonal=0, finite, nonnegative checks.

| File | n | Cost route (0,1,…,n−1) | SHA256 |
|---|---:|---:|---|
| 03Cities-6.txt | 3 | 6 | `479119c271477577a458e6994179b03855595e58cdf2fa7852c53699faa2910d` |
| 04Cities-189.txt | 4 | 224 | `5119516bc891f6475737d10abc4c3b8c354c51ac013a3db72e8a5634fa3e6e5f` |
| 06Cities-1248.txt | 6 | 1248 | `35010aefe80fba1594a74d3f2d087bc8251445fdbc196c3fca04528e4a262d9e` |
| 15Cities-1194.txt | 15 | 1312 | `deb32a09413ec1a2d7f94fa9c71d077df2f6a924e97b6082557e435733808b31` |
| 26Cities-937.txt | 26 | 1140 | `e4ac61b64b8a1b2a9c364830a0a80226bcfece32af4033c19dfa3be32e4aa6ef` |
| 42Cities-699.txt | 42 | 699 | `e84c18a1cf613f3b6cbef909fb926e9652b2be3dbba6665083d1b6751a4d292d` |
| 48Cities-33523.txt | 48 | 157553 | `6ec85f3661939d1b319b047769cc65e4327261b3a70cfe1fed0571cd3df0f3c0` |
