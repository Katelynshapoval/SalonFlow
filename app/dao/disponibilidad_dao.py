from datetime import datetime, timedelta

from config.db import Database


# Convert a database time value into an hour and minute tuple
def _td_to_time(td) -> tuple[int, int]:
    if isinstance(td, timedelta):
        total = int(td.total_seconds())
        h, rem = divmod(total, 3600)
        m = rem // 60
        return h, m

    return td.hour, td.minute


class DisponibilidadDAO:
    # Get available appointment slots for a service
    @staticmethod
    def obtener_slots_disponibles(
        id_servicio: int, dias_adelante: int = 14
    ) -> list[dict]:
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        # Get the service duration
        cursor.execute(
            "SELECT duracion_minutos FROM servicios WHERE id_servicio = %s",
            (id_servicio,),
        )

        svc = cursor.fetchone()

        if not svc:
            cursor.close()
            conn.close()
            return []

        duracion = svc["duracion_minutos"]

        # Get future employee availability
        cursor.execute(
            """
            SELECT d.id_empleado, e.nombre AS empleado_nombre,
                   d.fecha, d.hora_inicio, d.hora_fin
            FROM disponibilidad_empleado d
            JOIN empleados e ON d.id_empleado = e.id_empleado
            WHERE d.fecha BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL %s DAY)
              AND d.disponible = TRUE
            ORDER BY d.fecha, d.hora_inicio
            """,
            (dias_adelante,),
        )

        disponibilidades = cursor.fetchall()

        # Get confirmed appointments in the same date range
        cursor.execute(
            """
            SELECT id_empleado, fecha, hora FROM citas
            WHERE fecha >= CURDATE() AND estado = 'confirmada'
            """
        )

        citas = cursor.fetchall()

        cursor.close()
        conn.close()

        booked: set[tuple] = set()

        # Store booked slots for quick lookup
        for c in citas:
            h_c, m_c = _td_to_time(c["hora"])
            hora_str = f"{h_c:02d}:{m_c:02d}"
            booked.add((c["id_empleado"], str(c["fecha"]), hora_str))

        slots: list[dict] = []

        # Split each availability window into service-sized slots
        for disp in disponibilidades:
            fecha = disp["fecha"]
            h_ini, m_ini = _td_to_time(disp["hora_inicio"])
            h_fin, m_fin = _td_to_time(disp["hora_fin"])

            inicio = datetime(fecha.year, fecha.month, fecha.day, h_ini, m_ini)
            fin = datetime(fecha.year, fecha.month, fecha.day, h_fin, m_fin)

            current = inicio

            while current + timedelta(minutes=duracion) <= fin:
                hora_str = current.strftime("%H:%M")
                fecha_str = str(fecha)

                if (disp["id_empleado"], fecha_str, hora_str) not in booked:
                    slots.append(
                        {
                            "id_empleado": disp["id_empleado"],
                            "empleado_nombre": disp["empleado_nombre"],
                            "fecha": fecha_str,
                            "hora": hora_str,
                        }
                    )

                current += timedelta(minutes=duracion)

        return slots

    # Get upcoming availability as text for assistant context
    @staticmethod
    def obtener_proximos_slots_texto(limit: int = 8) -> str:
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT e.nombre, d.fecha, d.hora_inicio, d.hora_fin
            FROM disponibilidad_empleado d
            JOIN empleados e ON d.id_empleado = e.id_empleado
            WHERE d.fecha >= CURDATE() AND d.disponible = TRUE
            ORDER BY d.fecha, d.hora_inicio
            LIMIT %s
            """,
            (limit,),
        )

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        lines = []

        # Format each availability window as a readable line
        for r in results:
            h_i, m_i = _td_to_time(r["hora_inicio"])
            h_f, m_f = _td_to_time(r["hora_fin"])

            lines.append(
                f"- {r['nombre']}: {r['fecha']} de {h_i:02d}:{m_i:02d} a {h_f:02d}:{m_f:02d}"
            )

        return "\n".join(lines) if lines else "Sin disponibilidad próxima."