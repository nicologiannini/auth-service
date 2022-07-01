import unittest
import src.utils.authorizer as authorizer
import src.utils.authenticator as authenticator
import src.utils.exceptions as exceptions
from mock import patch


class TestAuthenticator(unittest.TestCase):
    def test_validate_email(self):
        email = "testgmail.com"
        self.assertRaises(
            exceptions.ValidationError, authenticator.validate_email, email)

    def test_validate_password(self):
        pwd = "123"
        self.assertRaises(
            exceptions.ValidationError, authenticator.validate_password, pwd)

    def test_password(self):
        pwd = "12345678"
        hashed_pwd = authenticator.secure_password(pwd)
        self.assertRaises(
            exceptions.Unauthorized, authenticator.verify_password, hashed_pwd,
            "abcd")


class TestAuthorizer(unittest.TestCase):
    def test_token(self):
        token = authorizer.generate_token("abcd", "12345678")
        payload = authorizer.validate_token(token)
        assert {"iat", "exp", "usr", "pwd"} == dict(payload).keys()


if __name__ == "__main__":
    unittest.main()
