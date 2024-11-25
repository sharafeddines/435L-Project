from models.customer import Customer
from utils.database import db
from utils.security import hash_password, verify_password

def register_customer(data):
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
    db.session.add(new_customer)
    db.session.commit()
    return new_customer

def delete_customer(username):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        raise ValueError('Customer not found.')
    db.session.delete(customer)
    db.session.commit()

def update_customer(username, data):
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

def get_all_customers():
    return Customer.query.all()

def get_customer_by_username(username):
    return Customer.query.filter_by(username=username).first()

def charge_wallet(username, amount):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        raise ValueError('Customer not found.')
    if amount<=0:
        raise ValueError('Need to charge a positive amount')
    customer.wallet_balance += amount
    db.session.commit()
    return customer.wallet_balance

def deduct_wallet(username, amount):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        raise ValueError('Customer not found.')
    if customer.wallet_balance < amount:
        raise ValueError('Insufficient balance.')
    customer.wallet_balance -= amount
    db.session.commit()
    return customer.wallet_balance

def authenticate_customer(username, password):
    print("authentication")
    customer = Customer.query.filter_by(username=username).first()
    if not customer or not verify_password(password, customer.password_hash):
        return None
    return customer
