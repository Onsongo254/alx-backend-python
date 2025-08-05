#!/usr/bin/python3
"""
Batch processing for large data using generators.
"""

import mysql.connector
from mysql.connector import Error


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


def stream_users_in_batches(batch_size):
    """
    Generator function that streams rows from the user_data table in batches.
    
    Args:
        batch_size (int): Number of rows to fetch in each batch
        
    Yields:
        list: Batch of user data rows, each with user_id, name, email, and age keys
    """
    connection = connect_to_prodev()
    if not connection:
        return
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) >= batch_size:
                yield batch
                batch = []
        
        # Yield any remaining rows in the last batch
        if batch:
            yield batch
        
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error streaming users in batches: {e}")
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25.
    
    Args:
        batch_size (int): Number of rows to process in each batch
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user) 