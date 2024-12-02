import unittest
from flask import Flask
from customers_service import create_app

class TestCustomerService(unittest.TestCase):
    def setUp(self):
        # Configure the test client
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_health_check(self):
        # Test the /health endpoint
        response = self.client.get('/customers/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn("service", response.json)

    def test_register(self):
        # Test the /register endpoint
        data = {
            "full_name": "Test User",
            "username": "testuser",
            "password": "password",
            "age": 25,
            "address": "beirut",
            "gender": "M",
            "marital_status": "Single"
        }
        response = self.client.post('/customers/register', json=data)
        self.assertEqual(response.status_code, 201)

    def test_delete(self):

        login_data = {
            "username": "testuser",
            "password": "password"
        }
        login_response = self.client.post('/customers/login', json=login_data)
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json.get('access_token')
        self.assertIsNotNone(token)

        headers = {
            "Authorization": f"Bearer {token}"
        }
        delete_response = self.client.delete('/customers/testuser', headers=headers)
        self.assertEqual(delete_response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
