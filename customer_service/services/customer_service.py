from models.customer import Customer
from utils.database import db
from utils.security import hash_password, verify_password
from memory_profiler import profile
import time

@profile
def register_customer(data, is_admin=False):
    """
    Register a new customer.

    Args:
        data (dict): A dictionary containing customer details such as full_name, 
            username, password, age, address, gender, and marital_status.
        is_admin (bool, optional): Specifies if the customer is an admin. Defaults to False.

    Raises:
        ValueError: If a customer with the provided username already exists.

    Returns:
        Customer: The newly registered customer object.
    """
    if Customer.query.filter_by(username=data['username']).first():
        raise ValueError('Username already exists.')

    password_hash = hash_password(data['password'])
    new_customer = Customer(
        full_name=data['full_name'],
        username=data['username'],
        password_hash=password_hash,
        age=data.get('age'),
        address=data.get('address'),
        gender=data.get('gender'),
        marital_status=data.get('marital_status')
    )
    new_customer.is_admin = is_admin
    db.session.add(new_customer)
    db.session.commit()
    return new_customer

@profile
def delete_customer(username):
    """
    Delete a customer by username.

    Args:
        username (str): The username of the customer to delete.

    Raises:
        ValueError: If the customer is not found.
    """
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        raise ValueError('Customer not found.')
    db.session.delete(customer)
    db.session.commit()

@profile
def update_customer(username, data):
    """
    Update the details of a customer.

    Args:
        username (str): The username of the customer to update.
        data (dict): A dictionary containing the fields to update.

    Raises:
        ValueError: If the customer is not found.

    Returns:
        Customer: The updated customer object.
    """
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        raise ValueError('Customer not found.')

    for key, value in data.items():
        if key == 'password':
            setattr(customer, 'password_hash', hash_password(value))
        else:
            setattr(customer, key, value)
    db.session.commit()
    return customer

@profile
def get_all_customers():
    """
    Retrieve all customers.

    Returns:
        list: A list of all customer objects.
    """
    return Customer.query.all()

@profile
def get_customer_by_username(username):
    """
    Retrieve a customer by username.

    Args:
        username (str): The username of the customer to retrieve.

    Returns:
        Customer: The customer object if found, else None.
    """
    return Customer.query.filter_by(username=username).first()

@profile
def charge_wallet(username, amount):
    """
    Charge a customer's wallet by a specific amount.

    Args:
        username (str): The username of the customer.
        amount (float): The amount to add to the wallet.

    Raises:
        ValueError: If the customer is not found or the amount is invalid.

    Returns:
        float: The updated wallet balance.
    """
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        raise ValueError('Customer not found.')
    if amount <= 0:
        raise ValueError('Need to charge a positive amount')
    customer.wallet_balance += amount
    db.session.commit()
    return customer.wallet_balance

@profile
def deduct_wallet(username, amount):
    """
    Deduct a specific amount from a customer's wallet.

    Args:
        username (str): The username of the customer.
        amount (float): The amount to deduct.

    Raises:
        ValueError: If the customer is not found or the balance is insufficient.

    Returns:
        float: The updated wallet balance.
    """
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        raise ValueError('Customer not found.')
    if customer.wallet_balance < amount:
        raise ValueError('Insufficient balance.')
    customer.wallet_balance -= amount
    db.session.commit()
    return customer.wallet_balance
@profile
def authenticate_customer(username, password):
    """
    Authenticate a customer using username and password.

    Args:
        username (str): The customer's username.
        password (str): The customer's password.

    Returns:
        Customer: The customer object if authentication is successful, else None.
    """
    customer = Customer.query.filter_by(username=username).first()
    if not customer or not verify_password(password, customer.password_hash):
        return None
    return customer
