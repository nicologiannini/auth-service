import sqlite3
import contextlib
from classes import User

DB = 'database.db'

def execute_statement(statement, params=None) -> bool:
    try:
        with contextlib.closing(sqlite3.connect(DB)) as conn:
            with conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute(
                        statement, params) if params else cursor.execute(statement)
        return True
    except Exception as e:
        return False

def execute_raw_query(query):
    try:
        with contextlib.closing(sqlite3.connect(DB)) as conn:
            with conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    result = cursor.execute(query).fetchall()
                    return result
    except Exception as e:
        return False

def database_init():
    create_users_table()

def create_users_table():
    return execute_statement(
        "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, email TEXT UNIQUE, password TEXT, multi_factor INTEGER, created_at TEXT, token TEXT, token_exp TEXT)")

def insert_user(user: User):
    return execute_statement("INSERT INTO users (username, email, password, multi_factor, created_at) VALUES (?, ?, ?, ?, ?)",
                             (user.username, user.email, user.password, str(user.multi_factor), user.created_at))

def get_user_by_username(username):
    result = execute_raw_query(
        f"SELECT * FROM users WHERE username = '{username}'")
    return result[0] if result else False

def get_user_by_email(email):
    result = execute_raw_query(f"SELECT * FROM users WHERE email = '{email}'")
    return result[0] if result else False

def update_user_token_info(user: User):
    return execute_statement(f"UPDATE users SET token = '{user.token}', token_exp = '{user.token_exp}' WHERE username = '{user.username}'")
