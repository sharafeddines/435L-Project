import pytest
from unittest.mock import patch
from flask import Flask
from inventory_service import create_app


@pytest.fixture
def client():
    """
    Fixture to set up a test client for the Flask application.
    """
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client, mocker):
    """
    Test the health check endpoint.
    """
    response = client.get('/inventory/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['service'] == "inventory-service"
    assert data['status'] == "healthy"
    assert data['db_connection'] is True
    assert 'uptime' in data


def test_add_goods_success(client, mocker):
    """
    Test successfully adding goods to the inventory.
    """
    data = {
        "name": "Test Item",
        "category": "Electronics",
        "price_per_item": 100.0,
        "count_in_stock": 50,
        "description": "Test Description"
    }
    response = client.post('/inventory/goods', json=data)
    assert response.status_code == 201
    assert response.get_json()['message'] == "Goods added successfully"


def test_add_goods_error(client, mocker):
    """
    Test error when adding duplicate goods to the inventory.
    """
    data = {
        "name": "Duplicate Item",
        "category": "Electronics",
        "price_per_item": 100.0,
        "count_in_stock": 50
    }
    response = client.post('/inventory/goods', json=data)
    data = {
        "name": "Duplicate Item",
        "category": "Electronics",
        "price_per_item": 100.0,
        "count_in_stock": 50
    }
    response = client.post('/inventory/goods', json=data)
    assert response.status_code == 400
    assert response.get_json()['error'] == "Item already exists."


def test_deduct_goods_success(client, mocker):
    """
    Test successfully deducting goods from the inventory.
    """
    data = {"count": 5}
    response = client.post('/inventory/goods/1/deduct', json=data)
    assert response.status_code == 200
    assert response.get_json()['message'] == "Goods deducted successfully"
    assert response.get_json()['goods']['count_in_stock'] == 45


def test_deduct_goods_insufficient_stock(client, mocker):
    """
    Test error when trying to deduct more goods than available in stock.
    """
    data = {"count": 50}
    response = client.post('/inventory/goods/1/deduct', json=data)
    assert response.status_code == 400
    assert response.get_json()['error'] == "Insufficient stock"


def test_update_goods_success(client, mocker):
    """
    Test successfully updating an inventory item.
    """
    data = {"price_per_item": 150.0, "count_in_stock": 30}
    response = client.put('/inventory/goods/1', json=data)
    assert response.status_code == 200
    assert response.get_json()['message'] == "Goods updated successfully"


def test_update_goods_not_found(client, mocker):
    """
    Test error when trying to update a non-existent inventory item.
    """
    data = {"price_per_item": 150.0, "count_in_stock": 30}
    response = client.put('/inventory/goods/999', json=data)
    assert response.status_code == 400
    assert response.get_json()['error'] == "Item not found"


def test_get_all_inventory(client, mocker):
    """
    Test retrieving all inventory items.
    """
    response = client.get('/inventory/')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['name'] == "Test Item"
    assert data[1]['count_in_stock'] == 50
