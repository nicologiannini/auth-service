from datetime import datetime

class User():
    def __init__(self):
        self._id = None
        self._username = None
        self._email = None
        self._password = None
        self._multi_factor = None
        self._created_at = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self._auth_token = None
        self._token_exp_date = None

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

    @property
    def auth_token(self):
        return self._auth_token

    @property
    def token_exp_date(self):
        return self._token_exp_date

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

    @auth_token.setter
    def auth_token(self, token):
        self._auth_token = token

    @token_exp_date.setter
    def token_exp_date(self, date):
        self._token_exp_date = date

    def load(self, id, username, email, password, multi_factor, created_at, auth_token, token_exp_date):
        self._id = int(id)
        self._username = username
        self._email = email
        self._password = password
        self._multi_factor = bool(multi_factor)
        self._created_at = created_at
        self._auth_token = auth_token
        self._token_exp_date = token_exp_date

class Response():
    def __init__(self):
        self.status_code = None
        self.body = {}
        self.error = ''

    def failed(self, status, error = ''):
        self.status_code = status
        self.error = error
