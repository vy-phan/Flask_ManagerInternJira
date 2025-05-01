from .interfaces.upload_repository import IUploadRepository
from typing import List
from werkzeug.datastructures import FileStorage
import os
import uuid

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class UploadRepository(IUploadRepository):
    def save_files(self, files: List[FileStorage], upload_folder: str) -> List[str]:
        """Save files to the specified upload folder and return their API URLs."""
        file_urls = []
        for file in files:
            if file and file.filename:
                filename = f"{uuid.uuid4()}_{file.filename}"
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                if not os.path.exists(file_path):
                    raise ValueError(f"Failed to save file: {filename}")
                
                # Get base URL from environment
                base_url = os.getenv('API_BASE_URL', 'http://localhost:5000')
                file_url = f"{base_url}/api/v1/uploads/{filename}"
                file_urls.append(file_url)
        return file_urls