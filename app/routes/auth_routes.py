from flask import Blueprint, jsonify, request, make_response
from ..services.user_service import UserService
from functools import wraps
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
user_service = UserService()

# bảo vệ router cần có token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Kiểm tra có header Authorization 
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        # Nếu không có token trong header, kiểm tra trong cookies
        if not token and 'access_token' in request.cookies:
            token = request.cookies.get('access_token')
        # báo lỗi nếu token vẫn không có trong cookie
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token is missing'
            }), 401
            
        # Xác thực lại token có phải là hợp lệ
        is_valid, payload = user_service.verify_token(token)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': payload.get('error', 'Invalid token')
            }), 401
            
        # Get user from token
        current_user = user_service.get_user_from_token(token)
        if not current_user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

# bảo vệ router nào chỉ có manager là có quyền 
def admin_required(f):
    @wraps(f)
    @token_required  
    def decorated(current_user, *args, **kwargs):
        # Thêm kiểm tra role có tồn tại không
        if not current_user.get('role'):
            return jsonify({
                'success': False,
                'message': 'User role not defined'
            }), 403
            
        # Kiểm tra role (case-insensitive)
        if current_user.get('role').upper() != 'MANAGER': 
            return jsonify({
                'success': False,
                'message': 'Admin privileges required'
            }), 403
        return f(current_user, *args, **kwargs)
    return decorated


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
    
    is_valid, user = user_service.verify_credentials(email, password)
    if is_valid and user:
        # Generate tokens
        access_token = user_service.generate_access_token(user.id)
        refresh_token = user_service.generate_refresh_token(user.id)
        
        # Create response
        response = make_response(jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user_service._format_user_data(user),
                'role': user.role.value if user.role else None  # Thêm role vào response
            }
        }))
        
        # Set cookies
        # Access token expires in 15 minutes
        response.set_cookie(
            'access_token', 
            access_token, 
            httponly=True, 
            secure=True, 
            samesite='None',
            max_age=15*60  # 15 minutes in seconds
        )
        
        # Refresh token expires in 7 days
        response.set_cookie(
            'refresh_token', 
            refresh_token, 
            httponly=True, 
            secure=True, 
            samesite='None',
            max_age=7*24*60*60  # 7 days in seconds
        )
        
        return response, 200
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid email or password'
        }), 401

# yêu cầu làm mới access token 
@auth_bp.route('/refresh/', methods=['POST'])
def refresh_token():
    # Luôn ưu tiên lấy từ cookie trước
    refresh_token = request.cookies.get('refresh_token')
    
    # Chỉ kiểm tra body nếu không có trong cookie
    if not refresh_token:
        data = request.get_json() or {}
        refresh_token = data.get('refresh_token')
    
    if not refresh_token:
        return jsonify({
            'success': False,
            'message': 'Refresh token is required'
        }), 400
        
    # Verify refresh token
    is_valid, payload = user_service.verify_token(refresh_token)
    if not is_valid:
        return jsonify({
            'success': False,
            'message': payload.get('error', 'Invalid refresh token')
        }), 401
        
    # Generate new access token
    user_id = payload.get('sub')
    if not user_id:
        return jsonify({
            'success': False,
            'message': 'Invalid token payload'
        }), 401
        
    new_access_token = user_service.generate_access_token(user_id)
    
    # Create response
    response = make_response(jsonify({
        'success': True,
        'message': 'Token refreshed successfully',
        'data': {
            'access_token': new_access_token
        }
    }))
    
    # Set new access token cookie
    response.set_cookie(
        'access_token', 
        new_access_token, 
        httponly=True, 
        secure=True, 
        samesite='None',
        max_age=15*60  # 15 minutes in seconds
    )
    
    return response, 200

# kiểm tra token còn hợp lệ không ?
@auth_bp.route('/validate/', methods=['POST'])
def validate_token():
    token = None
    # Check if token is in headers
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
    
    # If not in headers, check cookies
    if not token and 'access_token' in request.cookies:
        token = request.cookies.get('access_token')
    
    # If still not found, check request body
    if not token:
        data = request.get_json() or {}
        token = data.get('token')

    if not token:
        return jsonify({
            'success': False,
            'message': 'Token is required'
        }), 400
        
    # Verify token
    is_valid, payload = user_service.verify_token(token)
    if not is_valid:
        return jsonify({
            'success': False,
            'message': payload.get('error', 'Invalid token')
        }), 401
        
    return jsonify({
        'success': True,
        'message': 'Token is valid',
        'data': {
            'user_id': payload.get('sub')
        }
    }), 200

@auth_bp.route('/logout/', methods=['POST'])
def logout():
    try:
        response = make_response(jsonify({
            'success': True,
            'message': 'Logout successful'
        }))
        
        # Delete cookies by setting them to empty and expiring them
        response.set_cookie('access_token', '', expires=0)
        response.set_cookie('refresh_token', '', expires=0)
        
        return response, 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Logout failed',
            'error': str(e)
        }), 500

# lấy thông tin user hiện tại
@auth_bp.route('/me/', methods=['GET'])
@token_required
def get_current_user(current_user):
    try:
        if not current_user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
            
        return jsonify({
            'success': True,
            'data': current_user
        }), 200
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': 'Failed to get user info',
            'error': str(e)
        }), 500
