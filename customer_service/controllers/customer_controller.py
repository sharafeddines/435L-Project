from flask import Blueprint, request, jsonify
from services.customer_service import (
    register_customer, delete_customer, update_customer,
    get_all_customers, get_customer_by_username,
    charge_wallet, deduct_wallet, authenticate_customer
)
from utils.security import create_token, get_user_from_token, get_all_user_from_token
from utils.database import check_db_connection
from flask_jwt_extended import jwt_required, get_jwt_identity

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('/health')
def health_check():
    results = check_db_connection()
    db_status = results[0]
    elapsed_time = results[1]
    status = {
        "service": "backend-service-1",
        "status": "healthy" if db_status else "unhealthy",
        "db_connection": db_status,
        "uptime": elapsed_time
    }
    return jsonify(status), 200 if db_status else 503


@customer_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        customer = register_customer(data)
        return jsonify({'message': 'Customer registered successfully.'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@customer_bp.route('/<username>', methods=['DELETE'])
def delete(username):
    try:
        delete_customer(username)
        return jsonify({'message': 'Customer deleted successfully.'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@customer_bp.route('/<username>', methods=['PUT'])
def update(username):
    data = request.get_json()
    try:
        print("HEREEEEEEE")
        # Get the identity of the current user from the token
        current_user = get_user_from_token(request)[0]
        print(current_user)
        # Ensure the token identity matches the username in the request
        if current_user != username:
            return jsonify({'error': 'Access denied: Unauthorized user.'}), 403

        # Update the customer if the identity matches
        customer = update_customer(username, data)
        return jsonify({'message': 'Customer updated successfully.'}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@customer_bp.route('/', methods=['GET'])
def get_all():
    customers = get_all_customers()
    return jsonify([customer.to_dict() for customer in customers]), 200

@customer_bp.route('/<username>', methods=['GET'])
def get_by_username(username):
    customer = get_customer_by_username(username)
    if customer:
        return jsonify(customer.to_dict()), 200
    else:
        return jsonify({'error': 'Customer not found.'}), 404

@customer_bp.route('/charge', methods=['POST'])
def charge():
    print("USERRRRR")
    current_user = get_user_from_token(request)[0]
    print("USERRRRR")
    print(current_user)
    # Ensure the token identity matches the username in the request
    
    data = request.get_json()
    amount = data.get('amount')
    if amount is None or amount <= 0:
        return jsonify({'error': 'Invalid amount.'}), 400
    try:
        new_balance = charge_wallet(current_user, amount)
        return jsonify({'new_balance': new_balance}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@customer_bp.route('/deduct', methods=['POST'])
def deduct():
    try:
        current_user = get_user_from_token(request)[0]
        print(current_user)
        # Ensure the token identity matches the username in the request
        data = request.get_json()
        amount = data.get('amount')

        if amount is None or amount <= 0:
            return jsonify({'error': 'Invalid amount provided'}), 400

        updated_wallet = deduct_wallet(current_user, amount)
        return jsonify({'message': 'Amount deducted successfully', 'wallet_balance': updated_wallet}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        print(username)
        print(password)
        # Authenticate customer
        customer = authenticate_customer(username, password)
        if not customer:
            return jsonify({'error': 'Invalid username or password'}), 401

        # Generate token
        access_token = create_token(customer.id)
        return jsonify({'access_token': access_token}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/get_user_from_token', methods=['POST'])
def get_user_from_token_api():
    try:
        current_user = get_all_user_from_token(request)[0]
        if current_user == None:
            return jsonify({'error': 'Invalid amount provided'}), 400
        return jsonify(current_user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
