from models.inventory import Goods
from utils.database import db

def add_goods(data):
    new_goods = Goods(
        name=data["name"],
        category=data["category"],
        price_per_item=data["price_per_item"],
        description=data.get("description", ""),
        count_in_stock=data["count_in_stock"],
    )
    db.session.add(new_goods)
    db.session.commit()
    return new_goods

def deduct_goods(item_id, count):
    goods = Goods.query.get(item_id)
    if not goods:
        raise ValueError("Item not found")
    if goods.count_in_stock < count:
        raise ValueError("Insufficient stock")
    goods.count_in_stock -= count
    db.session.commit()
    return goods

def update_goods(item_id, update_data):
    goods = Goods.query.get(item_id)
    if not goods:
        raise ValueError("Item not found")

    for key, value in update_data.items():
        if hasattr(goods, key):
            setattr(goods, key, value)

    db.session.commit()
    return goods
