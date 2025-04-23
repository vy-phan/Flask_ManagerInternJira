from flask import Blueprint, jsonify, request
from ..services import UserService
from datetime import datetime

user_bp = Blueprint('user', __name__ , url_prefix='/user')
user_service = UserService()

@user_bp.route('/',methods=['GET'])
def get_all_users():
    try:
        users_data = user_service.get_all()  # Changed from get_all_users()
        return jsonify({
            'success': True,
            'data': users_data
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user_data = user_service.get_by_id(user_id)  # Changed from get_user_by_id()
        if not user_data:
            return jsonify({'success': False, 'error': 'User not found'}), 404
            
        return jsonify({
            'success': True,
            'data': user_data
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        # Kiểm tra các trường bắt buộc
        required_fields = ['username', 'password', 'email', 'start_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400

        # Kiểm tra định dạng start_date
        try:
            datetime.fromisoformat(data['start_date'])
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid start_date format. Use ISO format (e.g., 2025-04-21)'}), 400

        # Kiểm tra gender hợp lệ nếu được cung cấp
        if 'gender' in data:
            valid_genders = ['Nam', 'Nữ', 'Khác']
            if data['gender'] not in valid_genders:
                return jsonify({'success': False, 'error': f'Invalid gender. Must be one of: {valid_genders}'}), 400

        # Gọi service để tạo user và kiểm tra kết quả
        try:
            user_data = user_service.create(data)
            if not user_data or not isinstance(user_data, dict):
                return jsonify({
                    'success': False,
                    'error': 'Failed to create user: Invalid response from service'
                }), 500
                
            return jsonify({
                'success': True,
                'message': 'User created successfully',
                'data': user_data
            }), 201
            
        except Exception as service_error:
            return jsonify({
                'success': False,
                'error': f'Service error: {str(service_error)}'
            }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):  # Make sure this parameter matches the route
    try:
        # Lấy dữ liệu từ request body
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        # Kiểm tra gender hợp lệ nếu được cung cấp
        if 'gender' in data:
            valid_genders = ['Nam', 'Nữ', 'Khác']
            if data['gender'] not in valid_genders:
                return jsonify({'success': False, 'error': f'Invalid gender. Must be one of: {valid_genders}'}), 400
                
        # Kiểm tra định dạng start_date nếu được cung cấp
        if 'start_date' in data:
            try:
                datetime.fromisoformat(data['start_date'])
            except ValueError:
                return jsonify({'success': False, 'error': 'Invalid start_date format. Use ISO format (e.g., 2025-04-21)'}), 400

        # Gọi service để cập nhật user - ensure user_id is passed correctly
        updated_user = user_service.update(user_id, data)
        if not updated_user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        return jsonify({
            'success': True,
            'message': 'User updated successfully',
            'data': updated_user
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # Gọi service để xóa user
        result = user_service.delete(user_id)
        if not result:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
