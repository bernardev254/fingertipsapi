# fingertipsapi
## Table of Contents

- [Introduction](#introduction)
- [Endpoints](#endpoints)
- [Requests&ResponseFormat](#requests&responseformat)
- [Authentication](#authentication)
- [Errorcodes](#errorcodes)
- [Deployment](#deployment)

## Introduction

fingertips is a bookmarking solution that allows for collection and management of bookmarks for easier access.This api connects the frontend with the database by providing endpoints to get to the bookmarks

## Endpoints

| VERB     |      Route          |          Description            |
|----------|---------------------|---------------------------------|
| POST     | /new                | creates a new bookmark          |
| GET      | /my_bookmarks       | gets all the bookmark for a user|
| POST     | /getBookmarkDetails | get details for a bookmark      |
| DELETE   | /remove             | remove a bookmark from the db   |
| PATCH    | /update             | updates bookmark details        |

## Requests and Response Format

### requests format
All API requests must be made using the HTTP POST method and include the following headers
```
Content-Type: application/json
Authorization: Bearer <token>

```
the token is acquired during authentication

example request:
```bash
curl -i --header "content-Type": "application/json"/
        "Authorization": "Bearer <access token>"/
        https://fingertips.onrender.com/api/v1/mookmarks/my_bookmarks
```

### Response

the response is in json providing the data and response code

```json
HTTP/2 200 
date: Mon, 06 Feb 2023 10:40:06 GMT
{
  "bookmarks": [
    {
      "body": "", 
      "icon": "https://cdn.sstatic.net/Sites/stackoverflow/Img/favicon.ico?v=ec617d715196", 
      "id": 12, 
      "title": "Stack Overflow - Where Developers Learn, Share, & Build Careers", 
      "url": "https://stackoverflow.com/"
    }, 
    {
      "body": "", 
      "icon": "https://cdn.realpython.com/static/favicon.68cbf4197b0c.png", 
      "id": 13, 
      "title": "Flask by Example \u2013 Setting up Postgres, SQLAlchemy, and Alembic \u2013 Real Python", 
      "url": "https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/"
    }
  ]
}

```
## Authentication

this api uses jwt authentication where a user uses a password and an email on registration and is given an access token on login.Using this token we can access all the protected endpoints

get access token with two easy steps 
### register
```
curl -i -XPOST --header 'content_Type: application/json' --data '{"Username":"test","email":"test@gmail.com","password":"test"}' https://fingertipsapi.onrender.com/api/v1/auth/register
```
```json
created 201  
{
  "email": "test@gmail.com", 
  "message": "user created", 
  "username": "test"
}
```


### login
```
curl -i -XPOST --header 'content_Type: application/json' --data '{"email":"bernard1@gmail.com","password":"bernard1"}' https://fingertipsapi.onrender.com/api/v1/auth/login
```
```
{
	"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NTY4Mzc4NywianRpIjoiMDBlYmEzODctZDk5OS00YzJjLWJlZDAtNTkwNTc2MjE3MmYxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjc1NjgzNzg3fQ.4tq2cwur8GKEikJ9uhI12ULFLlmmvzjgDmXdIXN06Gc",
	"email": "test@gmail.com",
	"username": "test"
}
```
## Error codes

|code   | route       |          Description            |
|-------|-------------|---------------------------------|
| 400   | /register   | username already exixts         |
| 400   | /login      | wrong credentials               |


## Deployment

### on local environment:
configure the database

```
pip -r install requirements.txt
python3 -m app.py
```

### on cloud:
clone this repository on the remote server
configure environment variables
```DB_URI=""
   MY_SECRET=""
   MY_JWT_SECRET=""
```
```
pip -r install requirements.txt
gunicorn app:app
```

####link to live site consuming the api
```
https://fingertips-lite.onrender.com

```




