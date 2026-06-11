import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3310,
        user="root",
        password="root",
        database="library_db"
    )
