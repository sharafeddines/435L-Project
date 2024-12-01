from sqlalchemy import Column, String, Integer, Float, Boolean
from utils.database import db

class Customer(db.Model):
    """
    Represents a Customer entity in the database.

    Attributes:
        id (int): The unique identifier for the customer.
        full_name (str): The full name of the customer.
        username (str): The unique username for the customer.
        password_hash (str): The hashed password for the customer.
        age (int, optional): The age of the customer.
        address (str, optional): The address of the customer.
        gender (str, optional): The gender of the customer.
        marital_status (str, optional): The marital status of the customer.
        wallet_balance (float): The wallet balance of the customer. Default is 0.0.
        is_admin (bool): Indicates if the customer has admin privileges. Default is False.
    """
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    age = Column(Integer)
    address = Column(String(200))
    gender = Column(String(10))
    marital_status = Column(String(20))
    wallet_balance = Column(Float, default=0.0)
    is_admin = Column(Boolean, default=False)

    def to_dict(self):
        """
        Convert the Customer object to a dictionary for serialization.

        Returns:
            dict: A dictionary representation of the Customer object, 
            containing the customer's details.
        """
        return {
            'id': self.id,
            'full_name': self.full_name,
            'username': self.username,
            'age': self.age,
            'address': self.address,
            'gender': self.gender,
            'marital_status': self.marital_status,
            'wallet_balance': self.wallet_balance,
            "is_admin": self.is_admin
        }

    def __repr__(self):
        """
        Returns a string representation of the Customer object.

        Returns:
            str: A string in the format '<Customer username>'.
        """
        return f'<Customer {self.username}>'

