import unittest
from flask import Flask
from sales_service import create_app

class TestSalesService(unittest.TestCase):
    def setUp(self):
        # Configure the test client
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_health_check(self):
        # Test the /health endpoint
        response = self.client.get('/sales/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn("service", response.json)

    def test_display_available_goods(self):
        # Test the /display_available_goods endpoint
        response = self.client.get('/sales/display_available_goods')
        self.assertIn(response.status_code, [200, 400])  # Expect valid response or error
        if response.status_code == 200:
            self.assertTrue(isinstance(response.json, list))

    def test_get_details_of_item(self):
        # Test the /get_details/<item_name> endpoint
        response = self.client.get('/sales/get_details/TestItem')
        self.assertIn(response.status_code, [200, 400])
        if response.status_code == 200:
            self.assertIn("name", response.json)
            self.assertIn("price_per_item", response.json)

    def test_make_sale(self):
        # Test the /make_sale endpoint
        data = {
            "item_name": "TestItem",
            "quantity": 1
        }
        headers = {
            "Authorization": "Bearer test_token"  # Replace with a valid token if needed
        }
        response = self.client.post('/sales/make_sale', json=data, headers=headers)
        self.assertIn(response.status_code, [200, 400])  # Expect success or error
        if response.status_code == 200:
            self.assertIn("customer_id", response.json)
            self.assertIn("product_id", response.json)
            self.assertIn("quantity", response.json)

    def test_get_all_sales(self):
        # Test the /sales endpoint
        response = self.client.get('/sales/sales')
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json)
        self.assertIn("data", response.json)

    def test_get_sales_by_customer(self):
        # Test the /sales/customer/<customer_id> endpoint
        response = self.client.get('/sales/customer/0')  # Replace with a valid customer ID
        self.assertIn(response.status_code, [200, 400, 404])
        if response.status_code == 200:
            self.assertIn("status", response.json)
            self.assertIn("data", response.json)

    def test_invalid_item_name(self):
        # Test invalid item name for /get_details/<item_name>
        response = self.client.get('/sales/get_details/InvalidItemName')
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_make_sale_out_of_stock(self):
        # Test the /make_sale endpoint with out-of-stock item
        data = {
            "item_name": "OutOfStockItem",
            "quantity": 10  # Exceed available quantity
        }
        headers = {
            "Authorization": "Bearer test_token"  # Replace with a valid token if needed
        }
        response = self.client.post('/sales/make_sale', json=data, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

if __name__ == "__main__":
    unittest.main()
