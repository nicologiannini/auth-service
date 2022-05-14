from datetime import datetime

class User():
    def __init__(self):
        self._username = None
        self._email = None
        self._password = None
        self._multi_factor = False
        self._created_at = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def multi_factor(self):
        return self._multi_factor

    @property
    def created_at(self):
        return self._created_at

    @username.setter
    def username(self, username):
        self._username = username

    @email.setter
    def email(self, email):
        self._email = email

    @password.setter
    def password(self, password):
        self._password = password

    @multi_factor.setter
    def multi_factor(self, is_enabled):
        self._multi_factor = is_enabled


class Response():
    def __init__(self):
        self.status_code = None
        self.body = None
        self.error = None
