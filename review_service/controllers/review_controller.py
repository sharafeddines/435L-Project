from flask import Blueprint, request, jsonify
from services.review_service import add_review, update_review, get_all_reviews
import requests
from models.review import Review

review_bp = Blueprint("review", __name__)

@review_bp.route("/add", methods=["POST"])
def add_review_route():
    url_inventory = "http://172.17.0.4:5000/inventory/"
    url_customers = "http://172.17.0.3:5000/customers/get_user_from_token"
    try:
        data = request.get_json()
        data_items_request = requests.get(url_inventory)
        data_customer_request = requests.post(url_customers, headers = request.headers)
        if data_items_request.status_code == 200 and data_customer_request.status_code==200:
            data_items = data_items_request.json()
            item = next((item for item in data_items if item.get('name') == data["product_name"]), None)
            data_customer = data_customer_request.json() #validate it returned something correctly
            user_id = data_customer["id"] 

            new_review = add_review(user_id, item["id"], data)
            return jsonify({"message": "Review added successfully", "review": new_review.to_dict()}), 201
        else:
            return jsonify({"error": "Request failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@review_bp.route("/update", methods=["PUT"])
def update_review_route():
    pass


@review_bp.route('/', methods=['GET'])
def get_all():
    pass
