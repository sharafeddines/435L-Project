import unittest
from flask import Flask
from inventory_service import create_app

class TestInventoryService(unittest.TestCase):
    def setUp(self):
        # Configure the test client
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

        with self.app.app_context():
            # Add an initial inventory item
            self.client.post('/goods', json={
                "name": "Laptop",
                "category": "Electronics",
                "price_per_item": 1500.0,
                "description": "High-performance laptop",
                "count_in_stock": 10
            })
    
    def test_health_check(self):
        # Test the /health endpoint
        response = self.client.get('/inventory/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn("service", response.json)

    def test_add_goods(self):
        # Test the /goods POST endpoint
        data = {
            "name": "Smartphones",
            "category": "Electronics",
            "price_per_item": 800.0,
            "description": "Latest smartphone model",
            "count_in_stock": 20
        }
        response = self.client.post('/inventory/goods', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("goods", response.json)

    def test_deduct_goods(self):
        item_id = 1  # Assuming the first item has ID 1
        data = {"count": 2}
        response = self.client.post(f'/inventory/goods/{item_id}/deduct', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("goods", response.json)

    def test_update_goods(self):
        # Test the /goods/<item_id> PUT endpoint
        item_id = 1  # Assuming the first item has ID 1
        data = {"price_per_item": 1400.0, "description": "Discounted laptop"}
        response = self.client.put(f'/inventory/goods/{item_id}', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("goods", response.json)
        self.assertEqual(response.json["goods"]["price_per_item"], 1400.0)

    def test_get_all_inventory(self):
        # Test the / GET endpoint
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)
        self.assertIn("name", response.json[0])
        

    

if __name__ == "__main__":
    unittest.main()
