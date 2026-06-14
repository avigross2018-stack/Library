from database.db_connection import get_connection, create_tables
from pydantic import BaseModel


class NewBook(BaseModel):
    title:str
    author:str
    genre:str
    is_available:bool
    borrowed_by_member_id:int | None = None


class UpdateBook(BaseModel):
    title:str | None = None
    author:str | None = None
    genre:str | None = None
    is_available:bool | None = None
    borrowed_by_member_id:int | None = None



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
    

    def create_book(self, data: NewBook):
        '''
        arg data: get NewBook basemodel.
        return bool if data created.
        '''
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT INTO books (title, author, genre, is_available, borrowed_by_member_id)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (data.title, data.author, data.genre, data.is_available, data.borrowed_by_member_id))
            conn.commit()
            change = cursor.rowcount
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()
        return change > 0
    

    def get_book_by_id(self, book_id: int) -> dict:
        '''
        search in the db book by ID.
        return the book in dict.
        '''
        try:
            con = get_connection()
            cur = con.cursor(dictionary=True)
            cur.execute("""
                    SELECT * FROM books WHERE id = %s
                    """, (book_id,))
            data = cur.fetchone()
        except Exception as e:
            raise e
        finally:
            cur.close()
            con.close()
        return data
    

    def update_book_info(self, book_id: int, data: dict):
        if not data:
            raise Exception
        con = get_connection()
        cur = con.cursor()
        try:
            keys = [f"{k} = %s" for k in data]
            values = list(data.values())
            values.append(book_id)
            data_clause = ", ".join(keys)
            
            cur.execute(f"UPDATE books SET {data_clause} WHERE id = %s ", tuple(values))
            count = cur.rowcount
            con.commit()
        except Exception as e:
            raise e    
        finally:
            cur.close()
            con.close()
        return count > 0


    def set_available(self, book_id: int, val: bool, member_id: int):
        update_data = {"is_available": val,
                  "borrowed_by_member_id": member_id}
        self.update_book_info(book_id, update_data)

    
    def count_total_books(self):
        con = get_connection()
        cur = con.cursor(dictionary=True)
        try:
            cur.execute('''SELECT *, COUNT(*) FROM books''')
            data = cur.fetchall()
            
        except Exception as e:
            raise e
        finally:
            cur.close()
            con.close()
        return data