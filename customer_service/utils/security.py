from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

def hash_password(password):
    """
    Hashes a plain-text password.
    :param password: Plain-text password
    :return: Hashed password
    """
    return generate_password_hash(password)

def verify_password(password, hashed_password):
    """
    Verifies a plain-text password against a hashed password.
    :param password: Plain-text password
    :param hashed_password: Hashed password
    :return: True if the password matches, False otherwise
    """
    return check_password_hash(hashed_password, password)

SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"

def create_token(user_id):
    payload = {
        'exp': datetime.datetime.now() + datetime.timedelta(days=4),
        'iat': datetime.datetime.now() - datetime.timedelta(hours=10),
        'sub': str(user_id)
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )

def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get('Authorization')
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None

def decode_token(token):
    print("HON")
    print(type(token))
    print(SECRET_KEY)
    payload = jwt.decode(token, str(SECRET_KEY), "HS256")
    print("EWWW")
    print("payload")
    return payload['sub']

from flask import jsonify, abort
from models.customer import Customer

def get_user_from_token(request):
    """
    Extracts and validates the user from a given token in the request.

    Args:
        request: The Flask request object containing the authorization header.

    Returns:
        JSON response containing user information or error message.
    """
    # Extract token from request headers
    token = extract_auth_token(request)
    if not token:
        return jsonify({"error": "Token not provided!"}), 499

    try:
        # Remove 'Bearer ' prefix if present
        token = token.replace("Bearer ", "")
        print(token)
        # Decode the token to get the user identity (usually user_id or username)
        print("DECODING")
        user_id = decode_token(token)
        print('kan')
        print(user_id)
        #user_id = decoded_data.get("sub")  # Assuming the user identity is stored in the 'sub' claim
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid Token!"}), 498
    try:
        # Query the database for the user
        user = Customer.query.filter_by(id=user_id).first()
    except Exception:
        abort(500)

    if not user:
        return jsonify({"error": "Invalid Token!"}), 498

    # Serialize the user object
    return user.username, 200

def get_all_user_from_token(request):
    """
    Extracts and validates the user from a given token in the request.

    Args:
        request: The Flask request object containing the authorization header.

    Returns:
        JSON response containing user information or error message.
    """
    # Extract token from request headers
    token = extract_auth_token(request)
    if not token:
        return jsonify({"error": "Token not provided!"}), 499

    try:
        # Remove 'Bearer ' prefix if present
        token = token.replace("Bearer ", "")
        print(token)
        # Decode the token to get the user identity (usually user_id or username)
        print("DECODING")
        user_id = decode_token(token)
        print('kan')
        print(user_id)
        #user_id = decoded_data.get("sub")  # Assuming the user identity is stored in the 'sub' claim
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid Token!"}), 498
    try:
        # Query the database for the user
        user = Customer.query.filter_by(id=user_id).first()
    except Exception:
        abort(500)

    if not user:
        return jsonify({"error": "Invalid Token!"}), 498

    # Serialize the user object
    return user, 200
