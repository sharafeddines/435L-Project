from line_profiler import LineProfiler
from services.sales_service import (
    add_sale
)

def profile_functions(app):
    # Initialize the line profiler
    profiler = LineProfiler()

    # Add the review-related functions to the profiler
    profiler.add_function(add_sale)

    def test_cases():
        # Test data
        data = {
            "customer_id": 1,
            "product_id": 101,
            "quantity": 2
        }
        # Call the add_sale function
        new_sale = add_sale(data)

    # Run the profiler within the Flask application context
    with app.app_context():
        profiler.runcall(test_cases)
        profiler.print_stats()

if __name__ == "__main__":
    profile_functions()
