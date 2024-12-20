from flask import Blueprint, request, jsonify
from services.customer_service import (
    register_customer, delete_customer, update_customer,
    get_all_customers, get_customer_by_username,
    charge_wallet, deduct_wallet, authenticate_customer
)
from utils.security import create_token, get_user_from_token, get_all_user_from_token
from utils.database import check_db_connection
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from line_profiler import LineProfiler
import time
from functools import wraps
customer_bp = Blueprint('customer_bp', __name__)

limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"], 
    storage_uri="memory://",  
)



@customer_bp.route('/health')
def health_check():
    """
    Check the health status of the service.

    Returns:
        Response: A JSON object with the service health status,
        database connection status, and uptime.
    """
    results = check_db_connection()
    db_status = results[0]
    elapsed_time = results[1]
    status = {
        "service": "customer-service",
        "status": "healthy" if db_status else "unhealthy",
        "db_connection": db_status,
        "uptime": elapsed_time
    }
    return jsonify(status), 200 if db_status else 503


@customer_bp.route('/register', methods=['POST'])
@limiter.limit("10 per minute")  

def register():
    """
    Register a new customer.

    Request:
        JSON object with customer details.

    Returns:
        Response: A success message on successful registration
        or an error message on failure.
    """
    data = request.get_json()
    try:
        customer = register_customer(data)
        return jsonify({'message': 'Customer registered successfully.'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@customer_bp.route('/<username>', methods=['DELETE'])
@limiter.limit("5 per minute")

def delete(username):
    """
    Delete a customer by username.

    Args:
        username (str): The username of the customer to delete.

    Returns:
        Response: A success message on successful deletion
        or an error message if the customer is not found.
    """
    try:
        delete_customer(username)
        return jsonify({'message': 'Customer deleted successfully.'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@customer_bp.route('/<username>', methods=['PUT'])
@limiter.limit("5 per minute")
def update(username):
    """
    Update customer details by username.

    Args:
        username (str): The username of the customer to update.

    Returns:
        Response: A success message on successful update
        or an error message on failure.
    """
    data = request.get_json()
    try:
        current_user = get_user_from_token(request)[0]
        if current_user != username:
            return jsonify({'error': 'Access denied: Unauthorized user.'}), 403

        customer = update_customer(username, data)
        return jsonify({'message': 'Customer updated successfully.'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@customer_bp.route('/', methods=['GET'])
@limiter.limit("20 per minute")

def get_all():
    """
    Retrieve all customers.

    Returns:
        Response: A list of all customers in JSON format.
    """
    current_user = get_user_from_token(request)[0]
    if current_user != "admin":
        return jsonify({"error":"Action not allowed"}),400
    customers = get_all_customers()
    return jsonify([customer.to_dict() for customer in customers]), 200

@customer_bp.route('/<username>', methods=['GET'])
@limiter.limit("10 per minute")

def get_by_username(username):
    """
    Retrieve customer details by username.

    Args:
        username (str): The username of the customer.

    Returns:
        Response: A JSON object with the customer's details
        or an error message if not found.
    """
    customer = get_customer_by_username(username)
    if customer:
        return jsonify(customer.to_dict()), 200
    else:
        return jsonify({'error': 'Customer not found.'}), 404

@customer_bp.route('/charge', methods=['POST'])
@limiter.limit("10 per minute")

def charge():
    """
    Charge a customer's wallet.

    Request:
        JSON object with the amount to charge.

    Returns:
        Response: The new wallet balance or an error message.
    """
    current_user = get_user_from_token(request)[0]
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
@limiter.limit("10 per minute")

def deduct():
    """
    Deduct an amount from the customer's wallet.

    Request:
        JSON object with the amount to deduct.

    Returns:
        Response: A success message and the updated wallet balance,
        or an error message on failure.
    """
    try:
        current_user = get_user_from_token(request)[0]
        data = request.get_json()
        amount = data.get('amount')

        if amount is None or amount <= 0:
            return jsonify({'error': 'Invalid amount provided'}), 400

        updated_wallet = deduct_wallet(current_user, amount)
        return jsonify({'message': 'Amount deducted successfully', 'wallet_balance': updated_wallet}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")

def login():
    """
    Authenticate a customer and provide an access token.

    Request:
        JSON object with username and password.

    Returns:
        Response: An access token on successful authentication
        or an error message on failure.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        customer = authenticate_customer(username, password)
        if not customer:
            return jsonify({'error': 'Invalid username or password'}), 401

        access_token = create_token(customer.id)
        return jsonify({'access_token': access_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/get_user_from_token', methods=['POST'])
@limiter.limit("5 per minute")

def get_user_from_token_api():
    """
    Retrieve user details from a token.

    Returns:
        Response: A JSON object with the user's details
        or an error message on failure.
    """
    try:
        current_user = get_all_user_from_token(request)[0]
        if current_user is None:
            return jsonify({'error': 'Invalid request.'}), 400
        return jsonify(current_user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
