
import sqlite3


class DAO:
    def __init__(self,db_connection,query) -> None:
        self.query = query
        self.db_connection = db_connection
    def Get(self):
        if self.query:
            conn = sqlite3.connect(self.db_connection)  
            cur = conn.cursor()
            cur.execute(self.query)
            rows = cur.fetchall()
            return rows
        else: 
            return None