import mysql.connector





class DBConnection:
    def __init__(self):
        self.host="localhost"
        self.port=3310
        self.user="root"
        self.password="root"
        self.database="library_db"


    def get_connection(self):
        try:
            return mysql.connector.connect(
            host=self.host, 
            port=self.port, 
            user=self.user, 
            password=self.password, 
            database=self.database
            )
        except Exception as e:
            raise e


    def create_tables(self):
        con = self.get_connection()
        cur = con.cursor()
        cur.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id                      INT PRIMARY KEY AUTO_INCREMENT,
                    title                   VARCHAR(50) NOT NULL,
                    author                  VARCHAR(50) NOT NULL,
                    genre                   ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other'),
                    is_available            BOOLEAN DEFAULT TRUE NOT NULL,
                    borrowed_by_member_id   INT DEFAULT NULL
                    )
                ''')
        
        cur.execute('''
                CREATE TABLE IF NOT EXISTS members (
                    id              INT PRIMARY KEY AUTO_INCREMENT,
                    name            VARCHAR(50) NOT NULL,
                    email           VARCHAR(50) UNIQUE NOT NULL,
                    is_active       BOOLEAN NOT NULL,
                    total_borrows   INT NOT NULL
                    )
                ''')
        con.commit()
        cur.close()
        con.close()