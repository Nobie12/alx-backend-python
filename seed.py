#!/usr/bin/python3

import mysql.connector
from contextlib import contextmanager
import uuid
import csv
from dotenv import load_dotenv
import os

#load environment variables
load_dotenv()

DB_HOST=os.getenv('DB_HOST')
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_NAME=os.getenv('DB_NAME')

def connect_db():
    try:
        connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD
            )
        print('succefully connected to the Database')
        return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return none

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        connection.commit()
        print(f"Database {DB_NAME} ensured")

    except Error as e:
        print(f"Error creating Database: {e}")

    finally:
        if cursor:
            cursor.close()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
        print(f"connected to Database {DB_NAME}")
        return connection

    except Error as e:
        print(f"Error connecting to Database")
        return none


def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARACHAR(26) NOT NULL,
                email VARCHAR(26) NOT NULL,
                age BECIMAL(5,2) NOT NULL
            )
        """)
        connection.commit()
        print("Table 'user_data' ensured")

    except Error as e:
        print(f"Error creating table: {e}")

    finally:
        if cursor:
            cursor,close()

def insert_data(connection, data)
