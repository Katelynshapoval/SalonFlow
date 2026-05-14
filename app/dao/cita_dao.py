from datetime import datetime, timedelta
from config.db import Database
from app.models.cita import Cita


def _td_to_str(td) -> str:
    """Convert MySQL TIME (timedelta) or time object to HH:MM string."""
    if isinstance(td, timedelta):
        total = int(td.total_seconds())
        h, rem = divmod(total, 3600)
        m = rem // 60
        return f"{h:02d}:{m:02d}"
    return td.strftime("%H:%M")


class CitaDAO:

    @staticmethod
    def obtener_citas_futuras(id_usuario: int) -> list[Cita]:
        """Returns all confirmed/pending future appointments for a user."""
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT c.id_cita, c.id_usuario, c.id_servicio, c.id_empleado,
                   c.fecha, c.hora, c.estado,
                   s.nombre AS nombre_servicio,
                   e.nombre AS nombre_empleado
            FROM citas c
            JOIN servicios s ON c.id_servicio = s.id_servicio
            JOIN empleados e ON c.id_empleado = e.id_empleado
            WHERE c.id_usuario = %s
              AND c.fecha >= CURDATE()
              AND c.estado != 'cancelada'
            ORDER BY c.fecha, c.hora
            """,
            (id_usuario,),
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        citas = []
        for row in rows:
            citas.append(
                Cita(
                    id_cita=row["id_cita"],
                    id_usuario=row["id_usuario"],
                    id_servicio=row["id_servicio"],
                    id_empleado=row["id_empleado"],
                    fecha=row["fecha"],
                    hora=_td_to_str(row["hora"]),
                    estado=row["estado"],
                    nombre_servicio=row["nombre_servicio"],
                    nombre_empleado=row["nombre_empleado"],
                )
            )
        return citas

    @staticmethod
    def crear_cita(
        id_usuario: int,
        id_servicio: int,
        id_empleado: int,
        fecha: str,
        hora: str,
    ) -> int | None:
        """Inserts a new cita. Returns the new id_cita, or None on failure."""
        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO citas (id_usuario, id_servicio, id_empleado, fecha, hora, estado)
                VALUES (%s, %s, %s, %s, %s, 'confirmada')
                """,
                (id_usuario, id_servicio, id_empleado, fecha, hora),
            )
            conn.commit()
            return cursor.lastrowid
        except Exception:
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def cancelar_cita(id_cita: int, id_usuario: int) -> bool:
        """Sets cita status to 'cancelada'. Returns True on success."""
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE citas SET estado = 'cancelada'
            WHERE id_cita = %s AND id_usuario = %s AND estado != 'cancelada'
            """,
            (id_cita, id_usuario),
        )
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected > 0

    @staticmethod
    def hay_conflicto(id_empleado: int, fecha: str, hora: str) -> bool:
        """Returns True if the employee already has a confirmed booking at that slot."""
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM citas
            WHERE id_empleado = %s AND fecha = %s AND hora = %s AND estado = 'confirmada'
            """,
            (id_empleado, fecha, hora),
        )
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count > 0
