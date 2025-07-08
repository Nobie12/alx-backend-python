#!/usr/bin/python3


import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def stream_users():
    try:
        with mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            ) as connection:
            print('Succefully connected to the MySQL server.')

            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(f"SELECT * FROM user_data")
                for row in cursor:
                    yield row

    except mysql.connector.Error as e:
        print(f"Dtatabase Error: {e}")
