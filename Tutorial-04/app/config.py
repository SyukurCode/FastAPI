import os

# DB
user = os.getenv('POSTGRES_USER','admin')
password = os.getenv('POSTGRES_PASSWORD','qwe123***')
host = os.getenv('POSTGRES_HOST','172.20.6.217')
database = os.getenv('POSTGRES_DB','demo')
port = os.getenv('POSTGRES_PORT','5432')

DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

# SECURITY
secret_key = os.getenv("SECRET_KEY","pnvKO27wy2JXYnuyDoNQq9srvAIzxgNcQQ")
alogrithm = os.getenv("ALOGORITHM","HS256")
token_expired = float(os.getenv("TOKEN_EXPIRED_IN_MINUSTES",30)) # convert value from int to float
