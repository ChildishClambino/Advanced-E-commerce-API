from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import CustomerAccount, db, User

def register_user(username, password):
    """Register a new user."""
    if CustomerAccount.query.filter_by(username=username).first():
        return {'error': 'Username already exists'}

    hashed_password = generate_password_hash(password)
    new_user = CustomerAccount(username=username, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User registered successfully'}
    except Exception as e:
        return {'error': f"Error registering user: {str(e)}"}


def validate_user(username, password):
    """Validate user credentials."""
    user = CustomerAccount.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None

def create_user(username, hashed_password):
    """Creates a new user in the database."""
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user