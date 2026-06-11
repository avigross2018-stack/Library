from db_connection import get_connection, create_tables
from pydantic import BaseModel


class NewBook(BaseModel):
    title:str
    author:str
    genre:str
    is_available:bool
    borrowed_by_member_id:int | None


class BookDB:

    GENRE = ('Fiction', 'Non-Fiction', 'Science', 'History', 'Other')
    create_tables()

    def __init__(self):
        pass


    def get_all_books(self) -> dict:
        """
        Load data from table books.
        return all the data in type dict.
        """
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
    

    def create_book(data: NewBook):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT INTO books (title, author, genre, is_available, borrowed_by_member_id)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (data.title, data.author, data.genre, data.is_available, data.borrowed_by_member_id))
            change = cursor.rowcount
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()
        return change > 0