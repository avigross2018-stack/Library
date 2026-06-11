from db_connection import get_connection, create_tables




class BookDB:

    GENRE = ('Fiction', 'Non-Fiction', 'Science', 'History', 'Other')
    create_tables()

    def __init__(self):
        pass


    def get_all_books(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM books')
            data = cursor.fetchall()

        except Exception as e:
            raise e
        
        finally:
            cursor.close()
            conn.close()

        return data