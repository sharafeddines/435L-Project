import unittest
from flask import Flask
from review_service import create_app

class TestReviewService(unittest.TestCase):
    def setUp(self):
        # Configure the test client
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_health_check(self):
        # Test the /health endpoint
        response = self.client.get('/review/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn("service", response.json)

    def test_add_review(self):
        # Test the /add endpoint
        data = {
            "product_name": "Test Product",
            "rating": 5,
            "description": "Excellent product!"
        }
        headers = {
            "Authorization": "Bearer test_token"  # Replace with a valid token if needed
        }
        response = self.client.post('/review/add', json=data, headers=headers)
        self.assertIn(response.status_code, [201, 400, ])  # Expect success or validation error

    def test_update_review(self):
        # Test the /update endpoint
        data = {
            "product_name": "Test Product",
            "rating": 4,
            "description": "Updated review description."
        }
        headers = {
            "Authorization": "Bearer test_token"  # Replace with a valid token if needed
        }
        response = self.client.put('/review/update', json=data, headers=headers)
        self.assertIn(response.status_code, [201, 400, ])

    def test_delete_review(self):
        # Test the /delete endpoint
        data = {
            "product_name": "Test Product"
        }
        headers = {
            "Authorization": "Bearer test_token"  # Replace with a valid token if needed
        }
        response = self.client.delete('/review/delete', json=data, headers=headers)
        self.assertIn(response.status_code, [200, 400, ])

    def test_get_reviews_by_customer(self):
        # Test the /get/all_by_customer endpoint
        headers = {
            "Authorization": "Bearer test_token"  # Replace with a valid token if needed
        }
        response = self.client.get('/review/get/all_by_customer', headers=headers)
        self.assertIn(response.status_code, [200, 400, ])

    def test_get_reviews_by_product(self):
        # Test the /get/all_by_product endpoint
        data = {
            "product_name": "Test Product"
        }
        headers = {
            "Authorization": "Bearer test_token"  # Replace with a valid token if needed
        }
        response = self.client.get('/review/get/all_by_product', json=data, headers=headers)
        self.assertIn(response.status_code, [200, 400, ])

    def test_get_specific_review(self):
        # Test the /get/specific endpoint
        data = {
            "review_id": 1  # Replace with a valid review ID if needed
        }
        headers = {
            "Authorization": "Bearer test_token"  # Replace with a valid token if needed
        }
        response = self.client.get('/review/get/specific', json=data, headers=headers)
        self.assertIn(response.status_code, [200, 400, ])

    def test_flag_review(self):
        # Test the /flag endpoint
        data = {
            "review_id": 1  # Replace with a valid review ID if needed
        }
        headers = {
            "Authorization": "Bearer admin_token"  # Replace with a valid admin token if needed
        }
        response = self.client.post('/review/flag', json=data, headers=headers)
        self.assertIn(response.status_code, [201, 400, ])

    def test_delete_review_admin(self):
        # Test the /delete_admin endpoint
        data = {
            "review_id": 1  # Replace with a valid review ID if needed
        }
        headers = {
            "Authorization": "Bearer admin_token"  # Replace with a valid admin token if needed
        }
        response = self.client.delete('/review/delete_admin', json=data, headers=headers)
        self.assertIn(response.status_code, [201, 400, ])

if __name__ == "__main__":
    unittest.main()
