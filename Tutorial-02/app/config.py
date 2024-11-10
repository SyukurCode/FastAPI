import os

# DB
user = os.getenv('POSTGRES_USER','admin')
password = os.getenv('POSTGRES_PASSWORD','P@ssw0rd')
host = os.getenv('POSTGRES_HOST','178.128.118.126')
database = os.getenv('POSTGRES_DB','syukur_db')
port = os.getenv('POSTGRES_PORT','5432')

DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'