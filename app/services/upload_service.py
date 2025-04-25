# Import interface IUploadService từ thư mục con interfaces
# Interface này định nghĩa hợp đồng mà UploadService phải tuân theo
from .interfaces.upload_service import IUploadService

# Import interface IUploadRepository từ thư mục con repositories.interfaces
# Interface này định nghĩa hợp đồng cho repository xử lý việc upload file
from ..repositories.interfaces.upload_repository import IUploadRepository

# Import class UploadRepository từ thư mục repositories
# Đây là triển khai cụ thể của IUploadRepository, chịu trách nhiệm lưu file
from ..repositories.upload_repository import UploadRepository

# Import đối tượng Request từ Flask để xử lý yêu cầu HTTP và current_app để truy cập cấu hình của ứng dụng Flask
from flask import Request, current_app

# Import List từ typing để sử dụng type hints, định nghĩa kiểu trả về của phương thức upload_files
from typing import List

# Định nghĩa class UploadService, triển khai interface IUploadService
class UploadService(IUploadService):
    # Phương thức khởi tạo của UploadService
    # Nhận một tham số upload_repository (tùy chọn), phải triển khai IUploadRepository
    # Nếu không truyền repository, sẽ tạo một instance mới của UploadRepository
    def __init__(self, upload_repository: IUploadRepository = None):
        # Gán repository được truyền vào hoặc tạo mới một UploadRepository
        self.upload_repository = upload_repository or UploadRepository()

    # Phương thức xử lý upload file từ một yêu cầu HTTP
    # Tham số:
    # - request: Đối tượng Request của Flask chứa dữ liệu yêu cầu HTTP (bao gồm file)
    # - field_name: Tên của trường form chứa file (ví dụ: 'attachments')
    # Trả về danh sách các đường dẫn file (dạng chuỗi) nơi file được lưu
    def upload_files(self, request: Request, field_name: str) -> List[str]:
        """Upload file từ yêu cầu và trả về danh sách đường dẫn file."""
        # Kiểm tra xem trường field_name (ví dụ: 'attachments') có tồn tại trong phần file của yêu cầu không
        # Nếu không có, trả về danh sách rỗng (không có file để upload)
        if field_name not in request.files:
            return []
        
        # Lấy danh sách các file từ yêu cầu bằng field_name đã cho
        # request.files.getlist() được dùng để xử lý nhiều file trong cùng một trường
        files = request.files.getlist(field_name)
        
        # Kiểm tra xem có file nào không và liệu tất cả file có tên rỗng hay không
        # Nếu không có file hoặc tất cả file đều không có tên, trả về danh sách rỗng
        if not files or all(not file.filename for file in files):
            return []

        # Lấy đường dẫn thư mục upload từ cấu hình của ứng dụng Flask
        # current_app.config.get('UPLOAD_FOLDER') truy xuất giá trị của 'UPLOAD_FOLDER'
        upload_folder = current_app.config.get('UPLOAD_FOLDER')
        
        # Kiểm tra xem UPLOAD_FOLDER đã được cấu hình trong ứng dụng Flask chưa
        # Nếu chưa, ném lỗi ValueError để báo rằng cấu hình bị thiếu
        if not upload_folder:
            raise ValueError("UPLOAD_FOLDER chưa được cấu hình trong ứng dụng Flask")

        # Giao việc lưu file cho upload_repository
        # Phương thức save_files() nhận danh sách file và đường dẫn thư mục upload
        # Nó lưu file vào hệ thống và trả về danh sách các đường dẫn tuyệt đối của file
        return self.upload_repository.save_files(files, upload_folder)