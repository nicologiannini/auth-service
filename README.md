# basic-login-system
Once you have imported the docker image, you need to set some environment variables, i suggest to run this command: 
`docker run -d -p 5000:5000 -e PYTHONUNBUFFERED=1 -e ENABLE_LOG=1 -e SECRET_KEY=12345 -e SERVER_MAIL={your_gmail} -e SERVER_MAIL_PWD={your_gmail_password} basic-login-system`

\* in this case we can access the server from localhost:5000
### Endpoint
* http://localhost:5000 **/register/** <br/>
```json
{
    "username": "test", // 4-16 char
    "email": "test@gmail.com",
    "password": "12345678", // 8-16 char
    "multi_factor": true // boolean
}
```
The registration flow of new users is managed from this route. Following the validation steps if all parameters are compliant a new record is saved in the database.
<br/>
* http://localhost:5000 **/login/** <br/>
```json
{
    "username": "test", // 4-16 char
    "password": "12345678", // 8-16 char
}
```
From here you can log in for a specific user the password passed as a parameter will be compared with the one saved during registration.

In case of multi_factor instead a token will be generated and sent to the user's email.
<br/>
* http://localhost:5000<span>**/multi_factor/**</span><br/>
```json
{
    "username": "test", // 4-16 char
    "token": "000000", // 6-digit
}
```
 Endpoint for system access via token validation for multi-factor authentication. Access will be granted only in case of correct and non-expired token (5 minutes from generation).
