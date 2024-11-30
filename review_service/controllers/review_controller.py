from flask import Blueprint, request, jsonify
from services.review_service import add_review, update_review, get_all_reviews_by_product, delete_review, get_all_reviews_by_customer, get_specific_review_details, flag_review, delete_review_admin
import requests
from models.review import Review
import pybreaker
from utils.database import check_db_connection

# Define circuit breakers
inventory_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=6)
customers_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=6)
sales_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=6)


review_bp = Blueprint("review", __name__)

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"], 
    storage_uri="memory://",  
)

@review_bp.route('/health')
def health_check():
    results = check_db_connection()
    db_status = results[0]
    elapsed_time = results[1]
    status = {
        "service": "review-service",
        "status": "healthy" if db_status else "unhealthy",
        "db_connection": db_status,
        "uptime": elapsed_time
    }
    return jsonify(status), 200 if db_status else 503

@review_bp.route("/add", methods=["POST"])
@limiter.limit("5 per minute") 
def add_review_route():
    url_inventory = "http://172.17.0.4:5000/inventory/"
    url_customers = "http://172.17.0.3:5000/customers/get_user_from_token"
    try:
        data = request.get_json()
        try:
            data_items_request = inventory_breaker.call(requests.get, url_inventory)
            if data_items_request.status_code != 200:
                raise ValueError("Failed to fetch inventory data")
            data_items = data_items_request.json()
        except pybreaker.CircuitBreakerError:
            raise ValueError("Inventory service unavailable")
        try:
            data_customer_request = customers_breaker.call(requests.post, url_customers, headers=request.headers)
            if data_customer_request.status_code != 200:
                raise ValueError("Failed to fetch customer data")
            data_customer = data_customer_request.json()
        except pybreaker.CircuitBreakerError:
            raise ValueError("Customers service unavailable")
        if data_items_request.status_code == 200 and data_customer_request.status_code==200:
            data_items = data_items_request.json()
            item = next((item for item in data_items if item.get('name') == data["product_name"]), None)
            if item ==None:
                raise ValueError("No such item to review")
            data_customer = data_customer_request.json()
            user_id = data_customer["id"] 
            url_sales = f"http://172.17.0.5:5000/sales/sales/customer/{user_id}"
            try:
                data_sales_request = sales_breaker.call(requests.get, url_sales)
                if data_sales_request.status_code != 200:
                    raise ValueError("Failed to fetch sales data")
                data_sales = data_sales_request.json()["data"]
            except pybreaker.CircuitBreakerError:
                raise ValueError("Sales service unavailable")
            if data_sales_request.status_code == 200:
                data_sales = data_sales_request.json()["data"]
                print(data_sales)
                item_bought =  next((item2 for item2 in data_sales if item2.get('product_id') == item["id"]), None)
                if not item_bought:
                    raise ValueError("User hasnt bought this product.")

                new_review = add_review(user_id, item["id"], data)
                return jsonify({"message": "Review added successfully", "review": new_review.to_dict()}), 201
            else:
                return jsonify({"error": "Request failed"}), 400
        else:
            return jsonify({"error": "Request failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@review_bp.route("/update", methods=["PUT"])
@limiter.limit("5 per minute") 
def update_review_route():
    url_inventory = "http://172.17.0.4:5000/inventory/"
    url_customers = "http://172.17.0.3:5000/customers/get_user_from_token"
    try:
        data = request.get_json()
        data_items_request = requests.get(url_inventory)
        data_customer_request = requests.post(url_customers, headers = request.headers)
        if data_items_request.status_code == 200 and data_customer_request.status_code==200:
            data_items = data_items_request.json()
            item = next((item for item in data_items if item.get('name') == data["product_name"]), None)
            if item == None:
                raise ValueError("No such item exists.")
            data_customer = data_customer_request.json()
            user_id = data_customer["id"] 
            print(user_id)
            print(item)

            updated_review = update_review(user_id, item["id"], data)
            return jsonify({"message": "Review updated successfully", "review": updated_review.to_dict()}), 201
        else:
            return jsonify({"error": "Request failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@review_bp.route("/delete", methods=["DELETE"])
@limiter.limit("5 per minute") 
def delete_review_route():
    url_inventory = "http://172.17.0.4:5000/inventory/"
    url_customers = "http://172.17.0.3:5000/customers/get_user_from_token"
    try:
        data = request.get_json()
        try:
            data_items_request = inventory_breaker.call(requests.get, url_inventory)
            if data_items_request.status_code != 200:
                raise ValueError("Failed to fetch inventory data")
            data_items = data_items_request.json()
        except pybreaker.CircuitBreakerError:
            raise ValueError("Inventory service unavailable")
        try:
            data_customer_request = customers_breaker.call(requests.post, url_customers, headers=request.headers)
            if data_customer_request.status_code != 200:
                raise ValueError("Failed to fetch customer data")
            data_customer = data_customer_request.json()
        except pybreaker.CircuitBreakerError:
            raise ValueError("Customers service unavailable")
        if data_items_request.status_code == 200 and data_customer_request.status_code==200:
            data_items = data_items_request.json()
            item = next((item for item in data_items if item.get('name') == data["product_name"]), None)
            if item == None:
                raise ValueError("No such item exists.")
            data_customer = data_customer_request.json()
            user_id = data_customer["id"] 

            delete_review(user_id, item["id"])
            return jsonify({"message": "Review deleted successfully"}), 201
        else:
            return jsonify({"error": "Request failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@review_bp.route('/get/all_by_customer', methods=['GET'])
@limiter.limit("10 per minute") 
def get_all_by_customer():
    url_customers = "http://172.17.0.3:5000/customers/get_user_from_token"
    try:
        try:
            data_customer_request = customers_breaker.call(requests.post, url_customers, headers=request.headers)
            if data_customer_request.status_code != 200:
                raise ValueError("Failed to fetch customer data")
            data_customer = data_customer_request.json()
        except pybreaker.CircuitBreakerError:
            raise ValueError("Customers service unavailable")
        if data_customer_request.status_code==200:
            data_customer = data_customer_request.json()
            user_id = data_customer["id"]
            
            reviews_for_customer = get_all_reviews_by_customer(user_id)
            return jsonify([review.to_dict() for review in reviews_for_customer]), 200
        else:
            return jsonify({"error": "Request failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@review_bp.route('/get/all_by_product', methods=['GET'])
@limiter.limit("10 per minute") 
def get_all_by_product():
    url_inventory = "http://172.17.0.4:5000/inventory/"
    try:
        data = request.get_json()
        try:
            data_items_request = inventory_breaker.call(requests.get, url_inventory)
            if data_items_request.status_code != 200:
                raise ValueError("Failed to fetch inventory data")
            data_items = data_items_request.json()
        except pybreaker.CircuitBreakerError:
            raise ValueError("Inventory service unavailable")
        if data_items_request.status_code==200:
            data_items = data_items_request.json()
            item = next((item for item in data_items if item.get('name') == data["product_name"]), None)
            if item == None:
                raise ValueError("No such product exists.")
            reviews_for_product = get_all_reviews_by_product(item["id"])
            return jsonify([review.to_dict() for review in reviews_for_product]), 200
        else:
            return jsonify({"error": "Request failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@review_bp.route("/get/specific", methods=["GET"])
@limiter.limit("10 per minute") 
def get_specific_review():
    url_inventory = "http://172.17.0.4:5000/inventory/"
    url_customers = "http://172.17.0.3:5000/customers/"
    try:
        data = request.get_json()
        if not data:
            raise ValueError("Invalid input.") 
        print(data["review_id"])
        review = Review.query.filter_by(id = data["review_id"]).first()
        if not review:
            raise ValueError("No such review exists.")
        try:
            data_items_request = inventory_breaker.call(requests.get, url_inventory)
            if data_items_request.status_code != 200:
                raise ValueError("Failed to fetch inventory data")
            data_items = data_items_request.json()
        except pybreaker.CircuitBreakerError:
            raise ValueError("Inventory service unavailable")
        try:
            data_customer_request = customers_breaker.call(requests.get, url_customers)
            if data_customer_request.status_code != 200:
                raise ValueError("Failed to fetch customer data")
            data_customer = data_customer_request.json()
        except pybreaker.CircuitBreakerError:
            raise ValueError("Customers service unavailable")
        if data_items_request.status_code == 200 and data_customer_request.status_code==200:
            data_items = data_items_request.json()
            item = next((item for item in data_items if item.get('id') == review.product_id), None)
            
            data_customer = data_customer_request.json()
            customer = next((cust for cust in data_customer if cust.get('id') == review.customer_id), None)

            specific_details = get_specific_review_details(review, item, customer)
            return jsonify(specific_details), 200
        else:
            return jsonify({"error": "Request failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@review_bp.route("/flag", methods=["POST"])
@limiter.limit("10 per minute") 
def flag_review_route():
    url_customers = "http://172.17.0.3:5000/customers/get_user_from_token"
    try:
        data = request.get_json()
        try:
            data_customer_request = customers_breaker.call(requests.post, url_customers, headers=request.headers)
            if data_customer_request.status_code != 200:
                raise ValueError("Failed to fetch customer data")
            data_customer = data_customer_request.json()
        except pybreaker.CircuitBreakerError:
            raise ValueError("Customers service unavailable")
        if data_customer_request.status_code==200:
            data_customer = data_customer_request.json()
            user_id = data_customer["id"]
            is_admin = data_customer["is_admin"]
            if not is_admin:
                raise ValueError("Action not allowed")
            review = flag_review(data["review_id"])

            return jsonify({"message": "Review flagged successfully", "review": review.to_dict()}), 201

        else:
            return jsonify({"error": "Request failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@review_bp.route("/delete_admin", methods=["DELETE"])
@limiter.limit("10 per minute") 
def delete_review_admin_route():
    url_customers = "http://172.17.0.3:5000/customers/get_user_from_token"
    try:
        data = request.get_json()
        try:
            data_customer_request = customers_breaker.call(requests.post, url_customers, headers=request.headers)
            if data_customer_request.status_code != 200:
                raise ValueError("Failed to fetch customer data")
            data_customer = data_customer_request.json()
        except pybreaker.CircuitBreakerError:
            raise ValueError("Customers service unavailable")
        if data_customer_request.status_code==200:
            data_customer = data_customer_request.json()
            user_id = data_customer["id"]
            is_admin = data_customer["is_admin"]
            if not is_admin:
                raise ValueError("Action not allowed")
            review = delete_review_admin(data["review_id"])

            return jsonify({"message": "Review deleted successfully"}), 201

        else:
            return jsonify({"error": "Request failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

