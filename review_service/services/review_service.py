from models.review import Review
from utils.database import db

def add_review(user_id, prod_id, data):
    if user_id == None or prod_id == None:
        raise ValueError("Fields not found.")
    new_review = Review(
        customer_id=user_id,
        product_id=prod_id,
        rating=data["rating"],
        description=data.get("description", "")
    )
    try:
        db.session.add(new_review)
        db.session.commit()
        return new_review
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Failed to add review due to a database integrity error.")

def update_review(user_id, prod_id ,data):
    if user_id == None or prod_id == None:
        raise ValueError("Fields not found.")
    review = Review.query.filter_by(customer_id=user_id, product_id = prod_id).first()
    if not review:
        raise ValueError("Review not found.")
    try:
        for key, value in data.items():
            if key == 'product_name':
                setattr(review, 'product_id', prod_id)
            else:
                setattr(review, key, value)
        db.session.commit()
        return review
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Failed to update review due to a database integrity error.")

def delete_review(user_id, prod_id):
    review = Review.query.filter_by(customer_id=user_id, product_id = prod_id).first()
    if not review:
        raise ValueError('Review not found.')
    db.session.delete(review)
    db.session.commit()
        


def get_all_reviews_by_product(prod_id):
    reviews = Review.query.filter_by(product_id=prod_id, flagged = False)
    return reviews

def get_all_reviews_by_customer(customer_id):
    reviews = Review.query.filter_by(customer_id=customer_id, flagged = False)
    return reviews

def get_specific_review_details(review, item, customer):
    return {
        "id": review.id,
        "product_id": review.product_id,
        "customer_id":review.customer_id,
        "username": customer.get("username"), 
        "product_name": item.get("name"),
        "rating": review.rating,
        "description": review.description,
        "flagged": review.flagged      
    }

def flag_review(review_id):
    review = Review.query.filter_by(id = review_id).first()
    if not review:
        raise ValueError("No such review exists.")
    review.flagged=True
    db.session.commit()
    return review

def delete_review_admin(review_id):
    review = Review.query.filter_by(id = review_id).first()
    if not review:
        raise ValueError("No such review exists.")
    db.session.delete(review)
    db.session.commit()

