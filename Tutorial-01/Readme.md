# Setup virtual enviroment and install fastapi package
## Create python virtual enviroment
```
    python -m venv env
```
## Activate a virtual environment
```
    .\env\Scripts\activate
```
## Upgrade python installer package
```
    python -m pip install --upgrade pip
```
## Install fastapi package
```
    pip install fastapi[standard]
```
## Create working directory **app**
```
    .\Tutorial-01\app
```
## Create new file ***main.py*** and insert code below and save
```
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    def index():
        return {"message":"Hello World"}
```
## run the code
```
    fastapi dev main.py
```
## access api 
```
    http://localhost:8000
```
## access api document
```
    http://localhost:8000/docs
```
