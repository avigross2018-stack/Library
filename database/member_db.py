from database.db_connection import DBConnection
from pydantic import BaseModel

db_conn = DBConnection()

class NewMember(BaseModel):
    name:str
    email:str
    is_active:bool
    total_borrows:int


class UpdateMember(BaseModel):
    name:str | None = None
    email:str | None = None
    is_active:bool | None = None
    total_borrows:int | None = None


class MemberDB:
    def __init__(self):
        pass

    def  get_all_members(self):
        try:
            conn = db_conn.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM members')
            data = cursor.fetchall()

        except Exception as e:
            raise e
        
        finally:
            cursor.close()
            conn.close()

        return data       


    def create_member(self, new_member: NewMember):
        try:
            conn = db_conn.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT INTO members (name, email, is_active, total_borrows)
                        VALUES (%s, %s, %s, %s)
                    """, (new_member.name, new_member.email, new_member.is_active, new_member.total_borrows))
            conn.commit()
            change = cursor.rowcount
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()
        return change > 0


    def get_member_by_id(self, member_id: int):
        try:
            con = db_conn.get_connection()
            cur = con.cursor(dictionary=True)
            cur.execute("""
                    SELECT * FROM members WHERE id = %s
                    """, (member_id,))
            data = cur.fetchone()
        except Exception as e:
            raise e
        finally:
            cur.close()
            con.close()
        return data


    def update_member(self, member_id: int, data: dict):
        if not data:
            raise Exception
        con = db_conn.get_connection()
        cur = con.cursor()
        try:
            keys = [f"{k} = %s" for k in data]
            values = list(data.values())
            values.append(member_id)
            data_clause = ", ".join(keys)
            
            cur.execute(f"UPDATE members SET {data_clause} WHERE id = %s ", tuple(values))
            count = cur.rowcount
            con.commit()
        except Exception as e:
            raise e    
        finally:
            cur.close()
            con.close()
        return count > 0


    def deactivate_member(self, member_id: int):
        con = db_conn.get_connection()
        cur = con.cursor()
        try:
            cur.execute('''UPDATE members SET is_active = FALSE WHERE id = %s''',
                        (member_id,))
            con.commit()
            change = cur.rowcount
        except Exception as e:
            raise e    
        finally:
            cur.close()
            con.close()
        return change > 0


    def  activate_member(self, member_id: int):
        con = db_conn.get_connection()
        cur = con.cursor()
        try:
            cur.execute('''UPDATE members SET is_active = TRUE WHERE id = %s''',
                        (member_id,))
            con.commit()
            change = cur.rowcount
        except Exception as e:
            raise e    
        finally:
            cur.close()
            con.close()
        return change > 0


    def increment_borrows(self, member_id: int):
        c_member = self.get_member_by_id(member_id)["total_borrows"] + 1
        self.update_member(member_id, {"total_borrows": c_member})


    def count_active_members(self):
        con = db_conn.get_connection()
        cur = con.cursor(dictionary=True)
        try:
            cur.execute('''SELECT COUNT(*) AS active_members FROM members WHERE is_active = TRUE''',
                        )
            data = cur.fetchone()
            
        except Exception as e:
            raise e
        finally:
            cur.close()
            con.close()
        return data


    def get_top_member(self):
        con = db_conn.get_connection()
        cur = con.cursor(dictionary=True)
        try:
            cur.execute('''SELECT * from members
                        ORDER BY total_borrows DESC
                        LIMIT 1'''
                        )
            data = cur.fetchone()
            
        except Exception as e:
            raise e
        finally:
            cur.close()
            con.close()
        return data