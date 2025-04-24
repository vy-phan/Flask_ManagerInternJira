from typing import Dict, Any, List 
from flask import Blueprint, jsonify, request, current_app, send_file
from ..services import TaskService
from ..models import TaskAttachment
from datetime import datetime
import os
import uuid

task_bp = Blueprint('task', __name__, url_prefix='/task')
task_service = TaskService()

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
def create_task():
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

            file_paths = []
            if 'attachments' in request.files:
                files = request.files.getlist('attachments')
                for file in files:
                    if file and file.filename:
                        filename = f"{uuid.uuid4()}_{file.filename}"
                        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                        file.save(file_path)
                        if not os.path.exists(file_path):
                            return jsonify({
                                'success': False,
                                'error': f'Failed to save file: {filename}'
                            }), 500
                        # Chuyển thành đường dẫn tuyệt đối
                        absolute_file_path = os.path.abspath(file_path)
                        file_paths.append(absolute_file_path)
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
def update_task(task_id):
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
def delete_task(task_id):
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