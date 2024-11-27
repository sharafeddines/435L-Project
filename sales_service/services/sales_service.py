from utils.database import db
from models.sales import Sales

def add_sale(data):
    
    new_sale = Sales(
        customer_id=data["customer_id"],
        product_id=data["product_id"],
        quantity=data["quantity"],
    )
    db.session.add(new_sale)
    db.session.commit()
    return new_sale


