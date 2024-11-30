from sqlalchemy import Column, String, Integer, Float, Boolean
from utils.database import db

class Customer(db.Model):
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
            "is_admin" : self.is_admin
        }

    def __repr__(self):
        return f'<Customer {self.username}>'
