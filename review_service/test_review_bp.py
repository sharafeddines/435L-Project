import pytest
from unittest.mock import patch
from flask import Flask
from review_service import create_app

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
    response = client.get('/review/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "healthy"
    assert data['db_connection'] is True
    assert 'uptime' in data

def test_add_review_success(client, mocker):
    """
    Test successful addition of a review.
    """
    data = {
        'product_name': 'Test Product',
        'rating': 5,
        'description': 'Great product!'
    }
    response = client.post('/review/add', json=data)
    assert response.status_code == 201
    assert response.get_json()['message'] == "Review added successfully"

def test_update_review_success(client, mocker):
    """
    Test successful update of a review.
    """

    data = {
        'product_name': 'Test Product',
        'rating': 4,
        'description': 'Updated review'
    }
    response = client.put('/review/update', json=data)
    assert response.status_code == 201
    assert response.get_json()['message'] == "Review updated successfully"

def test_delete_review_success(client, mocker):
    """
    Test successful deletion of a review.
    """
    data = {'product_name': 'Test Product'}
    response = client.delete('/review/delete', json=data)
    assert response.status_code == 201
    assert response.get_json()['message'] == "Review deleted successfully"

def test_get_all_reviews_by_customer(client, mocker):
    """
    Test retrieving all reviews by a customer.
    """
    response = client.get('/review/get/all_by_customer')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['rating'] == 5

def test_get_all_reviews_by_product(client, mocker):
    """
    Test retrieving all reviews for a product.
    """
    data = {'product_name': 'Test Product'}
    response = client.get('/review/get/all_by_product', json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['rating'] == 5

def test_flag_review(client, mocker):
    """
    Test flagging a review.
    """
    data = {'review_id': 1}
    response = client.post('/review/flag', json=data)
    assert response.status_code == 201
    assert response.get_json()['message'] == "Review flagged successfully"

def test_delete_review_admin(client, mocker):
    """
    Test admin deletion of a review.
    """
    data = {'review_id': 1}
    response = client.delete('/review/delete_admin', json=data)
    assert response.status_code == 201
    assert response.get_json()['message'] == "Review deleted successfully"
