from ..models.task_attachment import TaskAttachment
from .. import db

class TaskAttachmentRepository:
    def get_by_task_id(self, task_id: int):
        """Lấy tất cả các tệp đính kèm của một task"""
        return TaskAttachment.query.filter_by(task_id=task_id).all()

    def create(self, task_id: int, file_path: str):
        """Thêm tệp đính kèm mới"""
        attachment = TaskAttachment(task_id=task_id, file_path=file_path)
        db.session.add(attachment)
        db.session.commit()
        return attachment

    def delete_by_task_id(self, task_id: int):
        """Xóa tất cả tệp đính kèm của một task"""
        attachments = self.get_by_task_id(task_id)
        for attachment in attachments:
            db.session.delete(attachment)
        db.session.commit()

    def delete_by_id(self, attachment_id: int):
        """Xóa tệp đính kèm theo ID"""
        attachment = TaskAttachment.query.get(attachment_id)
        if attachment:
            db.session.delete(attachment)
            db.session.commit()