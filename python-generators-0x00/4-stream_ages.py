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


def stream_user_ages():
    try:
        with mysql.connector.connect(
                    host = DB_HOST,
                    user = DB_USER,
                    password = DB_PASSWORD,
                    database = DB_NAME
                ) as connection:
            print("Successfully connected to the database")

            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(f"SELECT age FROM user_data")
                for age_row in cursor:
                    yield age_row['age']
    
    except mysql.connector.Error as e:
        print(f"Database Error: {e}")


def age_average():
    total = 0
    count = 0
    for age_value in stream_user_ages():
        total += age_value
        count += 1

    if count == 0:
        print("No user ages found in the database to calculate average.")
        return None
    else:
        return total / count
