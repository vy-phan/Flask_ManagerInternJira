from flask import Blueprint, jsonify

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login/', methods=['POST'])
def login():
    return jsonify({
            'success': True,
            'message': 'Login successful'
        }), 200

@auth_bp.route('/logout/', methods=['POST'])
def logout():
    return jsonify({
           'success': True,
           'message': 'Logout successful'
        }), 200