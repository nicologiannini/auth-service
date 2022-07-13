from dataclasses import dataclass, field
import uuid


@dataclass
class Result:
    status_code: int = 0
    body: dict = field(default_factory=dict)

    def build(self, status: int, body: dict):
        self.status_code = status
        self.body = body

    def succeded(self, status: int, message: str = ""):
        self.status_code = status
        self.body["message"] = message

    def failed(self, status: int, error: str = ""):
        self.status_code = status
        self.body["error"] = error


def generate_uuid() -> str:
    return uuid.uuid4().hex
