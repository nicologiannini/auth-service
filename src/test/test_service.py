import unittest
import src.utils.authorizer as authorizer
import src.utils.authenticator as authenticator
import src.utils.exceptions as exceptions


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
        assert len(hashed_pwd.split(":")) == 2
        assert len(hashed_pwd) == 97


class TestAuthorizer(unittest.TestCase):
    def test_generate_token(self):
        token = authorizer.generate_token("abcd")
        assert len(token.split(".")) == 3

    def test_token(self):
        token = authorizer.generate_token("abcd")
        payload = authorizer.validate_token(token)
        assert {"iat", "exp", "usr"} == dict(payload).keys()


if __name__ == "__main__":
    unittest.main()
