import sqlite3

DB_NAME = "totally_not_my_privateKeys.db"

def check_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT kid, exp FROM keys")
    keys = cursor.fetchall()
    conn.close()
    print("Keys in database:", keys)

if __name__ == "__main__":
    check_db()
