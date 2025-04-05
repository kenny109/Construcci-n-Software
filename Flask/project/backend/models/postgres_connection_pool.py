import time
import psycopg2
from psycopg2 import pool
import configparser

config = configparser.ConfigParser()
config.read('C:\\Users\\kenny\\Construcci-n-Software\\Flask\\postgres_config.ini')
dbconfig = {
    "user": config.get('postgres', 'user'),
    "password": config.get('postgres', 'pass'),
    "host": config.get('postgres', 'host'),
    "port": config.get('postgres', 'port'),
    "database": config.get('postgres', 'database')
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
            self.close(conn, cursor)
            return cursor
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
    sql = "SELECT * FROM tasks"
    rv = pg_pool.execute(sql)
    for result in rv:
        print(result)
    print("done")
