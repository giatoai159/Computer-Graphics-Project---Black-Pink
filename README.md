# Computer Graphics Project - Black Pink
## Đồ án lý thuyết: Sử dụng OpenGL để làm game 2D
## Thành viên:
1. Phan Quý Nguyên - 18120487 - Nhóm trưởng
   - pqn2810@gmail.com
2. Huỳnh Gia Toại - 18120598
   - giatoai159@gmail.com
3. Trang Thanh Trúc - 18120270
   - trangthanhtruc2103@gmail.com
4. Trần Tiến Sỹ - 1612571
   - 1612571@student.hcmus.edu.vn
5. Lê Hoàng Mộng Tuyền - 18120259
   - lehoangmongtuyen@gmail.com
## Nội dung
Game Flappy Bird được viết bằng ngôn ngữ Python. Mã nguồn logic game đa số dựa vào https://github.com/russs123/flappy_bird, chỉ thay đổi render bằng OpenGL thay vì PyGame, có một số sửa đổi nhỏ.
### Các thư viện sử dụng:
- PyGame: Tạo window, các hàm game cơ bản như chèn âm thanh, tương tác chuột/bàn phím,...
- PyOpenGL: Để render đồ họa game, code đa số theo Modern OpenGL (Không sử dụng glBegin và glEnd)
- GLM: OpenGL Math Library để tính toán ma trận
