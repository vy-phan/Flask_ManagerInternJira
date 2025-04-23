from typing import Dict, Any, List 
from flask import Blueprint, jsonify, request, current_app, send_file
from ..services import TaskService
from ..models import TaskAttachment  # Nhập TaskAttachment để tải xuống tệp (tùy chọn)
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

def create(self, data: Dict[str, Any], file_paths: List[str] = None) -> Dict[str, Any]:
        """Create a new task from request data and handle attachments"""
        try:
            # Validate required fields
            required_fields = ['code', 'title', 'deadline', 'created_by']
            for field in required_fields:
                if field not in data or not data[field]:
                    raise ValueError(f"Missing required field: {field}")

            # Validate deadline
            deadline = datetime.fromisoformat(data['deadline'])
            
            # Validate status with Vietnamese values
            valid_statuses = ['Đã giao', 'Đang thực hiện', 'Đã hoàn thành']
            status = data.get('status', 'Đã giao')
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")

            # Create new task
            new_task = Task(
                code=data['code'],
                title=data['title'],
                description=data.get('description'),
                deadline=deadline,
                status=status,
                created_by=data['created_by']
            )
            
            # Save task to database
            created_task = self.task_repository.create(new_task)

            # Lưu các tệp đính kèm nếu có
            if file_paths:
                for file_path in file_paths:
                    self.task_repository.create_attachment(created_task.id, file_path)

            # Format and return the created task
            return self._format_task_data(created_task)
            
        except Exception as e:
            raise Exception(f"Error creating task: {str(e)}")
    
def update(self, task_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing task from request data"""
        try:
            task = self.task_repository.get_by_id(task_id)
            if not task:
                raise ValueError(f"Task with ID {task_id} not found")
            
            # Convert English status to Vietnamese if needed
            status_map = {
                'assigned': 'Đã giao',
                'in_progress': 'Đang thực hiện',
                'completed': 'Đã hoàn thành'
            }
            if 'status' in data:
                data['status'] = status_map.get(data['status'], data['status'])
                
            # Validate status with Vietnamese values
            valid_statuses = ['Đã giao', 'Đang thực hiện', 'Đã hoàn thành']
            if 'status' in data and data['status'] not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")

            # Update task fields from data
            if 'code' in data:
                task.code = data['code']
            if 'title' in data:
                task.title = data['title']
            if 'description' in data:
                task.description = data['description']
            if 'deadline' in data:
                task.deadline = datetime.fromisoformat(data['deadline'])
            if 'status' in data:
                task.status = data['status']
            if 'created_by' in data:
                task.created_by = data['created_by']
            
            # Save changes
            updated_task = self.task_repository.update(task)
            return self._format_task_data(updated_task) if updated_task else None
            
        except Exception as e:
            raise Exception(f"Error updating task: {str(e)}")

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

# Endpoint tùy chọn để tải xuống tệp đính kèm
@task_bp.route('/attachment/<int:attachment_id>', methods=['GET'])
def download_attachment(attachment_id):
    try:
        attachment = TaskAttachment.query.get_or_404(attachment_id)
        return send_file(attachment.file_path, as_attachment=True)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500