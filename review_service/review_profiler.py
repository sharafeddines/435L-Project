from line_profiler import LineProfiler
from services.review_service import (
    add_review, update_review, delete_review, 
    get_all_reviews_by_product, get_all_reviews_by_customer,
    get_specific_review_details, flag_review, delete_review_admin
)
from review_service import create_app

def profile_functions(app):
    # Initialize the line profiler
    profiler = LineProfiler()

    # Add the review-related functions to the profiler
    profiler.add_function(add_review)
    profiler.add_function(update_review)
    profiler.add_function(delete_review)
    profiler.add_function(get_all_reviews_by_product)
    profiler.add_function(get_all_reviews_by_customer)
    profiler.add_function(get_specific_review_details)
    profiler.add_function(flag_review)
    profiler.add_function(delete_review_admin)

    def test_cases():
        # Test data for the functions
        user_id = 1
        prod_id = 1001
        review_data = {
            "rating": 4,
            "description": "Great product!"
        }

        # Run test cases for profiling
        try:
            # Add a review
            new_review = add_review(user_id, prod_id, review_data)

            # Update the review
            update_review(user_id, prod_id, {"rating": 5, "description": "Excellent product!"})

            # Get all reviews by product
            get_all_reviews_by_product(prod_id)

            # Get all reviews by customer
            get_all_reviews_by_customer(user_id)

            # Get specific review details
            dummy_item = {"name": "Product Name"}
            dummy_customer = {"username": "test_user"}
            get_specific_review_details(new_review, dummy_item, dummy_customer)

            # Flag a review
            flag_review(new_review.id)

            # Delete the review
            delete_review(user_id, prod_id)

        except Exception as e:
            print(f"Error during testing: {e}")

    # Run the profiler within the Flask application context
    with app.app_context():
        profiler.runcall(test_cases)
        profiler.print_stats()

if __name__ == "__main__":
    app = create_app()
    profile_functions(app)
