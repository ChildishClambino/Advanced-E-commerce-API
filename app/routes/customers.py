from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import Customer, db

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/customers', methods=['POST'])
@jwt_required()
def create_customer():
    """Create a new customer."""
    try:
        data = request.json
        if not data or not all(key in data for key in ('name', 'email')):
            return jsonify({'error': 'Name and email are required'}), 400

        # Create a new customer
        new_customer = Customer(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone')
        )
        db.session.add(new_customer)
        db.session.commit()

        return jsonify(new_customer.to_dict()), 201

    except Exception as e:
        current_app.logger.error(f"Error in create_customer: {e}")
        return jsonify({'error': str(e)}), 500


@customers_bp.route('/customers/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_customer(customer_id):
    """Retrieve a customer by ID."""
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        return jsonify(customer.to_dict())
    except Exception as e:
        current_app.logger.error(f"Error in get_customer: {str(e)}")
        return jsonify({'error': str(e)}), 500


@customers_bp.route('/customers', methods=['GET'])
@jwt_required()
def get_all_customers():
    """Retrieve all customers."""
    try:
        customers = Customer.query.all()
        return jsonify([customer.to_dict() for customer in customers])
    except Exception as e:
        current_app.logger.error(f"Error in get_all_customers: {str(e)}")
        return jsonify({'error': str(e)}), 500


@customers_bp.route('/customers/<int:customer_id>', methods=['PUT'])
@jwt_required()
def update_customer(customer_id):
    """Update a customer's details."""
    try:
        data = request.json
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404

        # Update customer details
        customer.name = data.get('name', customer.name)
        customer.email = data.get('email', customer.email)
        customer.phone = data.get('phone', customer.phone)

        db.session.commit()
        return jsonify(customer.to_dict())
    except Exception as e:
        current_app.logger.error(f"Error in update_customer: {str(e)}")
        return jsonify({'error': str(e)}), 500


@customers_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
@jwt_required()
def delete_customer(customer_id):
    """Delete a customer by ID."""
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404

        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'}), 200
    except Exception as e:
        current_app.logger.error(f"Error in delete_customer: {str(e)}")
        return jsonify({'error': str(e)}), 500


@customers_bp.route('/db-test', methods=['GET'])
def db_test():
    """Test database connectivity."""
    try:
        with db.engine.connect() as conn:
            result = conn.execute("SELECT 1")
            return jsonify({"db_status": "Connected", "result": [row for row in result]}), 200
    except Exception as e:
        current_app.logger.error(f"Database connection failed: {e}")
        return jsonify({"error": str(e)}), 500
