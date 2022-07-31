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

You must set in your .env file the following variables:

MAILJET_API_KEY=75444ec4456485fdda8f077ec7e93283
MAILJET_API_SECRET=dbdba5443ecefab04bfb87139cb2550e

Create and Running
```
$ docker-compose up -d --build
```

Testing the API :

In order to test, you must know the name of the container id.

```
docker ps


CONTAINER ID   IMAGE                COMMAND                  CREATED             STATUS         PORTS                               NAMES
9e92093da3e4   sample_fastapi_api   "uvicorn app.main:ap…"   About an hour ago   Up 8 seconds   0.0.0.0:8000->8000/tcp              api
7d421f9b1810   sample_fastapi_db    "docker-entrypoint.s…"   About an hour ago   Up 9 seconds   0.0.0.0:3306->3306/tcp, 33060/tcp   db
```	

You want to connect to the API
```
$ docker exec -it 9e92093da3e4 bash
cd /usr/src/server
pytest
```	


# Using the API

I noticed that sending an email to a hotmail account is not working. Please use a temp mail like "https://temp-mail.org/"


```

```


# Demo
## Document of API
http://localhost:8000/docs


Hi,
Congratulations on reaching this stage. We suggest that you take the time to read this technical test and to give us feedback when you are done.
We will propose you a debriefing with team members afterwards. 
If you have any questions, don't hesitate to come back to me.

## Context

Dailymotion handles user registrations. To do so, user creates an account and we send a code by email to verify the account.
As a core API developer, you are responsible for building this feature and expose it through API.

## Specifications

You have to manage a user registration and his activation.
The API must support the following use cases:
* Create a user with an email and a password.
* Send an email to the user with a 4 digits code.
* Activate this account with the 4 digits code received. For this step, we consider a `BASIC AUTH` is enough to check if he is the right user.
* The user has only one minute to use this code. After that, an error should be raised.
Design and build this API. You are completely free to propose the architecture you want.
## What do we expect?
- Your application should be in Python.
- We expect to have a level of code quality which could go to production.
- Using frameworks is allowed only for routing, dependency injection, event dispatcher, db connection. Don't use magic (ORM for example)! We want to see **your** implementation.
- Use the DBMS you want (except SQLite).
- Consider the SMTP server as a third party service offering an HTTP API. You can mock the call, use a local SMTP server running in a container, or simply print the 4 digits in console. But do not forget in your implementation that **it is a third party service**.
- Your code should be tested.
- Your application has to run within a docker containers.
- You should provide us the source code (or a link to GitHub)
- You should provide us the instructions to run your code and your tests. We should not install anything except docker/docker-compose to run you project.
- You should provide us an architecture schema.
