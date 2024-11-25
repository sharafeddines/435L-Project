from flask import Blueprint, request, jsonify
from services.inventory_service import add_goods, deduct_goods, update_goods
from models.inventory import Goods

inventory_bp = Blueprint("inventory", __name__)

@inventory_bp.route("/goods", methods=["POST"])
def add_goods_route():
    try:
        data = request.get_json()
        new_goods = add_goods(data)
        return jsonify({"message": "Goods added successfully", "goods": new_goods.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inventory_bp.route("/goods/<int:item_id>/deduct", methods=["POST"])
def deduct_goods_route(item_id):
    try:
        data = request.get_json()
        count = data.get("count", 1)
        updated_goods = deduct_goods(item_id, count)
        return jsonify({"message": "Goods deducted successfully", "goods": updated_goods.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inventory_bp.route("/goods/<int:item_id>", methods=["PUT"])
def update_goods_route(item_id):
    try:
        data = request.get_json()
        updated_goods = update_goods(item_id, data)
        return jsonify({"message": "Goods updated successfully", "goods": updated_goods.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
