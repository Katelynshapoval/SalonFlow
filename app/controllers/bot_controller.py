from telegram import Update
from telegram.ext import ContextTypes

from app.dao.servicio_dao import ServicioDAO


class BotController:

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "💅 Bienvenido a *SalonFlow*\n\n"
            "Tu asistente para gestionar citas en el centro de estética.\n\n"
            "Puedes usar los siguientes comandos:\n"
            "/servicios - Ver servicios disponibles\n"
            "/book - Reservar cita\n"
            "/cancel - Cancelar cita\n"
            "/help - Ayuda",
            parse_mode="Markdown"
        )

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "📋 *Comandos disponibles:*\n\n"
            "/servicios - Mostrar lista de servicios\n"
            "/book - Reservar una cita\n"
            "/cancel - Cancelar una cita\n"
            "/help - Mostrar ayuda",
            parse_mode="Markdown"
        )

    async def servicios(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        servicios = ServicioDAO.obtener_servicios()

        if not servicios:
            await update.message.reply_text("❌ No hay servicios disponibles.")
            return

        texto = "💅 *Servicios disponibles:*\n\n"

        for s in servicios:
            texto += f"{s.id_servicio}. {s.nombre} - {s.precio}€ ({s.duracion_minutos} min)\n"

        await update.message.reply_text(texto, parse_mode="Markdown")

    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "❌ Comando no reconocido.\n\nUsa /help para ver las opciones disponibles."
        )