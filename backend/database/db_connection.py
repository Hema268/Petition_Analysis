import mysql.connector
from config.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

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
        if connection.is_connected():
            print("✅ Connected to MySQL Database")
        return connection
    except Exception as e:
        print(f"Error connecting to MySQL database: {e}")
        return None
        