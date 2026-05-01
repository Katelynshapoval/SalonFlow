from config.db import Database
from app.models.cliente import Cliente


class ClienteDAO:

    @staticmethod
    def crear_cliente(nombre, telefono, email):
        conn = Database.get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO clientes (nombre, telefono, email)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (nombre, telefono, email))
        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def obtener_cliente_por_telefono(telefono):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM clientes WHERE telefono = %s"
        cursor.execute(query, (telefono,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return Cliente(**result)
        return None