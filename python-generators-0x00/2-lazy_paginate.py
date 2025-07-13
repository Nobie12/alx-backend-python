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

#Correctly fetch and return rows
def paginate_users(connection, page_size, offset):
    with connection.cursor(dictionary=True) as cursor:
        query = "SELECT * FROM users LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        rows = cursor.fetchall()  #actually gets the data
        return rows

# Lazy generator using one loop
def lazy_paginate(page_size):
    try:
        with mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        ) as connection:
            print("Successfully connected to the database")
            offset = 0

            while True:
                page = paginate_users(connection, page_size, offset)
                if not page:
                    break  # done
                yield page
                offset += page_size

    except mysql.connector.Error as err:
        print("Database error:", err)

