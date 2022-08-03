# Overview
This project is a project for Dailymotion. This is the functionnality of the project.

* Create a user with an email and a password.
* Send an email to the user with a 4 digits code.
* Activate this account with the 4 digits code received. For this step, we consider a BASIC AUTH is enough to check if he is the right user.
* The user has only one minute to use this code. After that, an error should be raised. Design and build this API. You are completely free to propose the architecture you want.

BONUS:
* CRUD system for the users.
* Hashed passwords.

# Install

You must create a .env in *code/app/.env*. 
The file must contain somes variables. Go to this link and copy past it in your .env file.
Password: dailymotion
```
https://pastebin.com/eSaFuRiH

```


Create and Running
```
$ docker-compose up -d --build
```

Testing the API :

To test the API, you can use the following command:


```
docker exec -it api bash
# If needed cd /usr/src/server
pytest
```	


# Using the API

There is two sections in the API. The first one is the user section. The second one is the login section.

The user section is basicaly a CRUD system. You can read users, create user, update user and delete user or search for a specific email
```	
GET /api/v1/user/ # Get all users
POST /api/v1/user/ # Create a user
GET /api/v1/user/{id} # Get a user by id
PUT /api/v1/user/{id} # Update a user by id
DELETE /api/v1/user/{id} # Delete a user by id
GET /api/v1/user/search/{email} # Search a user by email
```	
The login section is a login system. It allows you to connect with your account with a bearer token.
```	
POST /api/v1/login/auth : This is the login section. You can connect with your account with a bearer token.
POST /api/v1/login/me : This is the login section. It allows you to get your account information.
POST /api/v1/login/veryfy-email: This is the login section. It allows you to send a verification code to activate your account
POST /api/v1/login/verify-email/send:  It sends a token to validate your accoutn by sending an email with MAILJET
POST /api/v1/login/activate-user: It allows you to activate your account with a token.
```	

I noticed that sending an email to a hotmail account is not working. Please use a temp mail like "https://temp-mail.org/"

## Schema:

https://ibb.co/J56H1LP

## Improvement of the API

I didn't have time to implement every feature of the API. This is a quick list of improvment I could do:
- [ ] Using Poetry instead of requirements.txt
- [ ] Don't use an ORM
- [ ] Implement a CI/CD system
- [ ] A better test system like inserting data in the database for testing (instead of using a random email) or using a mock object for testing
- [ ] Better tests for login section (expiration token, wrong token, wrong email)
