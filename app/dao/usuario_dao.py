from config.db import Database


class UsuarioDAO:

    @staticmethod
    def obtener_por_telegram_id(telegram_id: int) -> dict | None:
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE telegram_id = %s", (telegram_id,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario

    @staticmethod
    def crear_usuario(telegram_id: int, username: str) -> None:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (telegram_id, username, registrado) VALUES (%s, %s, FALSE)",
            (telegram_id, username),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def completar_registro(telegram_id: int, nombre: str, telefono: str, email: str) -> None:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE usuarios
            SET nombre = %s, telefono = %s, email = %s, registrado = TRUE
            WHERE telegram_id = %s
            """,
            (nombre, telefono, email, telegram_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def obtener_id_usuario(telegram_id: int) -> int | None:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_usuario FROM usuarios WHERE telegram_id = %s", (telegram_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else None

    @staticmethod
    def usuario_registrado(telegram_id: int) -> bool:
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT registrado FROM usuarios WHERE telegram_id = %s", (telegram_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return bool(result and result[0])
