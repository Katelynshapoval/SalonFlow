from telegram import Update
from telegram.ext import ContextTypes

from app.dao.servicio_dao import ServicioDAO


class BookingController:

    async def servicios(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        servicios = ServicioDAO.obtener_servicios()

        if not servicios:
            await update.message.reply_text(
                "❌ No hay servicios disponibles en este momento."
            )
            return

        texto = "💅 *Servicios disponibles*\n\n"

        for s in servicios:
            texto += (
                f"🔹 *{s.nombre}*\n"
                f"⏱ Duración: {s.duracion_minutos} min\n"
                f"💶 Precio: {s.precio}€\n\n"
            )

        texto += "👉 Usa /book para reservar tu cita."

        await update.message.reply_text(texto, parse_mode="Markdown")

    # Aquí irá el booking real después
    async def book(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "📅 Funcionalidad de reserva en desarrollo..."
        )