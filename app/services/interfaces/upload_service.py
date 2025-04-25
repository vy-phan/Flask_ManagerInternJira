from typing import List
from flask import Request

class IUploadService:
    def upload_files(self, request: Request, field_name: str) -> List[str]:
        """Upload files from a request and return a list of file paths."""
        pass