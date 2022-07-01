# auth-service

[![CircleCI](https://circleci.com/gh/nicologiannini/auth-service/tree/main.svg?style=svg)](https://circleci.com/gh/nicologiannini/auth-service/tree/main)

A simple authentication system that supports registration, login and authorization.

## Endpoint
### /register/
POST method that requires the following body:
```javascript
{
    "first_name": "test",
    "last_name": "test",
    "email": "test@gmail.com",
    "password": "12345678"
}
```

### /login/
POST method that requires the following body:
```javascript
{
    "username": "test",
    "password": "12345678",
}
```

## Testing
```bash
pytest test.py
```
