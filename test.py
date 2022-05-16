import unittest
import utils
from mock import patch

class TestValidation(unittest.TestCase):
    def test_validate_username(self):
        with patch("dbengine.get_user_by_username") as patched:
            patched.return_value = False
            self.assertEqual(utils.validate_username("test"), "test")
            self.assertRaises(ValueError, utils.validate_username, "")
        
    def test_validate_email(self):
        with patch("dbengine.get_user_by_email") as patched:
            patched.return_value = False
            self.assertEqual(utils.validate_email("test@gmail.com"), "test@gmail.com")
            self.assertRaises(ValueError, utils.validate_email, "test@")
            self.assertRaises(TypeError, utils.validate_email, 0)
    
    def test_validate_password(self):
        self.assertEqual(utils.check_password_hash(utils.validate_password('12345678'), '12345678'), True)
        self.assertRaises(ValueError, utils.validate_email, 'abcd')

    def test_validate_multi_factor(self):
        self.assertEqual(utils.validate_multi_factor(True), 1)
        self.assertRaises(ValueError, utils.validate_multi_factor, 0)





if __name__ == "__main__":
    unittest.main()
