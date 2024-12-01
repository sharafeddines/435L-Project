from utils.database import db

class Review(db.Model):
    """
    Represents a review in the system.

    Attributes:
        id (int): The primary key of the review.
        customer_id (int): The ID of the customer who wrote the review.
        product_id (int): The ID of the product being reviewed.
        rating (int): The rating given by the customer, on a scale (e.g., 1-5).
        description (str): An optional text description of the review.
        flagged (bool): A flag indicating if the review has been flagged for administrative attention.
    """
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    flagged = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        """
        Converts the Review object into a dictionary representation.

        :return: A dictionary with review details.
        :rtype: dict
        """
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "rating": self.rating,
            "description": self.description,
            "flagged": self.flagged,
        }
