from memory_profiler import memory_usage, profile
from services.inventory_service import (
    add_goods, deduct_goods, update_goods, get_all_inventory
)


def memory_profile_functions(app):
    """
    Profile memory usage of inventory service functions.

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
        print(f"Memory usage for {func.__name__}: {mem_usage}")
        return func(*args, **kwargs)

    def test_cases():
        """
        Execute test cases for all inventory service functions.
        """
        try:
            # Add goods to inventory
            existing_inventory = get_all_inventory()
            if not any(item.name == "Laptop" for item in existing_inventory):
                # Add goods to inventory
                new_item = {
                    "name": "Laptop",
                    "category": "Electronics",
                    "price_per_item": 1500.0,
                    "description": "A high-performance laptop",
                    "count_in_stock": 10
                }
                added_item = profile_memory(add_goods, new_item)
                print(f"Added item: {added_item.name}")
            else:
                print("Item 'Laptop' already exists in inventory.")

            # Retrieve the item ID for further operations
            inventory = get_all_inventory()
            item_id = next((item.id for item in inventory if item.name == "Laptop"), None)
            if not item_id:
                raise ValueError("Item ID for 'Laptop' not found in inventory.")

            # Deduct goods from inventory
            profile_memory(deduct_goods, item_id, 2)
            print(f"Deducted 2 units from item ID {item_id}")

            # Update goods details
            update_data = {"price_per_item": 1400.0, "description": "Discounted laptop"}
            updated_item = profile_memory(update_goods, item_id, update_data)
            print(f"Updated item: {updated_item.name}, New price: {updated_item.price_per_item}")

            # Retrieve all inventory items
            inventory = profile_memory(get_all_inventory)
            print(f"Total inventory items: {len(inventory)}")

        except Exception as e:
            print(f"Error during memory profiling: {e}")

    # Run the test cases within the Flask app context
    with app.app_context():
        test_cases()


if __name__ == "__main__":
    memory_profile_functions()