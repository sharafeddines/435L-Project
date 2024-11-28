from flask import Blueprint, request, jsonify
import requests
from services.sales_service import add_sale
from models.sales import Sales

sales_bp = Blueprint("sales", __name__)

url_customer = "http://172.17.0.3:5000/customers/deduct"
url_inventory = "http://172.17.0.4:5000/inventory/"


@sales_bp.route("/display_available_goods", methods=["GET"])
def get_available_goods():
    try:
        response = requests.get(url_inventory)
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
        response = requests.get(url_inventory)
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

@sales_bp.route("/make_sale/<string:item_name>", methods=["POST"])
def make_sale(item_name):
    try:
        response_get_item = requests.get(url_inventory)
        if response_get_item.status_code == 200:
            data = response_get_item.json()  # Parse the JSON response
            item = next((item for item in data if item.get('name') == item_name), None)
            if (item == None):
                raise ValueError("Item not found")
            if item["count_in_stock"]<0:
                raise ValueError("Item out of stock")
        else:
            raise ValueError("An error has occured")
        print(item)
        url_deduct = url_inventory+"goods/"+str(item["id"])+"/deduct"
        print(url_deduct)
        response_deduct_quantity = requests.post(url_deduct, json={"count":1})
        if(response_deduct_quantity.status_code != 200):
            raise ValueError("Unable to deduct items from inventory")

        response = requests.post(url_customer, headers=request.headers, 
                                 json={
                                    "amount":item["price_per_item"]    
                                 }
                                 )
        print("response.json()")
        if response.status_code != 200:
            response_update_quantity = requests.put(url_inventory+f'/goods/{item["id"]}', json={"count_in_stock":item["count_in_stock"]})
            raise ValueError("Item not found")
        response_get_customer = requests.post('http://172.17.0.3:5000/customers/get_user_from_token', headers=request.headers)
        if response_get_customer.status_code != 200:
            raise ValueError("Item not found")
        customer = response_get_customer.json()
        print(customer)
        print(item["id"])
        data = {
            "customer_id":customer["id"],
            "product_id":item['id'],
            "quantity":1
        }
        sale = add_sale(data)
        return jsonify(sale.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
