from models.inventory import Inventory
from utils.database import db
from sqlalchemy.exc import IntegrityError

def add_goods(data):
    """
    Add new goods to the inventory.

    Args:
        data (dict): A dictionary containing the following keys:
            - name (str): The name of the item.
            - category (str): The category of the item.
            - price_per_item (float): The price per unit of the item.
            - description (str, optional): A brief description of the item.
            - count_in_stock (int): The quantity of the item to be added.

    Raises:
        ValueError: If the item already exists or if there is a database integrity error.

    Returns:
        Inventory: The newly added inventory item.
    """
    existing_goods = Inventory.query.filter_by(name=data["name"]).first()
    if existing_goods:
        raise ValueError("Item already exists.")

    new_goods = Inventory(
        name=data["name"],
        category=data["category"],
        price_per_item=data["price_per_item"],
        description=data.get("description", ""),
        count_in_stock=data["count_in_stock"],
    )
    try:
        db.session.add(new_goods)
        db.session.commit()
        return new_goods
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Failed to add goods due to a database integrity error.")

def deduct_goods(item_id, count):
    """
    Deduct a specific quantity of goods from the inventory.

    Args:
        item_id (int): The ID of the inventory item.
        count (int): The quantity to deduct.

    Raises:
        ValueError: If the item is not found or if the stock is insufficient.

    Returns:
        Inventory: The updated inventory item.
    """
    goods = Inventory.query.get(item_id)
    if not goods:
        raise ValueError("Item not found")
    if goods.count_in_stock < count:
        raise ValueError("Insufficient stock")
    goods.count_in_stock -= count
    db.session.commit()
    return goods

def update_goods(item_id, update_data):
    """
    Update the details of an inventory item.

    Args:
        item_id (int): The ID of the inventory item to update.
        update_data (dict): A dictionary containing the fields to update.

    Raises:
        ValueError: If the item is not found.

    Returns:
        Inventory: The updated inventory item.
    """
    goods = Inventory.query.get(item_id)
    if not goods:
        raise ValueError("Item not found")

    for key, value in update_data.items():
        if hasattr(goods, key):
            setattr(goods, key, value)

    db.session.commit()
    return goods

def get_all_inventory():
    """
    Retrieve all items in the inventory.

    Returns:
        list: A list of all `Inventory` objects.
    """
    return Inventory.query.all()
