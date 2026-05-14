from app.models.empleado import Empleado
from config.db import Database


class EmpleadoDAO:
    # Get all employees ordered by name
    @staticmethod
    def obtener_empleados() -> list[Empleado]:
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM empleados ORDER BY nombre")

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return [Empleado(**row) for row in results]

    # Get all employees as text for assistant context
    @staticmethod
    def obtener_todos_texto() -> str:
        empleados = EmpleadoDAO.obtener_empleados()

        return "\n".join(
            f"- {e.nombre} (especialidad: {e.especialidad})"
            for e in empleados
        )