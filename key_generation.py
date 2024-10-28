# key_generation.py
import sqlite3
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta

# Database name
DB_NAME = "totally_not_my_privateKeys.db"

def initialize_database():
    """Initialize the SQLite database and create the table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS keys(
                kid INTEGER PRIMARY KEY AUTOINCREMENT,
                key BLOB NOT NULL,
                exp INTEGER NOT NULL
            )
        """)
        conn.commit()
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print("Error initializing database:", e)
    finally:
        conn.close()

def generate_and_store_key(expiration_in_hours):
    """Generates an RSA private key and stores it in SQLite with an expiration time."""
    try:
        # Generate RSA private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # Serialize the private key to PEM format
        pem_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Calculate expiration time
        expiration = datetime.utcnow() + timedelta(hours=expiration_in_hours)
        exp_timestamp = int(expiration.timestamp())

        # Store the key in the database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO keys (key, exp) VALUES (?, ?)", (pem_key, exp_timestamp))
        conn.commit()

        kid = cursor.lastrowid  # Fetch the last inserted id (KID)
        print(f"Key with KID {kid} inserted with expiration at {expiration}. (Expired: {expiration_in_hours < 0})")

    except sqlite3.Error as e:
        print("Error storing key in database:", e)
    finally:
        conn.close()

# Main block to initialize the database and generate keys
if __name__ == "__main__":
    initialize_database()
    generate_and_store_key(-1)  # Insert an expired key
    generate_and_store_key(1)   # Insert a valid key
