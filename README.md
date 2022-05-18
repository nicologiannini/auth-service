# basic-login-system
A simple authentication system that supports registration, basic safe login and two-factor-authentication, sends e-mail when a token is generated.

Once you have imported the docker image, you need to set some environment variables, i suggest to run this command: 
```bash
docker run -d -p 5000:5000 -e PYTHONUNBUFFERED=1 -e ENABLE_LOG=1 -e SECRET_KEY=12345 -e SERVER_MAIL={your_gmail} -e SERVER_MAIL_PWD={your_gmail_password} basic-login-system
```

\* in this case we can access the server from localhost:5000
\* SERVER_MAIL and SERVER_MAIL_PWD need to be set
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
