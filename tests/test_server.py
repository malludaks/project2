import unittest
import requests

class JWKSAuthTests(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:8080"

    def test_jwks_endpoint(self):
        """Test if JWKS endpoint returns a 200 status and correct structure."""
        response = requests.get(f"{self.BASE_URL}/.well-known/jwks.json")
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn("keys", json_response)

    def test_auth_endpoint_valid_key(self):
        """Test if /auth endpoint returns a JWT with a valid key."""
        response = requests.post(f"{self.BASE_URL}/auth")
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn("token", json_response)

    def test_auth_endpoint_expired_key(self):
        """Test if /auth endpoint returns a JWT with an expired key."""
        response = requests.post(f"{self.BASE_URL}/auth?expired=true")
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn("token", json_response)

if __name__ == '__main__':
    unittest.main()
