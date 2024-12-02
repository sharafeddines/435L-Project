import time
from line_profiler import LineProfiler
from services.customer_service import (
    register_customer, delete_customer, update_customer,
    get_all_customers, get_customer_by_username,
    charge_wallet, deduct_wallet, authenticate_customer
)

def profile_functions(app):
    profiler = LineProfiler()
    profiler.add_function(register_customer)
    profiler.add_function(delete_customer)
    profiler.add_function(update_customer)
    profiler.add_function(get_all_customers)
    profiler.add_function(get_customer_by_username)
    profiler.add_function(charge_wallet)
    profiler.add_function(deduct_wallet)
    profiler.add_function(authenticate_customer)
    
    def test_cases():
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
            register_customer(data)
            get_customer_by_username("obk")
            update_customer("obk", {"age": 31})
            charge_wallet("obk", 100)
            deduct_wallet("obk", 50)
            delete_customer("obk")
        except Exception as e:
            print(f"Error: {e}")

    with app.app_context():
        profiler.runcall(test_cases)
        profiler.print_stats()

if __name__ == "__main__":
    profile_functions()
