from flask import Blueprint, jsonify, request, current_app
from app.models.models import db, Customer

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/customers', methods=['GET'])
def get_customers():
    try:
        customers = Customer.query.all()
        return jsonify([customer.to_dict() for customer in customers]), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching customers: {e}")
        return jsonify({'error': 'Failed to fetch customers'}), 500

@customers_bp.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    try:
        customer = Customer.query.get_or_404(id)
        return jsonify(customer.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching customer {id}: {e}")
        return jsonify({'error': 'Customer not found'}), 404

@customers_bp.route('/customers', methods=['POST'])
def create_customer():
    try:
        data = request.json
        if not data or not all(key in data for key in ['name', 'email']):
            return jsonify({'error': 'Name and email are required'}), 400
        
        customer = Customer(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', None)
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify(customer.to_dict()), 201
    except Exception as e:
        current_app.logger.error(f"Error creating customer: {e}")
        return jsonify({'error': 'Failed to create customer'}), 500

@customers_bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    try:
        customer = Customer.query.get_or_404(id)
        data = request.json

        customer.name = data.get('name', customer.name)
        customer.email = data.get('email', customer.email)
        customer.phone = data.get('phone', customer.phone)

        db.session.commit()
        return jsonify(customer.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f"Error updating customer {id}: {e}")
        return jsonify({'error': 'Failed to update customer'}), 500

@customers_bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        customer = Customer.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': f'Customer {id} deleted successfully'}), 200
    except Exception as e:
        current_app.logger.error(f"Error deleting customer {id}: {e}")
        return jsonify({'error': 'Failed to delete customer'}), 500
