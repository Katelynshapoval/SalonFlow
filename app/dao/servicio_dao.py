from app.models.servicio import Servicio
from config.db import Database


class ServicioDAO:
    # Get all services ordered by name
    @staticmethod
    def obtener_servicios() -> list[Servicio]:
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM servicios ORDER BY nombre")

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return [Servicio(**row) for row in results]

    # Get one service by its id
    @staticmethod
    def obtener_por_id(id_servicio: int) -> Servicio | None:
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM servicios WHERE id_servicio = %s", (id_servicio,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return Servicio(**row) if row else None

    # Get all services as text for assistant context
    @staticmethod
    def obtener_todos_texto() -> str:
        servicios = ServicioDAO.obtener_servicios()

        return "\n".join(
            f"- {s.nombre}: {s.precio}€, {s.duracion_minutos} min. {s.descripcion}"
            for s in servicios
        )