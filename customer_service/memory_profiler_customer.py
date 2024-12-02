from memory_profiler import memory_usage, profile
from services.customer_service import (
    register_customer, delete_customer, update_customer,
    get_all_customers, get_customer_by_username,
    charge_wallet, deduct_wallet, authenticate_customer
)

def memory_profile_functions(app):
    """
    Profile memory usage of customer service functions.

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
        Execute test cases for all customer service functions.
        """
        data = {
            "full_name": "Memory Test",
            "username": "memtest",
            "password": "securepassword",
            "age": 30,
            "address": "123 Memory Lane",
            "gender": "Male",
            "marital_status": "Single"
        }

        # Register a customer
        try:
            profile_memory(register_customer, data)
        except:
            pass

        # Get all customers
        profile_memory(get_all_customers)

        # Get customer by username
        profile_memory(get_customer_by_username, "memtest")

        # Update customer details
        profile_memory(update_customer, "memtest", {"age": 31})

        # Charge the customer's wallet
        profile_memory(charge_wallet, "memtest", 100)

        # Deduct from the customer's wallet
        profile_memory(deduct_wallet, "memtest", 50)

        # Authenticate the customer
        profile_memory(authenticate_customer, "memtest", "securepassword")

        # Delete the customer
        try:
            profile_memory(delete_customer, "memtest")
        except:
            pass

    # Run the profiler within the Flask app context
    with app.app_context():
        test_cases()


if __name__ == "__main__":
    memory_profile_functions()