import psycopg2

BASE_URL = "localhost:5000/api"

def db_connection():
    conn = psycopg2.connect(
        host = "localhost",
        port = "5432",
        user = "postgres",
        password = "toor",
        database = "db_logistics"
    )
   
    return conn

