import logging
import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
from logging.handlers import TimedRotatingFileHandler
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Cấu hình thư mục lưu tệp
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Giới hạn kích thước tệp: 16MB

    # Đảm bảo thư mục uploads tồn tại
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Khởi tạo đối tượng SQLAlchemy
    db.init_app(app)
    migrate.init_app(app, db) 
    app.config['MEDIA_FOLDER'] = 'media'

    # Cho phép các website nào được quyền truy cập vào API của mình 
    # Tạm thời cho * là tất cả trước mắt 
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    configure_logging(app)
    api = Api(app)
    
    # API cha để chứa các API con
    from app.routes import api_bp  
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Error handlers (xử lý lỗi) xử lý các lỗi 404, 500
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Hello World'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Inter server error'
        }), 500
    
    return app

# Configures the logging (log ra mọi kết quả)
def configure_logging(app):
    handler = TimedRotatingFileHandler('flask-template.log', when='midnight', interval=1, backupCount=10)
    handler.setLevel(logging.INFO) 
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)