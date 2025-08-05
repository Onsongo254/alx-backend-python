#!/usr/bin/python3
"""
Memory-efficient aggregation using generators.
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


def stream_user_ages():
    """
    Generator function that streams user ages one by one.
    
    Yields:
        int: User age
    """
    connection = connect_to_prodev()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        
        for row in cursor:
            yield row[0]
        
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error streaming user ages: {e}")
        if connection:
            connection.close()


def calculate_average_age():
    """
    Calculates the average age of users using the generator.
    Does not load the entire dataset into memory.
    """
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age}")
    else:
        print("No users found")


if __name__ == "__main__":
    calculate_average_age() 