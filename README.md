# Ứng Dụng Quản Lý Công Việc Flask

Đây là một ứng dụng web được xây dựng bằng Flask, được thiết kế để quản lý công việc (task) giữa người quản lý (manager) và thực tập sinh (intern) trong một tổ chức hoặc nhóm dự án. Nó cung cấp một nền tảng có cấu trúc để giao việc, theo dõi và cập nhật tiến độ công việc.

## Tính Năng Cốt Lõi

*   **Phân Quyền Dựa Trên Vai Trò:** Các chức năng riêng biệt cho vai trò "Quản lý" và "Thực tập sinh".
*   **Quản Lý Người Dùng:**
    *   Form đăng ký riêng cho Quản lý và Thực tập sinh.
    *   Hệ thống đăng nhập an toàn.
    *   (Tùy chọn) Xác thực email cho tài khoản mới.
    *   Quản lý có thể chỉnh sửa thông tin của thực tập sinh (nếu cần).
*   **Quản Lý Task (Dành cho Quản lý):**
    *   Tạo các task chính (task lớn) với các chi tiết như tiêu đề, mô tả, hạn chót và mã task duy nhất.
    *   Chỉnh sửa và xóa các task hiện có.
    *   Tạo các task con chi tiết (task\_details) bên trong một task chính.
*   **Giao Việc:**
    *   Giao thực tập sinh tham gia vào các task chính thông qua username của họ.
    *   Giao các task chi tiết cụ thể cho (các) thực tập sinh chịu trách nhiệm.
*   **Theo Dõi Tiến Độ:**
    *   Quản lý có thể xem trạng thái tổng thể của các task và các thực tập sinh được giao.
    *   Thực tập sinh xem một bảng điều khiển (dashboard) cá nhân hóa gồm các task và task chi tiết được giao cho họ.
    *   Thực tập sinh có thể cập nhật trạng thái của các task chi tiết được giao cho mình (ví dụ: sử dụng giao diện kéo-thả). Thay đổi trạng thái sẽ được ghi lại thời gian (`updated_at`).
    *   Tự động cập nhật trạng thái của task chính dựa trên việc hoàn thành các task chi tiết của nó.
*   **(Cải Tiến Có Thể Bổ Sung):**
    *   Gửi thông báo qua email cho thực tập sinh khi có task mới hoặc deadline sắp đến.
    *   Chức năng tìm kiếm task (theo tiêu đề, trạng thái).

## Ngăn Xếp Công Nghệ (Technology Stack)

*   **Backend:** Python, Flask
*   **Cơ sở dữ liệu:**  MySQL 
*   **ORM:** SQLAlchemy
*   **Quản lý Môi trường:** Virtualenv, tệp `.env`

Flask_Backend_ThucTapSinh/
│
├── app/ # Gói ứng dụng chính
│ ├── init.py # Application factory, đăng ký blueprint
│ ├── models/ # Các model cơ sở dữ liệu (ví dụ: User, Task, TaskDetail)
│ ├── public/ # Tài nguyên tĩnh (CSS, JS, ảnh) - Lưu ý: Đổi tên nếu cần
│ ├── repositories/ # Lớp truy cập dữ liệu (tương tác với models)
│ ├── routes/ # Các route/controller của ứng dụng (Blueprint thường được định nghĩa ở đây)
│ └── services/ # Lớp logic nghiệp vụ
│
├── venv/ # Môi trường ảo (thường được git bỏ qua)
├── .env # Biến môi trường (dữ liệu nhạy cảm, bị git bỏ qua)
├── .env.example # Mẫu tệp biến môi trường
├── .flaskenv # Biến môi trường dành riêng cho Flask (ví dụ: FLASK_APP, FLASK_ENV)
├── .gitignore # Quy tắc bỏ qua của Git
├── app.py # Điểm khởi chạy chính của ứng dụng (import và chạy app factory)
├── config.py # (Các) lớp chứa cài đặt cấu hình
├── flask-template.log # Tệp log của ứng dụng (ví dụ)
├── README.md # Tệp này
└── requirements.txt # Các thư viện Python phụ thuộc của dự án


## Cấu Trúc Dự Án
*(Lưu ý: Đảm bảo `app.py` được thiết lập đúng là điểm khởi chạy, hoặc điều chỉnh mô tả nếu bạn sử dụng tệp khác như `run.py` hoặc `wsgi.py`. Thư mục `public` trong cấu trúc của bạn có thể dùng cho static files, hãy kiểm tra lại cách bạn tổ chức file tĩnh)*

## Khởi Động Nhanh

1.  **Sao chép (clone) repository:**
    ```bash
    git clone https://github.com/vy-phan/Flask_Backend_ThucTapSinh.git
    cd Flask_Backend_ThucTapSinh
    ```
2.  **Tạo và kích hoạt môi trường ảo:**
    ```bash
    python -m venv venv
    # Trên Windows:
    .\venv\Scripts\activate
    # Trên macOS/Linux:
    source venv/bin/activate
    ```
3.  **Cấu hình biến môi trường:**
    *   Sao chép `.env.example` thành `.env`: `cp .env.example .env`
    *   Chỉnh sửa tệp `.env` và đặt các cấu hình cụ thể của bạn (Chuỗi kết nối CSDL, Secret Key, v.v.).
4.  **Cài đặt các thư viện phụ thuộc:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **(Nếu sử dụng cơ sở dữ liệu với migrations, ví dụ: Flask-Migrate):**
    ```bash
    # Khởi tạo migrations (chỉ lần đầu)
    # flask db init
    # Tạo script migration
    # flask db migrate -m "Migration ban đầu."
    # Áp dụng migrations vào cơ sở dữ liệu
    flask db upgrade
    ```
6.  **Chạy ứng dụng:**
    ```bash
    flask run
    ```
7.  Truy cập ứng dụng trong trình duyệt web của bạn (thường là tại `http://127.0.0.1:5000/`).

## Cấu Hình

Cài đặt ứng dụng được quản lý thông qua các biến môi trường được tải từ tệp `.env`. Tham khảo `.env.example` để biết danh sách các biến bắt buộc và tùy chọn. Các cấu hình chính thường bao gồm:

*   `FLASK_APP`: Nên được đặt thành `app.py` (hoặc điểm khởi chạy của bạn).
*   `FLASK_ENV`: `development` (phát triển) hoặc `production` (sản phẩm).
*   `SECRET_KEY`: Một khóa bí mật mạnh, duy nhất để bảo mật session.
*   `DATABASE_URL`: Chuỗi kết nối đến cơ sở dữ liệu của bạn.
*   (Các cài đặt cụ thể khác như chi tiết máy chủ email nếu triển khai thông báo).

## Tóm Tắt Quy Trình Cốt Lõi

1.  Người dùng đăng ký với vai trò "Quản lý" hoặc "Thực tập sinh".
2.  Quản lý đăng nhập và tạo các "Task" chính (task lớn).
3.  Quản lý gán "Thực tập sinh" vào các Task này bằng username của họ.
4.  Quản lý tạo các "Task Chi Tiết" cụ thể bên trong một Task chính và gán (các) Thực tập sinh chịu trách nhiệm.
5.  Thực tập sinh đăng nhập, xem các Task Chi Tiết được giao trên dashboard của họ.
6.  Thực tập sinh cập nhật trạng thái Task Chi Tiết của họ khi có tiến triển (ví dụ: 'Cần làm', 'Đang làm', 'Hoàn thành'). Hành động này cập nhật trạng thái và dấu thời gian `updated_at`.
7.  Hệ thống tự động đánh dấu một Task chính là "Hoàn thành" khi tất cả các Task Chi Tiết liên quan của nó đã hoàn thành. Các Task không có task chi tiết có thể có trạng thái mặc định như "Chờ giao việc".

## Lược Đồ Cơ Sở Dữ Liệu Đề Xuất

Ứng dụng dự kiến sử dụng các bảng cơ sở dữ liệu cốt lõi sau:

*   **users:** Lưu thông tin người dùng (ID, username, password hash, email, role - Quản lý/Thực tập sinh).
*   **tasks:** Lưu thông tin về các task chính (ID, task\_code, title, description, deadline, status, created\_at, updated\_at).
*   **task\_details:** Lưu thông tin về các task con/chi tiết (ID, task\_id (FK tới tasks), title, description, status, created\_at, updated\_at).
*   **task\_assignees:** Ánh xạ người dùng (Thực tập sinh) vào các task chính mà họ tham gia (task\_id, user\_id).
*   **task\_detail\_assignees:** Ánh xạ người dùng (Thực tập sinh) vào các task chi tiết cụ thể mà họ chịu trách nhiệm (task\_detail\_id, user\_id).

## Đóng Góp

Chào mừng các đóng góp. Vui lòng fork repository, tạo một nhánh tính năng (feature branch) và gửi một pull request với mô tả rõ ràng về những thay đổi của bạn.

## Giấy Phép

Dự án này được cấp phép theo Giấy phép MIT - xem tệp `LICENSE.md` (nếu có) để biết chi tiết.

## Lời Cảm Ơn

*   Được xây dựng bằng framework Flask.
*   Lấy cảm hứng từ nhu cầu về một hệ thống quản lý công việc đơn giản cho thực tập sinh.