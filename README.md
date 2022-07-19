# auth-service

[![CircleCI](https://circleci.com/gh/nicologiannini/auth-service/tree/main.svg?style=svg)](https://circleci.com/gh/nicologiannini/auth-service/tree/main)

A simple authentication system that supports registration, login and session.
To run the project, build the .Dockerfile in the repository and then run the command

```bash
docker run --name [container_name]  -p 80:80  auth-service:latest
```

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
