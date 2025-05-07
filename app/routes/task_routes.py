from typing import Dict, Any, List 
from flask import Blueprint, jsonify, request, current_app, send_file
from ..services import TaskService, UploadService, UserService
from ..models import TaskAttachment
from datetime import datetime
from .auth_routes import token_required

task_bp = Blueprint('task', __name__, url_prefix='/task')
task_service = TaskService()
user_service = UserService()
upload_service = UploadService()

@task_bp.route('/', methods=['GET'])
def get_all_tasks():
    try:
        tasks = task_service.get_all()
        return jsonify({
            'success': True,
            'data': tasks
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@task_bp.route('/', methods=['POST'])
@token_required
def create_task(current_user):
    try:
        if request.is_json:
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'error': 'No data provided'}), 400
            file_paths = None
        elif request.form:
            data = request.form.to_dict()
            if not data:
                return jsonify({'success': False, 'error': 'No form data provided'}), 400

            # Sử dụng UploadService để xử lý upload file
            file_paths = upload_service.upload_files(request, 'attachments')
        else:
            return jsonify({'success': False, 'error': 'Unsupported content type'}), 400

        required_fields = ['code', 'title', 'deadline', 'created_by']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400

        try:
            datetime.fromisoformat(data['deadline'])
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid deadline format. Use ISO format (e.g., 2025-04-21T15:30:00)'
            }), 400

        new_task = task_service.create(data, file_paths)
        if not new_task:
            return jsonify({
                'success': False,
                'error': 'Failed to create task'
            }), 500

        return jsonify({
            'success': True,
            'message': 'Task created successfully',
            'data': new_task
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_bp.route('/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    try:
        task = task_service.get_by_id(task_id)      
        if not task:
            return jsonify({
                'success': False,
                'error': f'Task with ID {task_id} not found'
            }), 404
        return jsonify({
            'success': True,
            'data': task
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@task_bp.route('/<int:task_id>', methods=['PUT'])
@token_required
def update_task(current_user, task_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        if 'deadline' in data:
            try:
                datetime.fromisoformat(data['deadline'])
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid deadline format. Use ISO format (e.g., 2025-04-21T15:30:00)'
                }), 400

        updated_task = task_service.update(task_id, data)
        if not updated_task:
            return jsonify({
                'success': False,
                'error': f'Task with ID {task_id} not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Task updated successfully',
            'data': updated_task
        }), 200

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@task_bp.route('/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    try:
        result = task_service.delete(task_id)
        if not result:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        }), 200
    except ValueError as e:  # Lỗi khóa ngoại
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@task_bp.route('/attachment/<int:attachment_id>', methods=['GET'])
def download_attachment(attachment_id):
    try:
        attachment_data = task_service.get_attachment_by_id(attachment_id)
        if not attachment_data:
            return jsonify({
                'success': False,
                'error': f'Attachment with ID {attachment_id} not found'
            }), 404

        file_path = attachment_data['file_path']
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': f'File not found at path: {file_path}'
            }), 404

        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
@task_bp.route('/<int:task_id>/incomplete_details', methods=['GET'])
def count_incomplete_task_details(task_id):
    try:
        count = task_service.count_incomplete_task_details(task_id)
        return jsonify({'success': True, 'count': count}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500