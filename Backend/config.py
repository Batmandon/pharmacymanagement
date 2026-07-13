import os 
from dotenv import load_dotenv


load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER", "postgres")
DB_NAME = os.getenv("DB_NAME", "postgres")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")