# cyberpunk_inventory_fastapi

## Set up

Project dependencies listed in **requirements.txt** file

Database path defined with the environment variable **DATABASE_URL** for example

`DATABASE_URL = "postgresql://postgres:postgres@mydb/sample_db"`

## Run project

To run the application use command 
from the project directory cyberpunk_inventory_fastapi$ 

```
uvicorn inventory_app.main:app --reload
```

## Project's structure

Endpoints implementation stored in **routers** directory

Test implementation stored in **tests** directory

## Features

During the testing in memory database is used so no additional files created

All endpoints **except prefixing auth** secure with authentication
so a user can see only own items

The admin user authorised to see all items of all users

## Test

To run the tests use command
from the project directory cyberpunk_inventory_fastapi$
```
pytest
```

To run one most basic test for the health check of the project run
from the project directory cyberpunk_inventory_fastapi$
```
pytest -k "smoke"
```

## Deployment
Project includes Dockerfile and docker-compose.yaml file for easy deployment using docker compose.
```
docker-compose up -d
```
