from config.db import Database
from app.models.servicio import Servicio


class ServicioDAO:

    @staticmethod
    def obtener_servicios():
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM servicios")
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return [Servicio(**row) for row in results]