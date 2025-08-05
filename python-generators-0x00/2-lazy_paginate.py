#!/usr/bin/python3
"""
Lazy pagination using generators.
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetches a page of users from the database.
    
    Args:
        page_size (int): Number of users to fetch per page
        offset (int): Offset for pagination
        
    Returns:
        list: List of user dictionaries
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """
    Generator function that implements lazy pagination.
    Only fetches the next page when needed at an offset of 0.
    
    Args:
        page_size (int): Number of users to fetch per page
        
    Yields:
        list: Page of user data rows
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # No more data to fetch
            break
        yield page
        offset += page_size 