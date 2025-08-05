
"""
Database setup and data seeding script for ALX_prodev database.
"""

import mysql.connector
import csv
import uuid
from mysql.connector import Error


def connect_db():
    """
    Connects to the MySQL database server.
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.
    
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        cursor.close()
        print("Database ALX_prodev created successfully")
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields.
    
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """
    Inserts data from CSV file into the database if it does not exist.
    
    Args:
        connection: MySQL connection object
        csv_file: Path to the CSV file containing user data
    """
    try:
        cursor = connection.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print("Data already exists in the database")
            cursor.close()
            return
        
        # Read CSV file and insert data
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                # Validate UUID format
                try:
                    uuid.UUID(row['user_id'])
                except ValueError:
                    print(f"Invalid UUID format: {row['user_id']}")
                    continue
                
                # Insert data
                insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                """
                values = (row['user_id'], row['name'], row['email'], row['age'])
                
                try:
                    cursor.execute(insert_query, values)
                except Error as e:
                    print(f"Error inserting row {row['user_id']}: {e}")
                    continue
        
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
        
    except FileNotFoundError:
        print(f"CSV file {csv_file} not found")
    except Error as e:
        print(f"Error inserting data: {e}")


def stream_users(connection):
    """
    Generator function that streams rows from the user_data table one by one.
    
    Args:
        connection: MySQL connection object
    
    Yields:
        tuple: User data row (user_id, name, email, age)
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
        
        cursor.close()
    except Error as e:
        print(f"Error streaming users: {e}")


if __name__ == "__main__":
    # Test the functions
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()
        print("Connection successful")
        
        connection = connect_to_prodev()
        if connection:
            create_table(connection)
            insert_data(connection, 'user_data.csv')
            
            # Test the generator
            print("\nStreaming users:")
            for user in stream_users(connection):
                print(user)
            
            connection.close() 