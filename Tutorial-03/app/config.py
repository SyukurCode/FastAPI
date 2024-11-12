import os

# DB
user = os.getenv('POSTGRES_USER','admin')
password = os.getenv('POSTGRES_PASSWORD','qwe123***')
host = os.getenv('POSTGRES_HOST','localhost')
database = os.getenv('POSTGRES_DB','fastapi')
port = os.getenv('POSTGRES_PORT','5432')

DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'