import src.engine as engine
import src.utils.exceptions as exceptions
import src.utils.messages as messages
import src.utils.helper as helper
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime


class UserStatus(Enum):
    Locked = 0
    Active = 1


@dataclass
class User:
    id: str = field(default_factory=helper.generate_uuid)
    created_at: int = int(datetime.timestamp(datetime.now()))
    status: int = UserStatus.Active.value
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    password: str = ""

    def insert(self) -> None:
        if not _insert_user(self):
            raise exceptions.InternalError(messages.GENERIC_ERROR)

    def update(self) -> None:
        if not _update_user(self):
            raise exceptions.InternalError(messages.GENERIC_ERROR)

    def delete(self) -> None:
        if not _delete_user(self.id):
            raise exceptions.InternalError(messages.GENERIC_ERROR)


def get_user(user_id) -> User:
    user = _get_user(user_id)
    if not user:
        raise exceptions.InternalError(messages.GENERIC_ERROR)

    return User(*user)


def get_user_by_email(email) -> User:
    user = _get_user_by_email(email)
    if not user:
        raise exceptions.InternalError(messages.GENERIC_ERROR)

    return User(*user)


def check_user_by_email(email) -> bool:
    return True if _get_user_by_email(email) else False


def _insert_user(user: User) -> bool:
    return engine.execute_statement(
        "INSERT INTO users(id, created_at, status, first_name, last_name, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (user.id, user.created_at, user.status, user.first_name, user.last_name,
         user.email, user.password))


def _update_user(user: User) -> bool:
    return engine.execute_statement(
        "UPDATE users SET status = %s,  first_name = %s, last_name = %s, email = %s, password = %s WHERE id = %s",
        (user.status, user.first_name, user.last_name, user.email, user.password, user.id))


def _delete_user(user_id) -> bool:
    return engine.execute_statement("DELETE FROM users WHERE id = %s",
                                    (user_id,))


def _get_user(user_id):
    return engine.execute_fetchone("SELECT * FROM users WHERE id = %s",
                                   (user_id,))


def _get_user_by_email(email):
    return engine.execute_fetchone("SELECT * FROM users WHERE email = %s",
                                   (email,))
