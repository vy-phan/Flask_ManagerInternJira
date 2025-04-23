from . import db  # Nhập db từ __init__.py

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)  # Mã nhiệm vụ
    title = db.Column(db.String(255), nullable=False)  # Tiêu đề
    description = db.Column(db.Text, nullable=True)  # Mô tả
    deadline = db.Column(db.DateTime, nullable=False)  # Thời hạn
    status = db.Column(db.Enum('Đã giao', 'Đang thực hiện', 'Đã hoàn thành'), default='Đã giao')  # Trạng thái
    created_by = db.Column(db.Integer, nullable=False)  # ID của người tạo
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Thời gian tạo

    # Mối quan hệ với TaskAttachment (đã tự động tạo qua backref)
    # attachments = db.relationship('TaskAttachment', backref='task', lazy=True)

    def __repr__(self):
        return f'<Task {self.code}>'


