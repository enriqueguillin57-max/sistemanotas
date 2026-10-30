import mysql.connector
from mysql.connector import Error

# =========================================
# Configuración de conexión a XAMPP (MySQL)
# =========================================
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",  # en XAMPP por defecto va vacío
    "database": "sistema_notas",
    "charset": "utf8mb4",
    "use_pure": True,
}


def get_connection():
    """Devuelve una conexión nueva a la base de datos."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise


def ejecutar_consulta(query, params=None, fetchone=False, fetchall=False, commit=False):
    """
    Ejecuta una consulta de forma segura (consultas parametrizadas).

    fetchone  -> devuelve una sola fila (dict)
    fetchall  -> devuelve lista de filas (dict)
    commit    -> para INSERT / UPDATE / DELETE, devuelve lastrowid
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    resultado = None
    try:
        cursor.execute(query, params or ())
        if fetchone:
            resultado = cursor.fetchone()
        elif fetchall:
            resultado = cursor.fetchall()
        elif commit:
            conn.commit()
            resultado = cursor.lastrowid
    except Error as e:
        conn.rollback()
        print(f"Error en la consulta: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
    return resultado
