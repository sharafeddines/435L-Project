from flask import Blueprint, request, jsonify
from services.inventory_service import add_goods, deduct_goods, update_goods, get_all_inventory
from utils.database import check_db_connection
from models.inventory import Inventory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

inventory_bp = Blueprint("inventory", __name__)

limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"], 
    storage_uri="memory://",  
)

@inventory_bp.route('/health')
def health_check():
    """
    Check the health status of the inventory service.

    Returns:
        Response: A JSON object with the service health status,
        database connection status, and uptime.
    """
    results = check_db_connection()
    db_status = results[0]
    elapsed_time = results[1]
    status = {
        "service": "inventory-service",
        "status": "healthy" if db_status else "unhealthy",
        "db_connection": db_status,
        "uptime": elapsed_time
    }
    return jsonify(status), 200 if db_status else 503

@inventory_bp.route("/goods", methods=["POST"])
@limiter.limit("20 per minute")  
def add_goods_route():
    """
    Add new goods to the inventory.

    Request:
        JSON object containing the details of the goods to be added.

    Returns:
        Response: A success message with the added goods' details,
        or an error message on failure.
    """
    try:
        data = request.get_json()
        new_goods = add_goods(data)
        return jsonify({"message": "Goods added successfully", "goods": new_goods.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inventory_bp.route("/goods/<int:item_id>/deduct", methods=["POST"])
@limiter.limit("20 per minute")  
def deduct_goods_route(item_id):
    """
    Deduct a specific quantity of goods from the inventory.

    Args:
        item_id (int): The ID of the inventory item to deduct goods from.

    Request:
        JSON object containing the quantity to deduct (`count`).

    Returns:
        Response: A success message with the updated goods' details,
        or an error message on failure.
    """
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
    """
    Update the details of an inventory item.

    Args:
        item_id (int): The ID of the inventory item to update.

    Request:
        JSON object containing the fields to update.

    Returns:
        Response: A success message with the updated goods' details,
        or an error message on failure.
    """
    try:
        data = request.get_json()
        updated_goods = update_goods(item_id, data)
        return jsonify({"message": "Goods updated successfully", "goods": updated_goods.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inventory_bp.route('/', methods=['GET'])
@limiter.limit("20 per minute")  
def get_all():
    """
    Retrieve all inventory items.

    Returns:
        Response: A JSON list of all inventory items.
    """
    inventories = get_all_inventory()
    return jsonify([inventory.to_dict() for inventory in inventories]), 200
