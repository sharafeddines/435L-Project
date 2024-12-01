from models.review import Review
from utils.database import db

def add_review(user_id, prod_id, data):
    """
    Add a new review to the database.

    :param user_id: The ID of the user submitting the review.
    :type user_id: int
    :param prod_id: The ID of the product being reviewed.
    :type prod_id: int
    :param data: A dictionary containing review details, including "rating" and optional "description".
    :type data: dict
    :raises ValueError: If required fields are missing or if a database integrity error occurs.
    :return: The newly added review object.
    :rtype: Review
    """
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
    """
    Update an existing review.

    :param user_id: The ID of the user updating the review.
    :type user_id: int
    :param prod_id: The ID of the product associated with the review.
    :type prod_id: int
    :param data: A dictionary containing updated review details.
    :type data: dict
    :raises ValueError: If the review is not found or if a database integrity error occurs.
    :return: The updated review object.
    :rtype: Review
    """
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
    """
    Delete a review.

    :param user_id: The ID of the user who wrote the review.
    :type user_id: int
    :param prod_id: The ID of the product associated with the review.
    :type prod_id: int
    :raises ValueError: If the review is not found.
    """
    review = Review.query.filter_by(customer_id=user_id, product_id = prod_id).first()
    if not review:
        raise ValueError('Review not found.')
    db.session.delete(review)
    db.session.commit()
        

def get_all_reviews_by_product(prod_id):
    """
    Retrieve all unflagged reviews for a specific product.

    :param prod_id: The ID of the product.
    :type prod_id: int
    :return: A query object containing the reviews.
    :rtype: sqlalchemy.orm.query.Query
    """
    reviews = Review.query.filter_by(product_id=prod_id, flagged = False)
    return reviews

def get_all_reviews_by_customer(customer_id):
    """
    Retrieve all unflagged reviews submitted by a specific customer.

    :param customer_id: The ID of the customer.
    :type customer_id: int
    :return: A query object containing the reviews.
    :rtype: sqlalchemy.orm.query.Query
    """
    reviews = Review.query.filter_by(customer_id=customer_id, flagged = False)
    return reviews

def get_specific_review_details(review, item, customer):
    """
    Retrieve detailed information about a specific review.

    :param review: The review object.
    :type review: Review
    :param item: A dictionary containing product information.
    :type item: dict
    :param customer: A dictionary containing customer information.
    :type customer: dict
    :return: A dictionary containing detailed review information.
    :rtype: dict
    """
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
    """
    Flag a review for administrative attention.

    :param review_id: The ID of the review to be flagged.
    :type review_id: int
    :raises ValueError: If the review is not found.
    :return: The flagged review object.
    :rtype: Review
    """
    review = Review.query.filter_by(id = review_id).first()
    if not review:
        raise ValueError("No such review exists.")
    review.flagged=True
    db.session.commit()
    return review

def delete_review_admin(review_id):
    """
    Delete a review as an administrator.

    :param review_id: The ID of the review to be deleted.
    :type review_id: int
    :raises ValueError: If the review is not found.
    """
    review = Review.query.filter_by(id = review_id).first()
    if not review:
        raise ValueError("No such review exists.")
    db.session.delete(review)
    db.session.commit()

