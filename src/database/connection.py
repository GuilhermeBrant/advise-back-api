import pyodbc
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

server = os.getenv("db_host")
database = os.getenv("db_name")
username = os.getenv("db_user")
password = os.getenv("db_password")

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='
    +str(server)
    +';DATABASE='
    +str(database)
    +';UID='
    +str(username)
    +';PWD='
    +str(password)
)
cursor = conn.cursor()
