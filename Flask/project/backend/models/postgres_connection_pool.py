import os
import time
import psycopg2
from psycopg2 import pool
import dotenv

# Cargar variables de entorno
dotenv.load_dotenv()

dbconfig = {
    "user": os.environ.get('DB_USER', 'postgres'),
    "password": os.environ.get('DB_PASSWORD', ''),
    "host": os.environ.get('DB_HOST', '127.0.0.1'),
    "port": os.environ.get('DB_PORT', '5432'),
    "database": os.environ.get('DB_NAME', 'author_books2')
}

class PostgreSQLPool:
    def __init__(self):
        self.pool = self.create_pool(minconn=1, maxconn=3)
    
    def create_pool(self, minconn, maxconn):
        return pool.SimpleConnectionPool(minconn, maxconn, **dbconfig)
    
    def close(self, conn, cursor):
        cursor.close()
        self.pool.putconn(conn)
    
    def execute(self, sql, args=None, commit=False):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        
        if commit:
            conn.commit()
            lastrowid = cursor.fetchone()[0] if "RETURNING" in sql.upper() else None
            self.close(conn, cursor)
            return lastrowid
        else:
            res = cursor.fetchall()
            self.close(conn, cursor)
            return res
    
    def executemany(self, sql, args, commit=False):
        conn = self.pool.getconn()
        cursor = conn.cursor()
        cursor.executemany(sql, args)
        
        if commit:
            conn.commit()
            self.close(conn, cursor)
            return None
        else:
            res = cursor.fetchall()
            self.close(conn, cursor)
            return res

if __name__ == "__main__":
    pg_pool = PostgreSQLPool()
    sql = "SELECT * FROM libros"
    rv = pg_pool.execute(sql)
    for result in rv:
        print(result)
    print("done")