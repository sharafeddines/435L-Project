import pytest
from unittest.mock import patch
from flask import Flask
from customers_service import create_app

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
    mock_check_db = mocker.patch('utils.database.check_db_connection', return_value=(True, 100))
    response = client.get('/customers/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "healthy"
    assert data['db_connection'] is True
    assert 'uptime' in data

def test_register_customer_success(client, mocker):
    """
    Test successful customer registration.
    """
    data = {
        'username': 'test_user',
        'password': 'password123',
        'full_name': 'Test User'
    }
    response = client.post('/customers/register', json=data)
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Customer registered successfully.'

def test_register_customer_error(client, mocker):
    """
    Test error during customer registration.
    """
    mock_register = mocker.patch('services.customer_service.register_customer', side_effect=ValueError("Username already exists."))
    data = {
        'username': 'test_user',
        'password': 'password123',
        'full_name': 'Test User'
    }
    response = client.post('/customers/register', json=data)
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Username already exists.'

def test_delete_customer_success(client, mocker):
    """
    Test successful deletion of a customer.
    """
    response = client.delete('/customers/test_user')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Customer deleted successfully.'

def test_login(client, mocker):
    """
    Test customer login.
    """
    data = {
        'username': 'test_user',
        'password': 'password123',
        'full_name': 'Test User'
    }
    response = client.post('/customers/register', json=data)
    data = {'username': 'test_user', 'password': 'password123'}
    response = client.post('/customers/login', json=data)
    assert response.status_code == 200

def test_get_user_from_token_api(client, mocker):
    """
    Test retrieving user details from a token.
    """
    data = {
        'username': 'test_user',
        'password': 'password123',
        'full_name': 'Test User'
    }
    response = client.post('/customers/register', json=data)
    data = {'username': 'test_user', 'password': 'password123'}
    response = client.post('/customers/login', json=data)
    assert response.status_code == 200
    token = response.get_json()["access_token"]
    response = client.post('/customers/get_user_from_token', headers={"Authorization":f"Bearer {token}"})
    assert response.status_code == 200
    assert response.get_json()['username'] == 'test_user'

def test_delete_customer_error(client, mocker):
    """
    Test error during customer deletion.
    """
    mock_delete = mocker.patch('services.customer_service.delete_customer', side_effect=ValueError("Customer not found."))
    response = client.delete('/customers/test_user')
    assert response.status_code == 200
    
def test_get_all_customers(client, mocker):
    """
    Test retrieving all customers.
    """
    mock_get_user = mocker.patch('utils.security.get_user_from_token', return_value=['admin'])
    mock_get_all = mocker.patch('services.customer_service.get_all_customers', return_value=[
        {'username': 'user1', 'balance': 100},
        {'username': 'user2', 'balance': 200}
    ])
    response = client.get('/customers/')
    assert response.status_code == 400
    