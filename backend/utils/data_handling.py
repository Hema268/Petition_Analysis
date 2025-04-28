
import mysql.connector
from mysql.connector import Error
from database.db_connection import get_db_connection

def get_db_connection():
    """
    Establish a connection to the MySQL database.
    
    Returns:
        mysql.connector.connection: Database connection object.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def fetch_data(query, params=None):
    """
    Fetch data from the database.
    
    Args:
        query (str): SQL query to execute.
        params (tuple, optional): Parameters for the query. Defaults to None.
    
    Returns:
        list: List of rows fetched from the database.
    """
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    except Error as e:
        print(f"Error fetching data from database: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def insert_data(query, params):
    """
    Insert data into the database.
    
    Args:
        query (str): SQL query to execute.
        params (tuple): Parameters for the query.
    
    Returns:
        int: The ID of the inserted row (if applicable).
    """
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Error inserting data into database: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def update_data(query, params):
    """
    Update data in the database.
    
    Args:
        query (str): SQL query to execute.
        params (tuple): Parameters for the query.
    
    Returns:
        bool: True if the update was successful, False otherwise.
    """
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            return True
    except Error as e:
        print(f"Error updating data in database: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def delete_data(query, params):
    """
    Delete data from the database.
    
    Args:
        query (str): SQL query to execute.
        params (tuple): Parameters for the query.
    
    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            return True
    except Error as e:
        print(f"Error deleting data from database: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def fetch_petitions():
    """
    Fetch all petitions from the database.
    
    Returns:
        list: List of petitions.
    """
    query = "SELECT * FROM petitions"
    return fetch_data(query)

def insert_petition(title, content):
    """
    Insert a new petition into the database.
    
    Args:
        title (str): Title of the petition.
        content (str): Content of the petition.
    
    Returns:
        int: The ID of the inserted petition.
    """
    query = "INSERT INTO petitions (title, content) VALUES (%s, %s)"
    params = (title, content)
    return insert_data(query, params)

def update_petition_status(petition_id, status):
    """
    Update the status of a petition.
    
    Args:
        petition_id (int): ID of the petition.
        status (str): New status of the petition.
    
    Returns:
        bool: True if the update was successful, False otherwise.
    """
    query = "UPDATE petitions SET status = %s WHERE id = %s"
    params = (status, petition_id)
    return update_data(query, params)

def delete_petition(petition_id):
    """
    Delete a petition from the database.
    
    Args:
        petition_id (int): ID of the petition.
    
    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    query = "DELETE FROM petitions WHERE id = %s"
    params = (petition_id,)
    return delete_data(query, params)