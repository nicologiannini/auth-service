from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    username: str
    email: str
    password: str
    multi_factor: int = 0
    created_at: str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    auth_token: str = ''
    token_exp_date: str = ''

@dataclass
class Response:
    status_code: int = 0
    body: dict = field(default_factory=dict)

    def succeded(self, status: int, message: str = ''):
        self.status_code = status
        self.body['message'] = message

    def failed(self, status: int, error: str = ''):
        self.status_code = status
        self.body['error'] = error
