from .interfaces.upload_repository import IUploadRepository
from typing import List
from werkzeug.datastructures import FileStorage
import os
import uuid

class UploadRepository(IUploadRepository):
    def save_files(self, files: List[FileStorage], upload_folder: str) -> List[str]:
        """Save files to the specified upload folder and return their absolute paths."""
        file_paths = []
        for file in files:
            if file and file.filename:
                # Tạo tên file duy nhất với UUID
                filename = f"{uuid.uuid4()}_{file.filename}"
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                if not os.path.exists(file_path):
                    raise ValueError(f"Failed to save file: {filename}")
                # Chuyển thành đường dẫn tuyệt đối
                absolute_file_path = os.path.abspath(file_path)
                file_paths.append(absolute_file_path)
        return file_paths