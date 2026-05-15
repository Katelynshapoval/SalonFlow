from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.dao.cita_dao import CitaDAO
from app.dao.disponibilidad_dao import DisponibilidadDAO
from app.dao.servicio_dao import ServicioDAO
from app.dao.usuario_dao import UsuarioDAO


_DIAS_ES = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
_MESES_ES = [
    "",
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]


# Format an iso date into a readable spanish date
def _fmt_fecha(fecha_str: str) -> str:
    d = date.fromisoformat(str(fecha_str))
    dia_semana = _DIAS_ES[d.weekday()]
    return f"{dia_semana} {d.day} {_MESES_ES[d.month]}"

def _slots_por_fecha(slots):
    fechas = {}

    for sl in slots:
        fecha = str(sl["fecha"])
        fechas.setdefault(fecha, []).append(sl)

    return fechas


# Check that the user is registered before running protected commands
def _require_registered(func):
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id

        if not UsuarioDAO.usuario_registrado(telegram_id):
            await update.effective_message.reply_text(
                "⚠️ Necesitas registrarte antes de usar este comando.\n"
                "Escribe /start para comenzar."
            )
            return

        return await func(self, update, context)

    return wrapper


class BookingController:
    # Show the available services
    async def servicios(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        servicios = ServicioDAO.obtener_servicios()

        if not servicios:
            await update.message.reply_text("❌ No hay servicios disponibles ahora mismo.")
            return

        texto = "💅 *Nuestros servicios*\n\n"

        for s in servicios:
            texto += (
                f"🔹 *{s.nombre}*\n"
                f"   📄 {s.descripcion}\n"
                f"   ⏱ {s.duracion_minutos} min · 💶 {s.precio}€\n\n"
            )

        texto += "👉 Reserva con /book"

        await update.message.reply_text(texto, parse_mode="Markdown")

    # Start the booking flow and ask the user to choose a service
    @_require_registered
    async def book(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        context.user_data["flow"] = "booking"
        context.user_data["booking"] = {"step": "service"}

        servicios = ServicioDAO.obtener_servicios()

        if not servicios:
            await update.effective_message.reply_text("❌ No hay servicios disponibles ahora mismo.")
            return

        keyboard = [
            [
                InlineKeyboardButton(
                    f"{s.nombre} — {s.precio}€",
                    callback_data=f"sv:{s.id_servicio}",
                )
            ]
            for s in servicios
        ]

        keyboard.append([InlineKeyboardButton("❌ Cancelar", callback_data="cb")])

        await update.effective_message.reply_text(
            "📅 *Nueva reserva*\n\nElige el servicio que deseas:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    # Save the selected service and show available slots
    # Save the selected service and ask the user to choose an available day
    async def seleccionar_servicio(
            self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        query = update.callback_query
        id_servicio = int(query.data.split(":")[1])

        servicio = ServicioDAO.obtener_por_id(id_servicio)

        if not servicio:
            await query.message.reply_text("❌ Servicio no encontrado.")
            return

        slots = DisponibilidadDAO.obtener_slots_disponibles(id_servicio)

        if not slots:
            context.user_data.pop("flow", None)
            context.user_data.pop("booking", None)

            await query.message.reply_text(
                "😔 No hay horarios disponibles para este servicio en los próximos 14 días.\n"
                "Llámanos al 976 123 456 para encontrar una fecha."
            )
            return

        fechas_disponibles = sorted({str(sl["fecha"]) for sl in slots})

        context.user_data["booking"] = {
            "step": "day",
            "id_servicio": id_servicio,
            "nombre_servicio": servicio.nombre,
            "slots": slots,
        }

        keyboard = [
            [
                InlineKeyboardButton(
                    f"📅 {_fmt_fecha(fecha)}",
                    callback_data=f"fd:{fecha}",
                )
            ]
            for fecha in fechas_disponibles
        ]

        keyboard.append([InlineKeyboardButton("❌ Cancelar", callback_data="cb")])

        await query.message.reply_text(
            f"✅ Has elegido: *{servicio.nombre}*\n\n"
            "Ahora elige el día de la cita:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    # Save the selected day and show available times for that day
    async def seleccionar_fecha(
            self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        query = update.callback_query
        fecha = query.data.split(":", 1)[1]

        booking = context.user_data.get("booking", {})
        slots = booking.get("slots", [])

        slots_dia = [
            sl for sl in slots
            if str(sl["fecha"]) == fecha
        ]

        if not slots_dia:
            await query.message.reply_text(
                "😔 Ya no hay horarios disponibles para ese día.\n"
                "Usa /book para elegir otra fecha."
            )
            return

        booking.update(
            step="slot",
            fecha=fecha,
        )
        context.user_data["booking"] = booking

        keyboard = []

        for sl in slots_dia:
            label = f"👤 {sl['empleado_nombre']}  🕐 {sl['hora']}"
            cb = f"sl:{sl['id_empleado']}:{fecha}:{sl['hora']}"
            keyboard.append([InlineKeyboardButton(label, callback_data=cb)])

        keyboard.append([InlineKeyboardButton("↩️ Elegir otro día", callback_data="bd")])
        keyboard.append([InlineKeyboardButton("❌ Cancelar", callback_data="cb")])

        await query.message.reply_text(
            f"🗓 *Horarios disponibles para {_fmt_fecha(fecha)}:*\n\n"
            f"Servicio: *{booking.get('nombre_servicio', '—')}*",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    # Go back from time selection to day selection
    async def volver_a_fechas(
            self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        query = update.callback_query

        booking = context.user_data.get("booking", {})
        slots = booking.get("slots", [])

        if not slots:
            await query.message.reply_text(
                "❌ No se encontraron horarios guardados. Usa /book para empezar de nuevo."
            )
            return

        fechas_disponibles = sorted({str(sl["fecha"]) for sl in slots})

        booking["step"] = "day"
        booking.pop("fecha", None)
        context.user_data["booking"] = booking

        keyboard = [
            [
                InlineKeyboardButton(
                    f"📅 {_fmt_fecha(fecha)}",
                    callback_data=f"fd:{fecha}",
                )
            ]
            for fecha in fechas_disponibles
        ]

        keyboard.append([InlineKeyboardButton("❌ Cancelar", callback_data="cb")])

        await query.message.reply_text(
            "📅 Elige otro día disponible:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    # Save the selected slot and ask the user to confirm the booking
    async def seleccionar_slot(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        query = update.callback_query
        _, id_empleado_str, fecha, hora = query.data.split(":", 3)
        id_empleado = int(id_empleado_str)

        booking = context.user_data.get("booking", {})
        booking.update(
            step="confirm",
            id_empleado=id_empleado,
            fecha=fecha,
            hora=hora,
        )
        context.user_data["booking"] = booking

        keyboard = [
            [
                InlineKeyboardButton("✅ Confirmar", callback_data="cn"),
                InlineKeyboardButton("❌ Cancelar", callback_data="cb"),
            ]
        ]

        await query.message.reply_text(
            "📋 *Resumen de tu reserva*\n\n"
            f"💅 Servicio: *{booking.get('nombre_servicio', '—')}*\n"
            f"📅 Fecha: *{_fmt_fecha(fecha)}*\n"
            f"🕐 Hora: *{hora} h*\n\n"
            "¿Confirmas la cita?",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    # Confirm the booking and create the appointment
    async def confirmar_booking(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        query = update.callback_query
        telegram_id = update.effective_user.id
        booking = context.user_data.get("booking", {})

        id_usuario = UsuarioDAO.obtener_id_usuario(telegram_id)

        if not id_usuario:
            await query.message.reply_text("❌ Error: usuario no encontrado.")
            return

        id_servicio = booking.get("id_servicio")
        id_empleado = booking.get("id_empleado")
        fecha = booking.get("fecha")
        hora = booking.get("hora")

        # Re-check availability before saving the appointment
        if CitaDAO.hay_conflicto(id_empleado, fecha, hora):
            context.user_data.pop("flow", None)
            context.user_data.pop("booking", None)

            await query.message.reply_text(
                "⚠️ Lo sentimos, ese horario acaba de ser reservado por otra persona.\n"
                "Usa /book para elegir otro horario."
            )
            return

        id_cita = CitaDAO.crear_cita(id_usuario, id_servicio, id_empleado, fecha, hora)

        context.user_data.pop("flow", None)
        context.user_data.pop("booking", None)

        if id_cita:
            await query.message.reply_text(
                "🎉 *¡Cita confirmada!*\n\n"
                f"💅 {booking.get('nombre_servicio', '—')}\n"
                f"📅 {_fmt_fecha(fecha)} a las {hora} h\n\n"
                "Te esperamos. Puedes ver tus citas con /mis\\_citas\n"
                "y cancelar si necesitas con /cancel.",
                parse_mode="Markdown",
            )
        else:
            await query.message.reply_text(
                "❌ Ha ocurrido un error al guardar la cita. "
                "Por favor llámanos al 976 123 456."
            )

    # Cancel the current booking flow
    async def cancelar_booking_flow(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        context.user_data.pop("flow", None)
        context.user_data.pop("booking", None)

        await update.callback_query.message.reply_text(
            "❌ Reserva cancelada. Usa /book cuando quieras intentarlo de nuevo."
        )

    # Show the user's future appointments
    @_require_registered
    async def mis_citas(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        telegram_id = update.effective_user.id
        id_usuario = UsuarioDAO.obtener_id_usuario(telegram_id)
        citas = CitaDAO.obtener_citas_futuras(id_usuario)

        if not citas:
            await update.effective_message.reply_text(
                "📋 No tienes citas próximas.\n\nReserva una con /book 😊"
            )
            return

        numeros = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        texto = "📋 *Tus próximas citas:*\n\n"

        for i, c in enumerate(citas):
            icono = numeros[i] if i < len(numeros) else "🔹"
            texto += (
                f"{icono} *{c.nombre_servicio}*\n"
                f"   👤 {c.nombre_empleado}\n"
                f"   📅 {_fmt_fecha(c.fecha)}\n"
                f"   🕐 {c.hora} h\n"
                f"   Estado: ✅ Confirmada\n\n"
            )

        texto += "Para cancelar alguna, usa /cancel."

        await update.effective_message.reply_text(texto, parse_mode="Markdown")

    # Start the cancellation flow and list future appointments
    @_require_registered
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        telegram_id = update.effective_user.id
        id_usuario = UsuarioDAO.obtener_id_usuario(telegram_id)
        citas = CitaDAO.obtener_citas_futuras(id_usuario)

        if not citas:
            await update.message.reply_text("📋 No tienes citas próximas que cancelar.")
            return

        keyboard = [
            [
                InlineKeyboardButton(
                    f"❌ {c.nombre_servicio} · {_fmt_fecha(c.fecha)} {c.hora}",
                    callback_data=f"cc:{c.id_cita}",
                )
            ]
            for c in citas
        ]

        keyboard.append([InlineKeyboardButton("↩️ Volver", callback_data="cb")])

        context.user_data["flow"] = "cancel"

        await update.message.reply_text(
            "🗑 *¿Cuál cita deseas cancelar?*\n\n"
            "Pulsa la cita que quieres anular:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    # Save the selected appointment and ask the user to confirm cancellation
    async def seleccionar_cancelacion(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        query = update.callback_query
        id_cita = int(query.data.split(":")[1])

        context.user_data["cancel_cita_id"] = id_cita

        keyboard = [
            [
                InlineKeyboardButton("✅ Sí, cancelar", callback_data=f"cy:{id_cita}"),
                InlineKeyboardButton("↩️ No, volver", callback_data="cb"),
            ]
        ]

        await query.message.reply_text(
            "⚠️ ¿Confirmas que quieres *cancelar* esta cita?",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    # Confirm the cancellation and update the appointment
    async def confirmar_cancelacion(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        query = update.callback_query
        id_cita = int(query.data.split(":")[1])
        telegram_id = update.effective_user.id
        id_usuario = UsuarioDAO.obtener_id_usuario(telegram_id)

        ok = CitaDAO.cancelar_cita(id_cita, id_usuario)

        context.user_data.pop("flow", None)
        context.user_data.pop("cancel_cita_id", None)

        if ok:
            await query.message.reply_text(
                "✅ *Cita cancelada correctamente.*\n\n"
                "Si necesitas reservar otra, usa /book.",
                parse_mode="Markdown",
            )
        else:
            await query.message.reply_text(
                "❌ No se ha podido cancelar la cita. "
                "Puede que ya estuviera cancelada o haya ocurrido un error."
            )