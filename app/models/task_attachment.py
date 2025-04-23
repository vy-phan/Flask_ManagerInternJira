from . import db  # Nhập db từ __init__.py

class TaskAttachment(db.Model):
    __tablename__ = 'task_attachments'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)  # Khóa ngoại liên kết với Task
    file_path = db.Column(db.String(255), nullable=False)  # Đường dẫn tệp
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Thời gian tải lên

    # Mối quan hệ với Task
    task = db.relationship('Task', backref=db.backref('attachments', lazy=True))

    def __repr__(self):
        return f'<TaskAttachment {self.id} for Task {self.task_id}>'