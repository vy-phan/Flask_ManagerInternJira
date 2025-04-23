from . import db  # Nhập db từ __init__.py
from flask_sqlalchemy import SQLAlchemy # type: ignore
from datetime import datetime
from .task import Task

class Task_Detail(db.Model):
    __tablename__ = 'task_details'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum('Đã giao', 'Đang thực hiện', 'Hoàn thành'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)