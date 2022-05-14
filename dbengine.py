import sqlite3
import contextlib
from classes import User

def execute_statement(statement, params=None) -> bool:
    try:
        with contextlib.closing(sqlite3.connect('database.db')) as conn:
            with conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute(statement, params) if params else cursor.execute(statement)
        return True
    except Exception as e:
        return False

def execute_raw_query(query):
    try:
        with contextlib.closing(sqlite3.connect('database.db')) as conn:
            with conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    result = cursor.execute(query).fetchall()
                    return result
    except Exception as e:
        return False

def create_users_table():
    return execute_statement(
        'CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, email TEXT, password TEXT, multi_factor TEXT, created_at TEXT, auth_token TEXT, token_exp_datetime TEXT)')

def insert_user(user: User):
    return execute_statement("INSERT INTO users (username, email, password, multi_factor, created_at) VALUES (?, ?, ?, ?, ?)",
                      (user.username, user.email, user.password, str(user.multi_factor), user.created_at))

def get_user_by_username(username):
    result = execute_raw_query(f"SELECT * FROM users WHERE username = '{username}'")
    return result[0] if len(result) > 0 else False

if __name__ == '__main__':
    create_users_table()
