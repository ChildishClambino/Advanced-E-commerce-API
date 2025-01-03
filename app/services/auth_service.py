from werkzeug.security import generate_password_hash
from app.models.models import db, User

def register_user(username, password, role):
    """Register a new user."""
    try:
        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            return {'error': 'Username already exists'}

        # Create a new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return {'message': f'User {username} registered successfully'}
    except Exception as e:
        return {'error': f"Error registering user: {str(e)}"}
