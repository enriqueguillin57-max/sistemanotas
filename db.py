import pymysql
from dbutils.pooled_db import PooledDB

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",          # en XAMPP por defecto va vacío
    "database": "sistema_notas",
    "port": 3306,
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}

pool = PooledDB(creator=pymysql, maxconnections=10, **DB_CONFIG)


def get_connection():
    """Devuelve una conexión del pool."""
    return pool.connection()


def ejecutar(query, params=None, fetch="all"):
    """
    Helper genérico.
    fetch: 'all' | 'one' | 'none'
    Devuelve filas, una fila o el id insertado / filas afectadas.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            if fetch == "all":
                return cursor.fetchall()
            if fetch == "one":
                return cursor.fetchone()
            conn.commit()
            return cursor.lastrowid or cursor.rowcount
