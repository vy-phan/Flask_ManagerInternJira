from flask import Blueprint, request, jsonify
from ..services import TaskDetailService
from .auth_routes import token_required

from ..repositories.task_detail_assignee_repository import TaskDetailAssigneeRepository
from ..repositories.user_repository import UserRepository


task_detail_bp = Blueprint('task_detail', __name__, url_prefix='/task_detail')
task_detail_service = TaskDetailService()

assignee_repo = TaskDetailAssigneeRepository()
user_repo = UserRepository()

@task_detail_bp.route('/<int:task_detail_id>/assignees', methods=['GET'])
def get_task_detail_assignees(task_detail_id):
    try:
        assignees = assignee_repo.get_by_task_detail_id(task_detail_id)
        # Lấy thông tin user từ user_id
        users = []
        for assignee in assignees:
            user = user_repo.get_by_id(assignee.user_id)
            if user:
                users.append({
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                })
        return jsonify({'success': True, 'data': users}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

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
@token_required # các route có bảo vệ phải thêm tham số current_user
def create_task_detail(current_user):
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
@token_required # các route có bảo vệ phải thêm tham số current_user
def update_task_detail(current_user,task_detail_id):
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
@token_required # các route có bảo vệ phải thêm tham số current_user
def delete_task_detail(current_user,task_detail_id):
    try:
        result = task_detail_service.delete(task_detail_id)
        if not result:
            return jsonify({'success': False, 'error': 'Task detail not found'}), 404

        return jsonify({'success': True, 'message': 'Task detail deleted successfully'}), 200
    except LookupError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@task_detail_bp.route('/<int:task_detail_id>/status/<string:status>', methods=['PATCH'])
@token_required # các route có bảo vệ phải thêm tham số current_user
def update_task_detail_status(current_user,task_detail_id, status):
    try:
        updated = task_detail_service.update_status(task_detail_id, status)
        if not updated:
            return jsonify({'success': False, 'error': f'Task detail {task_detail_id} not found'}), 404

        return jsonify({'success': True, 'message': 'Task detail status updated successfully', 'data': updated}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

