import mysql.connector


def get_connection():
    try:
        return mysql.connector.connect(
        host="localhost",
        port=3310,
        user="root",
        password="root",
        database="library_db"
        )
    except Exception as e:
        raise e


def create_tables():
    con = get_connection()
    cur = con.cursor()
    cur.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id                      INT PRIMARY KEY AUTO_INCREMENT,
                title                   VARCHAR(50) NOT NULL,
                author                  VARCHAR(50) NOT NULL,
                genre                   ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other'),
                is_available            BOOLEAN,
                borrowed_by_member_id   INT DEFAULT NULL
                )
            ''')
    
    cur.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id              INT PRIMARY KEY AUTO_INCREMENT,
                name            VARCHAR(50) NOT NULL,
                email           VARCHAR(50) NOT NULL,
                is_active       BOOLEAN,
                total_borrows   INT 
                )
            ''')
    con.commit()
    cur.close()
    con.close()