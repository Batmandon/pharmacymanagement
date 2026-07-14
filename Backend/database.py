import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from config import DB_PASSWORD, DB_HOST, DB_PORT, DB_USER, DB_NAME

connection_pool = psycopg2.pool.SimpleConnectionPool(
    1,
    10,
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    dbname=DB_NAME
)

@contextmanager
def get_cursor():
    conn = connection_pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        connection_pool.putconn(conn)

def Create_database():
    try:
        with get_cursor() as cursor: 

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                name VARCHAR(20) NOT NULL,
                pharmacy_name VARCHAR(100) NOT NULL,
                email VARCHAR(50) NOT NULL, 
                password TEXT NOT NULL
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS products(
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id),
                medicine_name TEXT NOT NULL,
                batch_no TEXT NOT NULL,
                expiry_date DATE,
                quantity INT,
                price INT,
                expiry_status TEXT)
            """)
            # If you need to alter an existing table, use:
            # ALTER TABLE products ALTER COLUMN expiry_date TYPE DATE;

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders(
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id),
                product_id INT REFERENCES products(id),
                quantity INT,
                status TEXT)
                """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders_log(
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'sent',
                sent_via TEXT DEFAULT 'whatsapp',
                items JSONB)
            """)

            cursor.execute("""
            ALTER TABLE orders 
            ALTER COLUMN status SET DEFAULT 'Pending';""")
            
        
            # cursor.execute("""
            # ALTER TABLE products ALTER COLUMN expiry_date TYPE DATE;""")


            # cursor.execute("""
            # DELETE FROM orders WHERE user_id = 4;""" )
            
    except Exception as e:
        print(f" Database Error: {e}")       