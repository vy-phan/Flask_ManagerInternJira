from . import db
from .task_detail import Task_Detail
from .user import User

class Task_Detail_Assignees(db.Model):
    __tablename__ = 'task_detail_assignees'
    id = db.Column(db.Integer, primary_key=True)
    task_detail_id = db.Column(db.Integer, db.ForeignKey('task_details.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, nullable=False)  # Renamed column