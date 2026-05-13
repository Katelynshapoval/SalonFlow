from config.db import Database


class SolicitudContactoDAO:

    @staticmethod
    def crear_solicitud(id_usuario: int, mensaje: str = "Solicitud de atención humana") -> bool:
        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO solicitudes_contacto (id_usuario, mensaje) VALUES (%s, %s)",
                (id_usuario, mensaje),
            )
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
