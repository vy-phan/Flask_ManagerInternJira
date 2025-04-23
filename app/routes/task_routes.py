from flask import Blueprint, jsonify, request
from ..services import TaskService
from datetime import datetime

task_bp = Blueprint('task', __name__, url_prefix='/task')
task_service = TaskService()

@task_bp.route('/', methods=['GET'])
def get_all_tasks():
    try:
        tasks = task_service.get_all()  # Changed from get_all_tasks()
        return jsonify({
            'success': True,
            'data': tasks
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@task_bp.route('/', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        # Validate required fields
        required_fields = ['code', 'title', 'deadline', 'created_by']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False, 
                    'error': f'Missing required field: {field}'
                }), 400

        # Validate deadline format
        try:
            datetime.fromisoformat(data['deadline'])
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid deadline format. Use ISO format (e.g., 2025-04-21T15:30:00)'
            }), 400

        # Validate status
        valid_statuses = ['assigned', 'in_progress', 'completed']
        if 'status' in data and data['status'] not in valid_statuses:
            return jsonify({
                'success': False,
                'error': f'Invalid status. Must be one of: {valid_statuses}'
            }), 400

        # Map English status to Vietnamese
        status_mapping = {
            'assigned': 'Đã giao',
            'in_progress': 'Đang thực hiện',
            'completed': 'Đã hoàn thành'
        }
        
        if 'status' in data:
            data['status'] = status_mapping.get(data['status'], 'Đã giao')

        # Create task using service
        new_task = task_service.create(data)  # Changed from create_task()
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

@task_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

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
        result = task_service.delete(task_id)  # Changed from delete_task()
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
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500