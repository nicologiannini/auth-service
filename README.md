# auth-service

[![CircleCI](https://circleci.com/gh/nicologiannini/auth-service/tree/main.svg?style=svg)](https://circleci.com/gh/nicologiannini/auth-service/tree/main)

A simple authentication system that supports registration, login and session.

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
    "email": "test",
    "password": "12345678"
}
```

## Testing
A CirceCI pipeline is running a test phase on committing/merging on the main branch, to run tests in local environment, after installing all the required dependencies, just run command:
```bash
pytest
```
