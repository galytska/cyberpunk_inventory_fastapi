# cyberpunk_inventory_fastapi

## Set up  
Project dependencies listed in **requirements.txt** file

Database path example specified in **database.py**

`SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/sample_db"`

## Run project
To run the application use command
```
uvicorn inventory_app.main:app --reload
```

## Project's structure 
endpoints implementation stored in **routers** directory

test implementation stored in **tests** directory
## Features
During the testing in memory database is used so no additional files created 

All endpoints **except prefixing auth** secure with authentication
so a user can see only own items

The admin user authorised to see all items of all users 
## Test
To run the tests use command
```
cyberpunk_inventory_fastapi$ pytest
```
To run one most basic test for the health check of the project run
```
cyberpunk_inventory_fastapi$ pytest -k "smoke"
```