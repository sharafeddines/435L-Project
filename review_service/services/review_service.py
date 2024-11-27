from models.review import Review
from utils.database import db

def add_review(user_id, prod_id, data):
    if user_id == None or prod_id == None:
        raise ValueError("Fields not found.")
    new_review = Review(
        customer_id=user_id,
        product_id=prod_id,
        rating=data["rating"],
        description=data.get("description", ""),
        flagged=data["flagged"],
    )
    try:
        db.session.add(new_review)
        db.session.commit()
        return new_review
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Failed to add review due to a database integrity error.")

def update_review(username ,data):
    pass
        


def get_all_reviews():
    pass
