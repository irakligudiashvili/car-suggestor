from dotenv import load_dotenv
import os
import psycopg2
from generator import generate

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('HOST'),
    dbname=os.getenv('DBNAME'),
    user=os.getenv('USER'),
    port=os.getenv('PORT'),
    password=os.getenv('PASSWORD')
)

cur = conn.cursor()

cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS cars(
        brand VARCHAR(255),
        year INT,
        drive_type VARCHAR(255),
        transmission VARCHAR(255),
        fuel_type VARCHAR(255),
        steering_side VARCHAR(255),
        seats INT,
        pros TEXT[],
        description TEXT,
        img_url TEXT,
        price INT
    )
    '''
)


# generate()

conn.commit()
cur.close()
conn.close()