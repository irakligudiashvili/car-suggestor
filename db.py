import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_all_cars():
    conn = psycopg2.connect(
        host=os.getenv('HOST'),
        dbname=os.getenv('DBNAME'),
        user=os.getenv('USER'),
        port=os.getenv('PORT'),
        password=os.getenv('PASSWORD')
    )

    cur = conn.cursor()

    cur.execute("SELECT * FROM cars")

    cars = cur.fetchall()

    cur.close()
    conn.close()

    return cars