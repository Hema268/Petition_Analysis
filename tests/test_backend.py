import unittest
import requests

class TestBackend(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000/api"

    def test_submit_petition(self):
        response = requests.post(f"{self.BASE_URL}/petitions", data={
            "title": "Fix Road",
            "content": "The road near my house is damaged."
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.json())

    def test_get_petitions(self):
        response = requests.get(f"{self.BASE_URL}/petitions")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

if __name__ == '__main__':
    unittest.main()