from memory_profiler import memory_usage
from services.sales_service import add_sale
from sales_service import create_app

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
        data = {
            "customer_id": 1,
            "product_id": 101,
            "quantity": 2
        }

        # Add a review
        try:
            profile_memory(add_sale, data)
        except:
            pass

    # Run the profiler within the Flask app context
    with app.app_context():
        test_cases()


if __name__ == "__main__":
    app = create_app()
    memory_profile_functions(app)
