from memory_profiler import memory_usage
from services.review_service import (
    add_review, update_review, delete_review,
    get_all_reviews_by_product, get_all_reviews_by_customer,
    flag_review, delete_review_admin, get_specific_review_details
)
from review_service import create_app

def memory_profile_functions(app):
    """
    Profile memory usage of review service functions.

    Args:
        app (Flask): The Flask application instance.
    """
    def profile_memory(func, *args, **kwargs):
        """
        Run memory profiling for a given function.

        Args:
            func (callable): The function to be profiled.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Any: The result of the function call.
        """
        mem_usage = memory_usage((func, args, kwargs), interval=0.1)
        result = func(*args, **kwargs)
        print(f"Memory usage for {func.__name__}: {mem_usage}")
        return result

    def test_cases():
        """
        Execute test cases for all review service functions.
        """
        # Sample test data
        user_id = 1
        prod_id = 101
        review_data = {"rating": 4, "description": "Great product!"}
        update_data = {"rating": 5, "description": "Updated review."}
        item = {"name": "Sample Product"}
        customer = {"username": "user1"}

        # Add a review
        try:
            profile_memory(add_review, user_id, prod_id, review_data)
        except:
            pass

        # Update a review
        try:
            profile_memory(update_review, user_id, prod_id, update_data)
        except:
            pass

        # Get all reviews by product
        profile_memory(get_all_reviews_by_product, prod_id)

        # Get all reviews by customer
        profile_memory(get_all_reviews_by_customer, user_id)

        # Get specific review details
        review = add_review(user_id, prod_id, review_data)  # Assuming this creates a test review
        profile_memory(get_specific_review_details, review, item, customer)

        # Flag a review
        profile_memory(flag_review, review.id)

        # Delete a review
        profile_memory(delete_review, user_id, prod_id)

        # Delete review as admin
        try:
            profile_memory(delete_review_admin, review.id)
        except:
            pass

    # Run the profiler within the Flask app context
    with app.app_context():
        test_cases()


if __name__ == "__main__":
    app = create_app()
    memory_profile_functions(app)
