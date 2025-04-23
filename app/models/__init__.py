from flask_sqlalchemy import SQLAlchemy

from app import db  

from .task import Task 
from .user import User
from .role import UserRole
from .task_detail import Task_Detail
from .task_detail_assignees import Task_Detail_Assignees  # Add this line
