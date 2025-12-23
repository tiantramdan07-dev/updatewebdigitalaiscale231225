# backend/create_admin.py
import os
import getpass
from werkzeug.security import generate_password_hash
import psycopg2

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 5432)),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASS", "gajahbengkak"),
    "dbname": os.environ.get("DB_NAME", "ujicobamodelai")
}

def main():
    first = input("First name: ") or "Admin"
    last = input("Last name: ") or "User"
    email = input("Email: ") or "admin@example.com"
    pw = getpass.getpass("Password: ")
    if not pw:
        print("Empty password, abort.")
        return
    hashed = generate_password_hash(pw)
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (first_name,last_name,email,password_hash,role) VALUES (%s,%s,%s,%s,%s) RETURNING id;",
                (first, last, email, hashed, "admin"))
    uid = cur.fetchone()[0]
    conn.commit()
    cur.close(); conn.close()
    print("Created admin id:", uid)

if __name__ == "__main__":
    main()
