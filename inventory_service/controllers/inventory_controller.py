from flask import Blueprint, request, jsonify
from services.inventory_service import add_goods, deduct_goods, update_goods, get_all_inventory
from models.inventory import Inventory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
inventory_bp = Blueprint("inventory", __name__)

limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"], 
    storage_uri="memory://",  
)

@inventory_bp.route("/goods", methods=["POST"])
@limiter.limit("20 per minute")  
def add_goods_route():
    try:
        data = request.get_json()
        new_goods = add_goods(data)
        return jsonify({"message": "Goods added successfully", "goods": new_goods.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inventory_bp.route("/goods/<int:item_id>/deduct", methods=["POST"])
@limiter.limit("20 per minute")  
def deduct_goods_route(item_id):
    try:
        data = request.get_json()
        count = data.get("count", 1)
        updated_goods = deduct_goods(item_id, count)
        return jsonify({"message": "Goods deducted successfully", "goods": updated_goods.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inventory_bp.route("/goods/<int:item_id>", methods=["PUT"])
@limiter.limit("10 per minute")  
def update_goods_route(item_id):
    try:
        data = request.get_json()
        updated_goods = update_goods(item_id, data)
        return jsonify({"message": "Goods updated successfully", "goods": updated_goods.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inventory_bp.route('/', methods=['GET'])
@limiter.limit("20 per minute")  
def get_all():
    inventories = get_all_inventory()
    return jsonify([inventory.to_dict() for inventory in inventories]), 200
