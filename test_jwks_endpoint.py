import requests

try:
    response = requests.get("http://127.0.0.1:8080/.well-known/jwks.json")
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Error:", e)
