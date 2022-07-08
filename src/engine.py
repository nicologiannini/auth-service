import psycopg2
import contextlib
from enum import Enum
from src.config import DB_CONFIG


class QueryType(Enum):
    Statement = 0
    Fetchall = 1
    Fetchone = 2


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


def execute_statement(query, params=None):
    return _execute(query, params, QueryType.Statement.value)


def execute_fetchall(query, params=None):
    return _execute(query, params, QueryType.Fetchall.value)


def execute_fetchone(query, params=None):
    return _execute(query, params, QueryType.Fetchone.value)


def _execute(query, params=None, type=None, config=DB_CONFIG):
    result = None
    conn = psycopg2.connect(**config)
    try:
        with conn:
            with contextlib.closing(conn.cursor()) as cursor:
                cursor.execute(
                    query, params) if params else cursor.execute(query)
                match type:
                    case QueryType.Fetchone.value:
                        result = cursor.fetchone()
                    case QueryType.Fetchall.value:
                        result = cursor.fetchall()
                    case QueryType.Statement.value:
                        result = True
                    case _:
                        result = None
                conn.commit()
    except Exception as e:
        conn.rollback()
        result = False
    finally:
        conn.close()
        return result
