from models.inventory import Inventory
from utils.database import db

def add_goods(data):
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
    goods = Inventory.query.get(item_id)
    if not goods:
        raise ValueError("Item not found")
    if goods.count_in_stock < count:
        raise ValueError("Insufficient stock")
    goods.count_in_stock -= count
    db.session.commit()
    return goods

def update_goods(item_id, update_data):
    goods = Inventory.query.get(item_id)
    if not goods:
        raise ValueError("Item not found")

    for key, value in update_data.items():
        if hasattr(goods, key):
            setattr(goods, key, value)

    db.session.commit()
    return goods

def get_all_inventory():
    return Inventory.query.all()
