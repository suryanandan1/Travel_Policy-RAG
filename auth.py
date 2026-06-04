import sqlite3
import hashlib


def create_user_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT UNIQUE,
        name TEXT,
        password TEXT,
        band TEXT
    )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def signup(employee_id, name, password, band):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users(employee_id,name,password,band)
            VALUES(?,?,?,?)
            """,
            (
                employee_id,
                name,
                hash_password(password),
                band
            )
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def login(employee_id, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE employee_id=?
        AND password=?
        """,
        (
            employee_id,
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user