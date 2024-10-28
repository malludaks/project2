import jwt

# Define your payload and secret (these should match what `gradebot.exe` expects)
payload = {"some": "data"}
secret = "your_secret_key"  # Replace with your actual secret key
token = jwt.encode(payload, secret, algorithm="HS256")

# Print the generated token
print("Generated JWT:", token)
