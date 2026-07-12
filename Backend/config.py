import os 
from dotenv import load_dotenv


load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_NAME = "postgres"
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")