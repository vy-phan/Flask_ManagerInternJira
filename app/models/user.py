from . import db
from .role import UserRole  
from enum import Enum

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    birth_year = db.Column(db.Integer)
    email = db.Column(db.String(255),nullable=False)
    phone = db.Column(db.String(20))
    gender = db.Column(db.Enum('Nam', 'Nữ', 'Khác'), default='Nam')
    avatar = db.Column(db.String(255))
    start_date = db.Column(db.Date, nullable=False)
    cv_link = db.Column(db.String(255))
    role = db.Column(db.Enum(UserRole), default=UserRole.INTERN)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    