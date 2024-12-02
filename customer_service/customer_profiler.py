import time
from line_profiler import LineProfiler
from services.customer_service import (
    register_customer, delete_customer, update_customer,
    get_all_customers, get_customer_by_username,
    charge_wallet, deduct_wallet, authenticate_customer
)
from customers_service import create_app

def profile_functions(app):
    profiler = LineProfiler()
    # Add all functions to be profiled
    profiler.add_function(register_customer)
    profiler.add_function(delete_customer)
    profiler.add_function(update_customer)
    profiler.add_function(get_all_customers)
    profiler.add_function(get_customer_by_username)
    profiler.add_function(charge_wallet)
    profiler.add_function(deduct_wallet)
    profiler.add_function(authenticate_customer)
    
    def test_cases():
        # Simulated test data
        data = {
            "full_name": "omar",
            "username": "obk",
            "password": "securepassword",
            "age": 30,
            "address": "beirut",
            "gender": "Male",
            "marital_status": "Single"
        }

        try:
            # Test register_customer
            register_customer(data)

            # Test get_all_customers
            all_customers = get_all_customers()
            print(f"Total customers: {len(all_customers)}")

            # Test get_customer_by_username
            customer = get_customer_by_username("obk")
            print(f"Customer retrieved: {customer.full_name}")

            # Test update_customer
            update_customer("obk", {"age": 31})
            
            # Test charge_wallet
            new_balance = charge_wallet("obk", 100)
            print(f"New wallet balance after charging: {new_balance}")
            
            # Test deduct_wallet
            new_balance = deduct_wallet("obk", 50)
            print(f"New wallet balance after deduction: {new_balance}")

            # Test authenticate_customer
            authenticated = authenticate_customer("obk", "securepassword")
            print(f"Authentication successful: {authenticated is not None}")
            
            # Test delete_customer
            delete_customer("obk")
            print("Customer deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")

    # Run the profiler with Flask app context
    with app.app_context():
        profiler.runcall(test_cases)
        profiler.print_stats()

if __name__ == "__main__":
    app = create_app()
    profile_functions(app)
