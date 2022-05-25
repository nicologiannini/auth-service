# auth-service
A simple authentication system that supports registration, login and two-factor-authentication, sends email when a token is generated.

## Endpoint
### /register/
POST method that requires the following body:
```javascript
{
    "username": "test", // 4-16 char
    "email": "test@gmail.com",
    "password": "12345678", // 8-16 char
    "multi_factor": true // boolean
}
```
The registration flow of new users is managed from this route. Following the validation steps if all parameters are compliant a new record is saved in the database.
<br/><br/>
### /login/
POST method that requires the following body:
```javascript
{
    "username": "test",
    "password": "12345678",
}
```
From here you can log in for a specific username, the password passed as a parameter will be compared with the one saved during registration.

In case of multi_factor a token will be generated and sent to the user's email instead.
<br/><br/>
### /multi_factor/
POST method that requires the following body:
```javascript
{
    "username": "test",
    "token": "000000", // 6-digit
}
```
Endpoint for system login via token validation for multi-factor authentication. Access will be granted only in case of correct and non-expired token (5 minutes from generation).

## Testing
```bash
pytest test.py
```
