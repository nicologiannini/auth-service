import unittest
import utils.helper as helper
import utils.validator as validator
import utils.handler as handler
from mock import patch
from classes import Response
from flask_bcrypt import generate_password_hash

class TestValidations(unittest.TestCase):
    def test_validate_username(self):
        with patch('dbengine.get_user_by_username') as patched:
            patched.return_value = False
            self.assertEqual(validator.validate_username('test'), 'test')
            self.assertRaises(ValueError, validator.validate_username, '')

    def test_validate_email(self):
        with patch('dbengine.get_user_by_email') as patched:
            patched.return_value = False
            self.assertEqual(validator.validate_email(
                'test@gmail.com'), 'test@gmail.com')
            self.assertRaises(ValueError, validator.validate_email, 'test@')
            self.assertRaises(TypeError, validator.validate_email, 0)

    def test_validate_password(self):
        self.assertEqual(validator.check_password_hash(
            validator.validate_password('12345678'), '12345678'), True)
        self.assertRaises(ValueError, validator.validate_email, 'abcd')

    def test_validate_multi_factor(self):
        self.assertEqual(validator.validate_multi_factor(True), 1)
        self.assertRaises(ValueError, validator.validate_multi_factor, 0)

class TestVerifications(unittest.TestCase):
    def test_verify_password(self):
        hashed_password = generate_password_hash(
            'abcd1234').decode('utf-8')
        self.assertRaises(ValueError, validator.verify_password,
                          hashed_password, 'abcd1111')

    def test_verify_token(self):
        self.assertRaises(ValueError, validator.verify_token,
                          '123456', helper.time_now(), '000000')

class TestProcessHandlers(unittest.TestCase):
    def test_register_handler(self):
        with patch('dbengine.get_user_by_username') as patched_a, \
                patch('dbengine.get_user_by_email') as patched_b, \
                patch('dbengine.insert_user') as patched_c:
            patched_a.return_value = False
            patched_b.return_value = False
            patched_c.return_value = True
            response_sample = Response()
            data_sample = {'username': 'test', 'email': 'test@gmail.com',
                           'password': '00000000', 'multi_factor': True}
            self.assertEqual(handler.register_handler(
                response_sample, data_sample), None)
            self.assertEqual(response_sample.status_code, 200)
            self.assertRaises(
                AttributeError, handler.register_handler, response_sample, {})

    def test_login_handler(self):
        with patch('dbengine.get_user_by_username') as patched_a, \
                patch('dbengine.update_user_token_info') as patched_b, \
                patch('utils.sender.send_token_mail') as patched_c, \
                patch('utils.handler.session', dict()) as session:
            user_sample = [-1, '', '', generate_password_hash(
                '00000000').decode('utf-8'), 0, '', '', '']
            patched_a.return_value = user_sample
            patched_b.return_value = True
            patched_c.return_value = True
            response_sample = Response()
            data_sample = {'username': 'test', 'password': '00000000'}
            self.assertEqual(handler.login_handler(
                response_sample, data_sample), None)
            self.assertEqual(response_sample.status_code, 200)
            self.assertRaises(
                AttributeError, handler.login_handler, response_sample, {})
            user_sample[4] = 1
            self.assertEqual(handler.login_handler(
                response_sample, data_sample), None)

    def test_multi_factor_handler(self):
        with patch('dbengine.get_user_by_username') as patched, \
                patch('utils.handler.session', dict()) as session:
            user_sample = [-1, '', '', '', 1, '', '123456', helper.time_now()]
            patched.return_value = user_sample
            response_sample = Response()
            data_sample = {'username': 'test', 'token': '123456'}
            self.assertEqual(handler.multi_factor_handler(
                response_sample, data_sample), None)
            self.assertEqual(response_sample.status_code, 200)
            self.assertRaises(
                AttributeError, handler.multi_factor_handler, response_sample, {})


if __name__ == '__main__':
    unittest.main()
