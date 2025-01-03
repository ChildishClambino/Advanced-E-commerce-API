from flask import Blueprint, request, jsonify, current_app
from app.services.auth_service import register_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json

        # Validate input
        if not data or not all(key in data for key in ('username', 'password', 'role')):
            return jsonify({'error': 'Username, password, and role are required'}), 400

        # Call the service to register the user
        result = register_user(data['username'], data['password'], data['role'])
        if 'error' in result:
            return jsonify(result), 400

        return jsonify(result), 201
    except Exception as e:
        current_app.logger.error(f"Error in /register: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
