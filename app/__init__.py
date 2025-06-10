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
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Cấu hình thư mục lưu tệp
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Giới hạn kích thước tệp: 100MB

    # Đảm bảo thư mục uploads tồn tại
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Khởi tạo đối tượng SQLAlchemy
    db.init_app(app)
    migrate.init_app(app, db) 
    app.config['MEDIA_FOLDER'] = 'media'

    # Cho phép các website nào được quyền truy cập vào API của mình 
    # Tạm thời cho * là tất cả trước mắt 
    # Configure CORS
    CORS(app, resources={
        r"/api/v1/*": {
            "origins": [
                "http://localhost:5173",  
                "http://127.0.0.1:5173",
                "http://localhost:4173",  
                "http://test-wp.test"
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
            "supports_credentials": True,
            "max_age": 86400  # Cache preflight requests for 1 day
        }
    })
    configure_logging(app)
    api = Api(app)
    

    # api cha để chứa các api con
    from app.routes import api_bp  
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    
    # Error handlers ( xử lí lỗi ) xử lý các lỗi 404, 500
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
    
    @app.route('/api/v1/uploads/<filename>')
    def uploaded_file(filename):
        from flask import send_from_directory, abort
        try:
            # Get absolute path to upload folder
            upload_folder = os.path.abspath(app.config['UPLOAD_FOLDER'])
            
            # Verify file exists
            file_path = os.path.join(upload_folder, filename)
            if not os.path.exists(file_path):
                app.logger.error(f"File not found: {file_path}")
                abort(404)
            
            # Determine file type and set appropriate mimetype
            file_ext = os.path.splitext(filename)[1].lower()
            mimetypes = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.pdf': 'application/pdf',
                '.doc': 'application/msword',
                '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                '.xls': 'application/vnd.ms-excel',
                '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                '.ppt': 'application/vnd.ms-powerpoint',
                '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            }
            
            mimetype = mimetypes.get(file_ext, 'application/octet-stream')
            return send_from_directory(upload_folder, filename, mimetype=mimetype)
        except Exception as e:
            app.logger.error(f"Error serving file {filename}: {str(e)}")
            abort(500)

    return app



# Configures the logging ( log ra mọi kết quả )
def configure_logging(app):
    handler = TimedRotatingFileHandler('flask-template.log', when='midnight', interval=1, backupCount=10)
    handler.setLevel(logging.INFO) 
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

