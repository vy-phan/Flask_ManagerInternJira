from flask import Blueprint, request, jsonify
from ..services import task_detail_services

task_detail_bp = Blueprint('task_detail', __name__, url_prefix='/task_detail')
task_detail_service = task_detail_services.TaskDetailService()

@task_detail_bp.route('/', methods=['GET'])
def get_all_task_details():
    try:
        task_details = task_detail_service.get_all()
        return jsonify({'success': True, 'data': task_details}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@task_detail_bp.route('/<int:task_id>', methods=['GET'])
def get_task_detail_by_task_id(task_id):
    try:
        task_details = task_detail_service.get_by_task_id(task_id)
        if not task_details:
            return jsonify({'success': False, 'error': 'No task details found'}), 404
        return jsonify({'success': True, 'data': task_details}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@task_detail_bp.route('/', methods=['POST'])
def create_task_detail():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        # Ensure assignees is a list of usernames
        if 'assignees' in data and not isinstance(data['assignees'], list):
            return jsonify({'success': False, 'error': 'Assignees must be a list of usernames'}), 400

        new_detail = task_detail_service.create(data)
        if not new_detail:
            return jsonify({'success': False, 'error': 'Failed to create task detail'}), 500

        return jsonify({'success': True, 'message': 'Task detail created successfully', 'data': new_detail}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except LookupError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@task_detail_bp.route('/<int:task_detail_id>', methods=['PUT'])
def update_task_detail(task_detail_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        updated = task_detail_service.update(task_detail_id, data)
        if not updated:
            return jsonify({'success': False, 'error': f'Task detail {task_detail_id} not found'}), 404

        return jsonify({'success': True, 'message': 'Task detail updated successfully', 'data': updated}), 200
    except LookupError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@task_detail_bp.route('/<int:task_detail_id>', methods=['DELETE'])
def delete_task_detail(task_detail_id):
    try:
        result = task_detail_service.delete(task_detail_id)
        if not result:
            return jsonify({'success': False, 'error': 'Task detail not found'}), 404

        return jsonify({'success': True, 'message': 'Task detail deleted successfully'}), 200
    except LookupError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
