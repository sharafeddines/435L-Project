from utils.database import db
from models.sales import Sales

def add_sale(data):
    """
    Add a new sales record to the database.

    :param data: A dictionary containing the sales details, including:
        - "customer_id" (int): The ID of the customer making the purchase.
        - "product_id" (int): The ID of the product being purchased.
        - "quantity" (int): The quantity of the product purchased.
    :type data: dict
    :return: The newly created Sales object.
    :rtype: Sales
    """    
    new_sale = Sales(
        customer_id=data["customer_id"],
        product_id=data["product_id"],
        quantity=data["quantity"],
    )
    db.session.add(new_sale)
    db.session.commit()
    return new_sale


