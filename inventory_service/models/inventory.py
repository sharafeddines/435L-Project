from utils.database import db

class Inventory(db.Model):
    """
    Represents an inventory item in the database.

    Attributes:
        id (int): The unique identifier for the inventory item.
        name (str): The name of the inventory item (must be unique).
        category (str): The category of the inventory item.
        price_per_item (float): The price per unit of the inventory item.
        description (str, optional): A brief description of the inventory item.
        count_in_stock (int): The quantity of the item available in stock.
    """
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    price_per_item = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    count_in_stock = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """
        Convert the Inventory object to a dictionary for serialization.

        Returns:
            dict: A dictionary representation of the Inventory object, containing:
                - id (int): The unique identifier.
                - name (str): The name of the item.
                - category (str): The category of the item.
                - price_per_item (float): The price per unit.
                - description (str): The description of the item.
                - count_in_stock (int): The quantity in stock.
        """
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price_per_item": self.price_per_item,
            "description": self.description,
            "count_in_stock": self.count_in_stock,
        }
