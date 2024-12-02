import unittest
from flask import Flask
from customers_service import create_app

class TestCustomerService(unittest.TestCase):
    def setUp(self):
        # Configure the test client
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True
        with self.app.app_context():
            # Pre-register an admin user
            admin_data = {
                "full_name": "Admin User",
                "username": "admin",
                "password": "admin",
                "age": 35,
                "address": "Admin Address",
                "gender": "M",
                "marital_status": "Single"
            }
            self.client.post('/customers/register', json=admin_data)

    def test_health_check(self):
        # Test the /health endpoint
        response = self.client.get('/customers/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn("service", response.json)

    def get_token(self, username, password):
        # Helper method to get a token for a user
        login_data = {"username": username, "password": password}
        response = self.client.post('/customers/login', json=login_data)
        self.assertEqual(response.status_code, 200)
        token = response.json.get('access_token')
        self.assertIsNotNone(token)
        return token

    def test_register(self):
        # Test the /register endpoint
        data = {
            "full_name": "TestUser1",
            "username": "testuser2",
            "password": "password",
            "age": 25,
            "address": "beirut",
            "gender": "M",
            "marital_status": "Single"
        }
        response = self.client.post('/customers/register', json=data)
        self.assertEqual(response.status_code, 201)

    def test_get_all_customers(self):
        # Test the /customers endpoint to retrieve all customers
        token = self.get_token("admin", "admin")
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get('/customers/', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_customer_by_username(self):
        # Test retrieving a customer by username
        token = self.get_token("admin", "admin")
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get('/customers/admin', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], "admin")

    def test_charge_deduct_wallet(self):
        # Test charging a customer's wallet
        token = self.get_token("testuser", "password")
        headers = {"Authorization": f"Bearer {token}"}
        data = {"amount": 50}
        response = self.client.post('/customers/charge', json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("new_balance", response.json)

        data2 = {"amount": 10}
        response2 = self.client.post('/customers/deduct', json=data2, headers=headers)
        self.assertEqual(response2.status_code, 200)
        self.assertIn("wallet_balance", response2.json)


    def test_update_customer(self):
        # Test updating a customer's details
        token = self.get_token("admin", "admin")
        headers = {"Authorization": f"Bearer {token}"}
        data = {"age": 40, "address": "New Address"}
        response = self.client.put('/customers/admin', json=data, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_authenticate_customer(self):
        # Test authenticating a customer
        login_data = {
            "username": "admin",
            "password": "admin"
        }
        response = self.client.post('/customers/login', json=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json)

    def test_delete(self):
        # Test deleting a customer
        token = self.get_token("admin", "admin")
        headers = {"Authorization": f"Bearer {token}"}
        delete_response = self.client.delete('/customers/admin', headers=headers)
        self.assertEqual(delete_response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
