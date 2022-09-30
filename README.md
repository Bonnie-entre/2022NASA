## TODO
* frontend page
    - upload page 
    - search page
        - if empty => list all
* change to_chart, make sure pic show

### Maybe Cause Some Bugs
* If there are files with same filename, I should set filename as id when saving file 

### Not Emergency
* check if program hang, and use try to modify
* limit the wsl memory use
* 整理 script (https://fastapi.tiangolo.com/advanced/templates/)



## how poetry works

* start venv

    ```poetry shell```

## how fast api work

* run server

    ```uvicorn app.main:app --reload```

## how to start postgresql in wsl

    ```sudo service postgresql start```
    sudo -u postgres psql

    list database
    ```\l```
    
    list user
    ```\du```

## Problem

* when import path err 

    ```poetry run python -m nlp_model.test```

## css
### flex
* container
    display: flex
    flex-direction:
    justify-content: center; 
    align-items: center;
    width: ;

* obj
    no display


## Alembic
1. Add `sqlalchemy.url= postgresql.....` at ~/alembic.ini
2. Modify ~/alembic/env.py
    `target_metadata = Base.metadata` &  `from app.database import Base`
    `from app.models import Files`

Cmd:
    alembic init alembic
    alembic revision --autogenerate -m "Added files table"
    alembic upgrade head