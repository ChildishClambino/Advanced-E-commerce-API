from flask import Blueprint, request, jsonify
from app.models.models import CustomerAccount, db

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    new_account = CustomerAccount(
        username=data['username'],
        password=data['password'],
        customer_id=data['customer_id']
    )
    db.session.add(new_account)
    db.session.commit()
    return jsonify(new_account.to_dict()), 201

@accounts_bp.route('/accounts/<int:id>', methods=['GET'])
def get_account(id):
    account = CustomerAccount.query.get_or_404(id)
    return jsonify(account.to_dict())

@accounts_bp.route('/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    account = CustomerAccount.query.get_or_404(id)
    data = request.get_json()
    account.username = data.get('username', account.username)
    account.password = data.get('password', account.password)
    db.session.commit()
    return jsonify(account.to_dict())

@accounts_bp.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    account = CustomerAccount.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    return jsonify({'message': 'Account deleted successfully'})
