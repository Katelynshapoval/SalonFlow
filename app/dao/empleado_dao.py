from config.db import Database
from app.models.empleado import Empleado


class EmpleadoDAO:

    @staticmethod
    def obtener_empleados() -> list[Empleado]:
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM empleados ORDER BY nombre")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Empleado(**row) for row in results]

    @staticmethod
    def obtener_todos_texto() -> str:
        # Returns a text summary for AI context injection.
        empleados = EmpleadoDAO.obtener_empleados()
        return "\n".join(
            f"- {e.nombre} (especialidad: {e.especialidad})"
            for e in empleados
        )
