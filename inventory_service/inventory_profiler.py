import time
from line_profiler import LineProfiler
from services.inventory_service import (
    add_goods, deduct_goods, update_goods, get_all_inventory
)


def profile_functions(app):
    profiler = LineProfiler()
    # Add all functions to be profiled
    profiler.add_function(add_goods)
    profiler.add_function(deduct_goods)
    profiler.add_function(update_goods)
    profiler.add_function(get_all_inventory)

    def test_cases():
        # Simulated test data
        try:
            # Add goods to inventory
            new_item = {
                "name": "Laptop2",
                "category": "Electronics",
                "price_per_item": 1500.0,
                "description": "A high-performance laptop",
                "count_in_stock": 10
            }
            added_item = add_goods(new_item)
            print(f"Added item: {added_item.name}")

            # Deduct goods from inventory
            item_id = added_item.id
            deduct_goods(item_id, 2)
            print(f"Deducted 2 units from item ID {item_id}")

            # Update goods details
            update_data = {"price_per_item": 1400.0, "description": "Discounted laptop"}
            updated_item = update_goods(item_id, update_data)
            print(f"Updated item: {updated_item.name}, New price: {updated_item.price_per_item}")

            # Retrieve all inventory items
            inventory = get_all_inventory()
            print(f"Total inventory items: {len(inventory)}")

        except Exception as e:
            print(f"Error during profiling: {e}")

    # Run the profiler with Flask app context
    with app.app_context():
        profiler.runcall(test_cases)
        profiler.print_stats()


if __name__ == "__main__":
    profile_functions()
