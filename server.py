from flask import Flask, jsonify, request, make_response
import sqlite3
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import jwt
import base64

# Define a shared secret key for HS256
SHARED_SECRET = "your-256-bit-secret"  # Replace with an actual secure key

app = Flask(__name__)
DB_NAME = "totally_not_my_privateKeys.db"
KID = "fixed-kid-for-hs256"  # Fixed kid for JWKS compatibility

def initialize_database():
    """Initializes the SQLite database and creates the table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Create the keys table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS keys(
                kid INTEGER PRIMARY KEY AUTOINCREMENT,
                key BLOB NOT NULL,
                exp INTEGER NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        print("Database initialized with the keys table.")
    except sqlite3.OperationalError as e:
        print("Error initializing database:", e)

def generate_and_store_key(expiration_in_hours):
    """Generates an RSA private key, stores it in SQLite with expiration time."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    pem_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    expiration = datetime.utcnow() + timedelta(hours=expiration_in_hours)
    exp_timestamp = int(expiration.timestamp())
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO keys (key, exp) VALUES (?, ?)", (pem_key, exp_timestamp))
    conn.commit()
    cursor.execute("SELECT * FROM keys WHERE exp = ?", (exp_timestamp,))
    result = cursor.fetchone()
    if result:
        print(f"Key with expiration at {expiration} (expired: {expiration_in_hours < 0}) inserted.")
    else:
        print("Failed to insert key.")
    conn.close()

def check_for_expired_keys():
    """Checks if there is an expired key in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = int(datetime.utcnow().timestamp())
    cursor.execute("SELECT * FROM keys WHERE exp <= ?", (now,))
    expired_keys = cursor.fetchall()
    conn.close()
    
    if expired_keys:
        print("Expired keys found in the database.")
        for key in expired_keys:
            print(f"KID: {key[0]}, Expiry: {datetime.utcfromtimestamp(key[2])}")
    else:
        print("Error: No expired keys found in the database.")
    return bool(expired_keys)


def get_private_key(expired=False):
    """Fetches a private key from SQLite based on expiration status."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        now = int(datetime.utcnow().timestamp())
        query = "SELECT key FROM keys WHERE exp <= ?" if expired else "SELECT key FROM keys WHERE exp > ?"
        cursor.execute(query, (now,))
        row = cursor.fetchone()
        print(f"Row fetched: {row}")  # Debug pri
        conn.close()
        if row:
            return serialization.load_pem_private_key(row[0], password=None, backend=default_backend())
        return None
    except Exception as e:
        print("Error retrieving private key:", e)
        return None

@app.route('/auth', methods=['POST'])
def auth():
    """Issues JWT using HS256 with a shared secret key."""
    expired = request.args.get('expired', 'false').lower() == 'true'

    # Set token expiration based on whether it's expired or not
    expiration_time = datetime.utcnow() - timedelta(minutes=1) if expired else datetime.utcnow() + timedelta(minutes=30)
    
    # Create the JWT payload with a fixed kid in the header
    payload = {
        "user": "userABC",
        "exp": expiration_time
    }
    
    # Encode the token with HS256 and include the fixed kid in the header
    token = jwt.encode(payload, SHARED_SECRET, algorithm='HS256', headers={'kid': KID})
    return jsonify({"token": token})

@app.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
    """Serves a JWKS with a single fixed key entry for HS256 compatibility."""
    # Create a placeholder JWK entry for HS256 compatibility
    jwk = {
        "kid": KID,
        "kty": "oct",
        "alg": "HS256",
        "use": "sig",
        "k": base64.urlsafe_b64encode(SHARED_SECRET.encode()).decode('utf-8').rstrip("=")
    }
    return jsonify({"keys": [jwk]})

# Main block to initialize the database, generate keys, and start the server
if __name__ == "__main__":
    initialize_database()
    # Generate an expired key with an expiration time in the past (-1 hour)
    generate_and_store_key(-1)
    # Generate a valid key with an expiration time in the future (+1 hour)
    generate_and_store_key(1)

    # Verify the presence of expired keys before starting the server
    if check_for_expired_keys():
        print("Starting server with expired key(s) confirmed in the database.")
        app.run(host='127.0.0.1', port=8080)
    else:
        print("Exiting: No expired keys found in the database.")
