import pytest
from flask import Flask
from models.sales import Sales
from controllers.sales_controller import sales_bp

# Fixtures
@pytest.fixture
def client():
    """
    Fixture to set up a test client for the Flask application.
    """
    app = Flask(__name__)
    app.testing = True
    app.register_blueprint(sales_bp, url_prefix="/sales")
    with app.test_client() as client:
        yield client

# Health Check
def test_health_check(client, mocker):
    """
    Test the health check endpoint.
    """
    mock_check_db = mocker.patch('utils.database.check_db_connection', return_value=(True, 100))
    response = client.get('/sales/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "healthy"
    assert data['db_connection'] is True

# Get Available Goods
def test_display_available_goods(client, mocker):
    """
    Test fetching available goods.
    """
    mock_inventory = mocker.patch(
        'requests.get',
        return_value=mocker.Mock(status_code=200, json=lambda: [
            {'name': 'Product1', 'price_per_item': 10, 'count_in_stock': 5},
            {'name': 'Product2', 'price_per_item': 15, 'count_in_stock': 0}
        ])
    )
    response = client.get('/sales/display_available_goods')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['name'] == 'Product1'

# Get Item Details
def test_get_details_of_item(client, mocker):
    """
    Test fetching details of a specific item.
    """
    mock_inventory = mocker.patch(
        'requests.get',
        return_value=mocker.Mock(status_code=200, json=lambda: [
            {'name': 'Product1', 'price_per_item': 10, 'count_in_stock': 5}
        ])
    )
    response = client.get('/sales/get_details/Product1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Product1'
    assert data['price_per_item'] == 10

# Make Sale
def test_make_sale_success(client, mocker):
    """
    Test making a sale successfully.
    """
    mock_inventory = mocker.patch(
        'requests.get',
        return_value=mocker.Mock(status_code=200, json=lambda: [
            {'id': 1, 'name': 'Product1', 'price_per_item': 10, 'count_in_stock': 5}
        ])
    )
    mock_inventory_deduct = mocker.patch(
        'requests.post',
        side_effect=lambda url, json=None: (
            mocker.Mock(status_code=200) if "deduct" in url else mocker.Mock(status_code=400)
        )
    )
    mock_customer_deduct = mocker.patch(
        'requests.post',
        return_value=mocker.Mock(status_code=200)
    )
    mock_add_sale = mocker.patch(
        'services.sales_service.add_sale',
        return_value=Sales(customer_id=1, product_id=1, quantity=2)
    )

    data = {"item_name": "Product1", "quantity": 2}
    response = client.post('/sales/make_sale', json=data)
    assert response.status_code == 200
    sale = response.get_json()
    assert sale['quantity'] == 2

# Get All Sales
def test_get_all_sales(client, mocker):
    """
    Test fetching all sales.
    """
    mock_sales = [
        Sales(customer_id=1, product_id=1, quantity=5),
        Sales(customer_id=2, product_id=2, quantity=3)
    ]
    mocker.patch('models.sales.Sales.query.all', return_value=mock_sales)

    response = client.get('/sales/sales')
    assert response.status_code == 200
    data = response.get_json()['data']
    assert len(data) == 2
    assert data[0]['quantity'] == 5

# Get Sales by Customer
def test_get_sales_by_customer(client, mocker):
    """
    Test fetching sales by a specific customer.
    """
    mock_sales = [
        Sales(customer_id=1, product_id=1, quantity=5),
        Sales(customer_id=1, product_id=2, quantity=2)
    ]
    mocker.patch('models.sales.Sales.query.filter_by', return_value=mocker.Mock(all=lambda: mock_sales))

    response = client.get('/sales/sales/customer/1')
    assert response.status_code == 200
    data = response.get_json()['data']
    assert len(data) == 2
    assert data[0]['quantity'] == 5
