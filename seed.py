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

path = user_data.csv

def insert_data(connection, path):
    try:
        cursor = connection.cursor()
        with open(path, 'r') as f:
            reader = csv.DictReader(path)
            inserted_count = 0
            skipped_count = 0

            for row in reader:
                try:
                    #exctract fields safely
                    name = row.get('name', '').strip()
                    email = row.get('email', '').strip()
                    age_str = row.get('age', '').strip()

                    #convert age safley
                    age = Decimal(age_str)

                    #generate unique user_id
                    user_id = str(uuid.uuid4())

                    #insert into database
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                        """,(user_id, name, email, age))

                        inserted_count += 1

                except Error as e:
                    print(f"Skipped row: {row} - Reason: {e}")

                    skipped_count += 1

            connection.commit()
            print(f"Inserted {inserted_count} records succefully")
            print(f"Skipped {skipped_count} bad records")


            except FileNotFoundError:
                print(f"CSV fil {path} not found.")
            except mysql.connector.Error as e:
                print('Database error during insertion: {e}')
            
            finally:
                if cursor:
                    cursor.close()
