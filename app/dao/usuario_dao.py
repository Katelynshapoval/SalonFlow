from config.db import Database


class UsuarioDAO:

    @staticmethod
    def obtener_por_telegram_id(telegram_id: int):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM usuarios WHERE telegram_id = %s"
        cursor.execute(query, (telegram_id,))
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        return usuario

    @staticmethod
    def crear_usuario(telegram_id: int, username: str):
        conn = Database.get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO usuarios (telegram_id, username, registrado)
        VALUES (%s, %s, FALSE)
        """

        cursor.execute(query, (telegram_id, username))
        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def completar_registro(telegram_id: int, nombre: str, telefono: str, email: str):
        conn = Database.get_connection()
        cursor = conn.cursor()

        query = """
        UPDATE usuarios
        SET nombre = %s,
            telefono = %s,
            email = %s,
            registrado = TRUE
        WHERE telegram_id = %s
        """

        cursor.execute(query, (nombre, telefono, email, telegram_id))
        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def obtener_id_usuario(telegram_id: int):
        conn = Database.get_connection()
        cursor = conn.cursor()

        query = "SELECT id_usuario FROM usuarios WHERE telegram_id = %s"
        cursor.execute(query, (telegram_id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return result[0]
        return None

    @staticmethod
    def usuario_registrado(telegram_id: int):
        conn = Database.get_connection()
        cursor = conn.cursor()

        query = "SELECT registrado FROM usuarios WHERE telegram_id = %s"
        cursor.execute(query, (telegram_id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return result[0] == 1
        return False