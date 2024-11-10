# Tutorial 2 : Create enviroment variable and database connection string
## Install database library for postgresql
```
    pip install SQLAlchemy
    pip install psycopg2-binary
```
## Create ***config.py*** file and setting up environment variable
```
    import os

    # DB
    user = os.getenv('POSTGRES_USER','admin')
    password = os.getenv('POSTGRES_PASSWORD','P@ssw0rd')
    host = os.getenv('POSTGRES_HOST','178.128.118.126')
    database = os.getenv('POSTGRES_DB','syukur_db')
    port = os.getenv('POSTGRES_PORT','5432')

    DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
```
## Create file ***database.py***
```
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    import config, models

    SQLALCHEMY_DATABASE_URL = config.DATABASE_CONNECTION_URI

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={}
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def initial_db():
        models.Base.metadata.create_all(bind=engine)
```