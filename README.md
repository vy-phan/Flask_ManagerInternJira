# Ứng Dụng Quản Lý Công Việc Flask

Đây là một ứng dụng web được xây dựng bằng Flask, được thiết kế để quản lý công việc (task) giữa người quản lý (manager) và thực tập sinh (intern) trong một tổ chức hoặc nhóm dự án. Nó cung cấp một nền tảng có cấu trúc để giao việc, theo dõi và cập nhật tiến độ công việc.

## Tính Năng Cốt Lõi

*   **Phân Quyền Dựa Trên Vai Trò:** Các chức năng riêng biệt cho vai trò "Quản lý" và "Thực tập sinh".
*   **Quản Lý Người Dùng:**
    *   Form đăng ký riêng cho Quản lý .
    *   Hệ thống đăng nhập an toàn với access token và refresh token.
    *   (Tùy chọn) Xác thực email cho tài khoản mới.
    *   Quản lý có thể chỉnh sửa thông tin của thực tập sinh (nếu cần).
*   **Quản Lý Task (Dành cho Quản lý hoặc tài khoản Thực tập sinh đã được xác thực):**
    *   Tạo các task chính (task lớn) với các chi tiết như tiêu đề, mô tả, hạn chót và mã task duy nhất.
    *   Chỉnh sửa và xóa các task hiện có.
    *   Tạo các task con chi tiết (task\_details) bên trong một task chính.
*   **Giao Việc:**
    *   Giao thực tập sinh tham gia vào các task chính thông qua id của họ.
    *   Giao các task chi tiết cụ thể cho (các) thực tập sinh chịu trách nhiệm.
*   **Theo Dõi Tiến Độ:**
    *   Quản lý có thể xem trạng thái tổng thể của các task và các thực tập sinh được giao.
    *   Thực tập sinh xem một bảng điều khiển (dashboard) cá nhân hóa gồm các task và task chi tiết được giao cho họ.
    *   Thực tập sinh có thể cập nhật trạng thái của các task chi tiết được giao cho mình (ví dụ: sử dụng giao diện kéo-thả). Thay đổi trạng thái sẽ được ghi lại thời gian (`updated_at`).
    *   Tự động cập nhật trạng thái của task chính dựa trên việc hoàn thành các task chi tiết của nó.

## Ngăn Xếp Công Nghệ (Technology Stack)

*   **Backend:** Python, Flask
*   **Cơ sở dữ liệu:**  MySQL 
*   **ORM:** SQLAlchemy
*   **Quản lý Môi trường:** Virtualenv, tệp `.env`



```markdown
Flask_Backend_ThucTapSinh/
├── app/                  # Gói ứng dụng chính
│   ├── __init__.py       # Application factory, đăng ký blueprint
│   ├── models/           # Các model cơ sở dữ liệu (ví dụ: User, Task, TaskDetail)
│   ├── public/           # Tài nguyên tĩnh ( ảnh) 
│   ├── repositories/     # Lớp truy cập dữ liệu (tương tác với models)
│   ├── routes/           # Các route của ứng dụng (Blueprint thường được định nghĩa ở đây)
│   └── services/         # Lớp logic nghiệp vụ
├── venv/                 # Môi trường ảo (thường được git bỏ qua)
├── .env                  # Biến môi trường 
├── .env.example          # Mẫu tệp biến môi trường
├── .flaskenv             # Biến môi trường dành riêng cho Flask (ví dụ: FLASK_APP, FLASK_ENV)
├── .gitignore            # Quy tắc bỏ qua của Git
├── app.py                # Điểm khởi chạy chính của ứng dụng (import và chạy app factory)
├── config.py             # (Các) lớp chứa cài đặt cấu hình
├── flask-template.log    # Tệp log của ứng dụng 
├── README.md             # Tệp này
└── requirements.txt      # Các thư viện Python phụ thuộc của dự án
```


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

1.  QUản lí sẽ đăng kí tài khoản cho người dùng với vai trò "Quản lý" hoặc "Thực tập sinh". 
2.  Thực tập sinh được quản lí cấp tài khoản đăng nhập và tạo các "Task" chính (task lớn).
3.  Quản lý giao có quyền tạo Task hoặc Thực tập sinh được xác thực mới có quyền tạo Task .
4.  Quản lý tạo các "Task Chi Tiết" cụ thể bên trong một Task chính và gán/giao (các) Thực tập sinh các công việc.
5.  Thực tập sinh đăng nhập, xem các Task Chi Tiết được giao trên dashboard của họ.
6.  Thực tập sinh cập nhật trạng thái Task Chi Tiết của họ khi có tiến triển (ví dụ: 'Đã giao', 'Đang tiến hành', 'Hoàn thành'). Hành động này cập nhật trạng thái và dấu thời gian `updated_at`.
7.  Hệ thống tự động đánh dấu một Task chính là "Hoàn thành" khi tất cả các Task Chi Tiết liên quan của nó đã hoàn thành. Các Task không có task chi tiết có thể có trạng thái mặc định như "Chờ giao việc".
8.  Quản lý có thể quản lí các người dùng có trong website 

## Lược Đồ Cơ Sở Dữ Liệu

### 1. Bảng users (Người dùng)
- **Nội dung chính**: Lưu thông tin tài khoản hệ thống
- id (Khóa chính)
- username (Tên đăng nhập, duy nhất)
- password_hash (Mật khẩu đã mã hóa)
- email (Email, duy nhất)
- role (Vai trò: 'MANAGER' - Quản lý hoặc 'INTERN' - Thực tập sinh)
- created_at (Thời gian tạo)
- updated_at (Thời gian cập nhật)
- created_by (Người tạo, tham chiếu đến chính bảng users)

### 2. Bảng tasks (Công việc chính)
- **Nội dung chính**: Quản lý các task lớn, dự án
- id (Khóa chính)
- code (Mã task, duy nhất)
- title (Tiêu đề task)
- description (Mô tả chi tiết)
- deadline (Hạn chót)
- status (Trạng thái: Đã giao - Đang tiến hành - Hoàn thành)
- created_by (Người tạo, tham chiếu đến users)
- created_at/updated_at (Thời gian tạo/cập nhật)

### 3. Bảng task_details (Chi tiết công việc)
- **Nội dung chính**: Các công việc con trong task lớn
- id (Khóa chính)
- task_id (Tham chiếu đến tasks)
- title/description (Thông tin chi tiết)
- status (Trạng thái: Đã giao - Đang tiến hành - Hoàn thành)
- deadline (Hạn chót riêng cho task con)
- created_at/updated_at (Thời gian tạo/cập nhật)

### 4. Bảng task_assignments (Phân công task lớn)
- **Nội dung chính**: Ai được giao task nào
- id (Khóa chính)
- task_id (Tham chiếu đến tasks)
- user_id (Tham chiếu đến users)
- assigned_at (Thời gian giao việc)
- completed_at (Thời gian hoàn thành, có thể null)

### 5. Bảng task_detail_assignments (Phân công task chi tiết)
- **Nội dung chính**: Ai chịu trách nhiệm task con nào
- id (Khóa chính)
- task_detail_id (Tham chiếu đến task_details)
- user_id (Tham chiếu đến users)
- assigned_at (Thời gian giao việc)
- completed_at (Thời gian hoàn thành, có thể null)

### Mối quan hệ giữa các bảng:
1. Một user có thể tạo nhiều tasks (1-n)
2. Một task có nhiều task_details (1-n)
3. Một task có thể giao cho nhiều users (n-n qua task_assignments)
4. Một task_detail được giao cho 1 hoặc nhiều users (n-n qua task_detail_assignments)

## Đóng Góp

Chào mừng các đóng góp. Vui lòng fork repository, tạo một nhánh tính năng (feature branch) và gửi một pull request với mô tả rõ ràng về những thay đổi của bạn.

## Giấy Phép

Dự án này được cấp phép theo Giấy phép MIT - xem tệp `LICENSE.md` (nếu có) để biết chi tiết.

## Lời Cảm Ơn

*   Được xây dựng bằng framework Flask.
*   Lấy cảm hứng từ nhu cầu về một hệ thống quản lý công việc đơn giản cho thực tập sinh.