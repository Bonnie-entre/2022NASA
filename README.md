#TODO
* frontend page
    - main page (maybe combine with other) with upload(only in main page?) & search(右上 in header)
    - upload page => show page
    - search page
* change to_chart, make sure pic show

* show both output_keyword & output_keyword_float
* migrate file_title, picture 只有一張?
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