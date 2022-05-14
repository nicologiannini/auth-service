import dbengine
import re

def validate_username(username):
    if not dbengine.get_user_by_username(username) and len(username) <= 25:
        return username
    else:
        raise ValueError("username is not valid.")

def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email) and len(email) <= 40:
        return email
    else:
        raise ValueError("email is not valid.")

def validate_multi_factor(is_enabled):
    if isinstance(is_enabled, bool):
        return is_enabled
    else:
        raise ValueError('multi_factor should be boolean type.')
