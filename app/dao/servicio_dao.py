from config.db import Database
from app.models.servicio import Servicio


class ServicioDAO:

    @staticmethod
    def obtener_servicios() -> list[Servicio]:
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM servicios ORDER BY nombre")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Servicio(**row) for row in results]

    @staticmethod
    def obtener_por_id(id_servicio: int) -> Servicio | None:
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM servicios WHERE id_servicio = %s", (id_servicio,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return Servicio(**row) if row else None

    @staticmethod
    def obtener_todos_texto() -> str:
        """Returns a text summary for AI context injection."""
        servicios = ServicioDAO.obtener_servicios()
        return "\n".join(
            f"- {s.nombre}: {s.precio}€, {s.duracion_minutos} min. {s.descripcion}"
            for s in servicios
        )
