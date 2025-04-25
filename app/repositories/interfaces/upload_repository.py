from typing import List
from werkzeug.datastructures import FileStorage

class IUploadRepository:
    def save_files(self, files: List[FileStorage], upload_folder: str) -> List[str]:
        """Save files to the specified upload folder and return their absolute paths."""
        pass