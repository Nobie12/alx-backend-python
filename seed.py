#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
import uuid
import csv
from decimal import Decimal
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def connect_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print('Successfully connected to the MySQL server.')
        return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        connection.commit()
        print(f"Database '{DB_NAME}' ensured.")
    except Error as e:
        print(f"Error creating database: {e}")
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
        print(f"Connected to database '{DB_NAME}'.")
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(5, 2) NOT NULL
            )
        """)
        connection.commit()
        print("Table 'user_data' ensured.")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        if cursor:
            cursor.close()

path = 'user_data.csv'

def insert_data(connection, path):
    try:
        cursor = connection.cursor()
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            inserted_count = 0
            skipped_count = 0

            for row in reader:
                try:
                    name = row.get('name', '').strip()
                    email = row.get('email', '').strip()
                    age_str = row.get('age', '').strip()

                    age = Decimal(age_str) if age_str else Decimal('0.00')

                    user_id = str(uuid.uuid4())

                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, name, email, age))

                    inserted_count += 1

                except Exception as e:
                    print(f"Skipped row: {row} - Reason: {e}")
                    skipped_count += 1

            connection.commit()
            print(f"Inserted {inserted_count} records successfully.")
            print(f"Skipped {skipped_count} bad records.")

    except FileNotFoundError:
        print(f"CSV file '{path}' not found.")
    except mysql.connector.Error as e:
        print(f'Database error during insertion: {e}')
    finally:
        if cursor:
            cursor.close()
