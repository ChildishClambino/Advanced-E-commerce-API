from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash
from app.models.models import db, User
from app.services.auth_service import create_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json

        # Validate input
        if not data or not all(key in data for key in ('username', 'password')):
            return jsonify({'error': 'Username and password are required'}), 400

        username = data['username']
        password = data['password']

        # Hash the password and save the user
        hashed_password = generate_password_hash(password)
        user = create_user(username, hashed_password)

        return jsonify({'message': f'User {user.username} created successfully!'}), 201
    except Exception as e:
        current_app.logger.error(f"Error in /register: {str(e)}")
        return jsonify({'error': str(e)}), 500
