from flask import Blueprint, jsonify, request
from ..services.user_service import UserService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
user_service = UserService()

@auth_bp.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({
            'success': False,
            'message': 'Email and password are required'
        }), 400
    
    if user_service.verify_credentials(email, password):
        return jsonify({
            'success': True,
            'message': 'Login successful'
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid email or password'
        }), 401

@auth_bp.route('/logout/', methods=['POST'])
def logout():
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    }), 200