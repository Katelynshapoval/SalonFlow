from config.db import Database


class UsuarioDAO:
    # Get a user by their telegram id
    @staticmethod
    def obtener_por_telegram_id(telegram_id: int) -> dict | None:
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios WHERE telegram_id = %s", (telegram_id,))

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        return usuario

    # Create a new unregistered user
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

    # Complete the user's registration data
    @staticmethod
    def completar_registro(
        telegram_id: int, nombre: str, telefono: str, email: str
    ) -> None:
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

    # Get the internal user id from a telegram id
    @staticmethod
    def obtener_id_usuario(telegram_id: int) -> int | None:
        conn = Database.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id_usuario FROM usuarios WHERE telegram_id = %s",
            (telegram_id,),
        )

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result[0] if result else None

    # Check whether a user has completed registration
    @staticmethod
    def usuario_registrado(telegram_id: int) -> bool:
        conn = Database.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT registrado FROM usuarios WHERE telegram_id = %s",
            (telegram_id,),
        )

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return bool(result and result[0])