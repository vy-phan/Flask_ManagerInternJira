from flask import Blueprint

api_bp = Blueprint('api', __name__)

from .auth_routes import auth_bp
api_bp.register_blueprint(auth_bp)

from .user_routes import user_bp
api_bp.register_blueprint(user_bp)

from .task_routes import task_bp
api_bp.register_blueprint(task_bp)

from .task_detail_routes import task_detail_bp
api_bp.register_blueprint(task_detail_bp)