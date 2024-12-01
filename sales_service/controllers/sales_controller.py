from flask import Blueprint, request, jsonify
import requests
from services.sales_service import add_sale
from models.sales import Sales
import pybreaker
from utils.database import check_db_connection

sales_bp = Blueprint("sales", __name__)

url_customer = "http://192.168.1.3:5000/customers/deduct"
url_inventory = "http://192.168.1.4:5000/inventory/"

customers_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=6)
inventory_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=6)

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"], 
    storage_uri="memory://",  
)

@sales_bp.route('/health')
def health_check():
    """
    Check the health of the sales service.

    :return: JSON response indicating service health and database connection status.
    :rtype: tuple
    """
    results = check_db_connection()
    db_status = results[0]
    elapsed_time = results[1]
    status = {
        "service": "sales-service",
        "status": "healthy" if db_status else "unhealthy",
        "db_connection": db_status,
        "uptime": elapsed_time
    }
    return jsonify(status), 200 if db_status else 503

@sales_bp.route("/display_available_goods", methods=["GET"])
@limiter.limit("25 per minute") 
def get_available_goods():
    """
    Fetch a list of available goods in the inventory.

    :return: JSON response with a list of available goods or an error message.
    :rtype: tuple
    """
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
@limiter.limit("20 per minute") 
def get_details_of_item(item_name):
    """
    Fetch details for a specific item.

    :param item_name: The name of the item.
    :type item_name: str
    :return: JSON response with item details or an error message.
    :rtype: tuple
    """
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
@limiter.limit("5 per minute") 
def make_sale():
    """
    Process a sale by deducting inventory and charging the customer.

    :return: JSON response with sale details or an error message.
    :rtype: tuple
    """
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
                "http://192.168.1.3:5000/customers/get_user_from_token",
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
@limiter.limit("20 per minute") 
def get_all_sales():
    """
    Fetch all sales records.

    :return: JSON response with all sales data or an error message.
    :rtype: tuple
    """
    try:
        all_sales = Sales.query.all()  # Fetches all sales records from the database
        sales_data = [sale.to_dict() for sale in all_sales]  # Convert to dictionary
        return jsonify({'status': 'success', 'data': sales_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@sales_bp.route('/sales/customer/<int:customer_id>', methods=['GET'])
@limiter.limit("15 per minute") 
def get_sales_by_customer(customer_id):
    """
    Fetch all sales records for a specific customer.

    :param customer_id: The ID of the customer.
    :type customer_id: int
    :return: JSON response with sales data for the customer or an error message.
    :rtype: tuple
    """
    try:
        customer_sales = Sales.query.filter_by(customer_id=customer_id).all()  # Fetch sales for a specific customer
        sales_data = [sale.to_dict() for sale in customer_sales]  # Convert to dictionary
        return jsonify({'status': 'success', 'data': sales_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
