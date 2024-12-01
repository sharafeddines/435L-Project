from utils.database import db

class Sales(db.Model):
    """
    Represents a sales record in the database.

    Attributes:
        id (int): The primary key of the sales record.
        customer_id (int): The ID of the customer who made the purchase.
        product_id (int): The ID of the product purchased.
        quantity (int): The quantity of the product purchased.
    """
    __tablename__ = "sales"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    def to_dict(self):
        """
        Converts the Sales object into a dictionary representation.

        :return: A dictionary with the sales record details.
        :rtype: dict
        """
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "quantity": self.quantity
        }
