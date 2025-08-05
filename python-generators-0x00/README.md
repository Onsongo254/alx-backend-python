# Python Generators - Database Streaming

This project demonstrates the use of Python generators to stream data from a MySQL database. The main objective is to create a generator that streams rows from an SQL database one by one.

## Project Structure

- `seed.py` - Main script containing database setup and generator functions
- `user_data.csv` - Sample data file with user information
- `0-main.py` - Test script to demonstrate the functionality
- `README.md` - This documentation file

## Database Schema

The project sets up a MySQL database named `ALX_prodev` with a table `user_data` containing:

- `user_id` (VARCHAR(36), Primary Key, Indexed) - UUID format
- `name` (VARCHAR(255), NOT NULL) - User's full name
- `email` (VARCHAR(255), NOT NULL) - User's email address
- `age` (DECIMAL(3,0), NOT NULL) - User's age

## Functions

### `connect_db()`
Connects to the MySQL database server.

### `create_database(connection)`
Creates the database `ALX_prodev` if it does not exist.

### `connect_to_prodev()`
Connects to the `ALX_prodev` database in MySQL.

### `create_table(connection)`
Creates a table `user_data` if it does not exist with the required fields.

### `insert_data(connection, data)`
Inserts data from CSV file into the database if it does not exist.

### `stream_users(connection)`
Generator function that streams rows from the `user_data` table one by one.

## Usage

1. Ensure MySQL server is running
2. Install required dependencies:
   ```bash
   pip install mysql-connector-python
   ```
3. Run the test script:
   ```bash
   python3 0-main.py
   ```

## Requirements

- Python 3.x
- MySQL server
- mysql-connector-python package

## Example Output

```
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ...]
``` 