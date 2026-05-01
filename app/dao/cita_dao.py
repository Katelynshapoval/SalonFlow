from config.db import Database
from app.models.cita import Cita


class CitaDAO:

    @staticmethod
    def crear_cita(id_cliente, id_servicio, id_empleado, fecha, hora):
        conn = Database.get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO citas (id_cliente, id_servicio, id_empleado, fecha, hora, estado)
        VALUES (%s, %s, %s, %s, %s, 'confirmada')
        """

        cursor.execute(query, (id_cliente, id_servicio, id_empleado, fecha, hora))
        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def obtener_citas_por_fecha(fecha):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM citas WHERE fecha = %s"
        cursor.execute(query, (fecha,))
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return [Cita(**row) for row in results]