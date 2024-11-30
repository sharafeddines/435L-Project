from flask import Blueprint, request, jsonify
import requests
from services.sales_service import add_sale
from models.sales import Sales
import pybreaker

sales_bp = Blueprint("sales", __name__)

url_customer = "http://172.17.0.3:5000/customers/deduct"
url_inventory = "http://172.17.0.4:5000/inventory/"

customers_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=6)
inventory_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=6)

@sales_bp.route("/display_available_goods", methods=["GET"])
def get_available_goods():
    try:
        try:
            response = inventory_breaker.call(requests.get, url_inventory)
            if response.status_code != 200:
                raise ValueError("Failed to fetch inventory data")
        except pybreaker.CircuitBreakerError:
            raise ValueError("Inventory service unavailable")
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            available_goods = [{"name":item["name"], "price_per_item":item["price_per_item"]} for item in data if item.get('count_in_stock', 0) != 0]
            return jsonify(available_goods), 200
        else:
            raise TypeError("Error")
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@sales_bp.route("/get_details/<string:item_name>", methods=["GET"])
def get_details_of_item(item_name):
    try:
        try:
            response = inventory_breaker.call(requests.get, url_inventory)
            if response.status_code != 200:
                raise ValueError("Failed to fetch inventory data")
        except pybreaker.CircuitBreakerError:
            raise ValueError("Inventory service unavailable")
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            item = next((item for item in data if item.get('name') == item_name), None)
            if (item == None):
                raise ValueError("Item not found")
            del item["id"]
            return jsonify(item), 200
        else:
            raise ValueError("Item not found")
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@sales_bp.route('/make_sale', methods=['POST'])
def make_sale():
    try:
        data = request.get_json()
        item_name = data.get("item_name")
        quantity = data.get("quantity")
        try:
            response_get_item = inventory_breaker.call(requests.get, url_inventory)
            if response_get_item.status_code != 200:
                raise ValueError("Failed to fetch inventory data")
        except pybreaker.CircuitBreakerError:
            raise ValueError("Inventory service unavailable")
        if response_get_item.status_code == 200:
            data = response_get_item.json()  # Parse the JSON response
            item = next((item for item in data if item.get('name') == item_name), None)
            print(item)
            if (item == None):
                raise ValueError("Item not found")
            if item["count_in_stock"]<0 or item["count_in_stock"]<quantity:
                raise ValueError(f"Item out of stock or there is not this much of product {item_name}")
        else:
            raise ValueError("An error has occured")
        print(item)
        url_deduct = url_inventory+"goods/"+str(item["id"])+"/deduct"
        print(url_deduct)
        try:
            response_deduct_quantity = inventory_breaker.call(
                requests.post, url_deduct, json={"count": quantity}
            )
            if response_deduct_quantity.status_code != 200:
                raise ValueError("Unable to deduct items from inventory")
        except pybreaker.CircuitBreakerError:
            raise ValueError("Inventory service unavailable for deduction")
        if(response_deduct_quantity.status_code != 200):
            raise ValueError("Unable to deduct items from inventory")

        try:
            response_deduct_payment = customers_breaker.call(
                requests.post,
                url_customer,
                headers=request.headers,
                json={"amount": item["price_per_item"] * quantity},
            )
            if response_deduct_payment.status_code != 200:
                # Rollback inventory if payment deduction fails
                inventory_breaker.call(
                    requests.put,
                    f"{url_inventory}goods/{item['id']}",
                    json={"count_in_stock": item["count_in_stock"]},
                )
                raise ValueError("Failed to deduct payment from customer")
        except pybreaker.CircuitBreakerError:
            raise ValueError("Customers service unavailable for payment deduction")

        try:
            response_get_customer = customers_breaker.call(
                requests.post,
                "http://172.17.0.3:5000/customers/get_user_from_token",
                headers=request.headers,
            )
            if response_get_customer.status_code != 200:
                raise ValueError("Failed to fetch customer data")
        except pybreaker.CircuitBreakerError:
            raise ValueError("Customers service unavailable")

        if response_get_customer.status_code != 200:
            raise ValueError("Item not found")
        customer = response_get_customer.json()
        print(customer)
        print(item["id"])
        data = {
            "customer_id":customer["id"],
            "product_id":item['id'],
            "quantity":quantity
        }
        sale = add_sale(data)
        return jsonify(sale.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@sales_bp.route('/sales', methods=['GET'])
def get_all_sales():
    try:
        all_sales = Sales.query.all()  # Fetches all sales records from the database
        sales_data = [sale.to_dict() for sale in all_sales]  # Convert to dictionary
        return jsonify({'status': 'success', 'data': sales_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@sales_bp.route('/sales/customer/<int:customer_id>', methods=['GET'])
def get_sales_by_customer(customer_id):
    try:
        customer_sales = Sales.query.filter_by(customer_id=customer_id).all()  # Fetch sales for a specific customer
        sales_data = [sale.to_dict() for sale in customer_sales]  # Convert to dictionary
        return jsonify({'status': 'success', 'data': sales_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
