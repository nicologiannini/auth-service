import psycopg2
import contextlib
from src.config import DB_CONFIG


def execute_statement(query, params=None):
    return _execute(query, params)


def execute_fetchall(query, params=None):
    return _execute(query, params, "fetchall")


def execute_fetchone(query, params=None):
    return _execute(query, params, "fetchone")


def _execute(query, params=None, type=None, config=DB_CONFIG):
    result = None
    try:
        with contextlib.closing(psycopg2.connect(**config)) as conn:
            with conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute(
                        query, params) if params else cursor.execute(query)
                    match type:
                        case "fetchone":
                            result = cursor.fetchone()
                        case "fetchall":
                            result = cursor.fetchall()
                        case _:
                            result = True
                    conn.commit()
    except Exception as e:
        result = False
    finally:
        conn.close()
        return result


def database_init():
    create_users_table()


def create_users_table():
    return execute_statement("""CREATE TABLE IF NOT EXISTS users(
                                    id VARCHAR(36) PRIMARY KEY,
                                    created_at INT NOT NULL,
                                    status INT,
                                    first_name VARCHAR(24) NOT NULL,
                                    last_name VARCHAR(24) NOT NULL,
                                    email VARCHAR(36) NOT NULL,
                                    password VARCHAR(128) NOT NULL)""")
