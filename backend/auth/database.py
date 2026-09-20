import sqlite3
from pathlib import Path


# ============================================================
# DATABASE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_PATH = BASE_DIR / "users.db"


# ============================================================
# GET CONNECTION
# ============================================================

def get_connection():

    return sqlite3.connect(
        DATABASE_PATH
    )


# ============================================================
# CREATE USERS TABLE
# ============================================================

def create_users_table():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()

    connection.close()


# ============================================================
# CREATE USER
# ============================================================

def create_user(
    username: str,
    email: str,
    password_hash: str
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (username, email, password_hash)
        VALUES (?, ?, ?)
        """,
        (
            username,
            email,
            password_hash
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# FIND USER
# ============================================================

def get_user(
    username: str
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, username, email, password_hash
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()

    connection.close()

    return user