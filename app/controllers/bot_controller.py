from telegram import Update
from telegram.ext import ContextTypes

from app.dao.servicio_dao import ServicioDAO
from app.dao.usuario_dao import UsuarioDAO
from app.handlers.registro_handler import RegistroHandler


class BotController:

    # START
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        username = update.effective_user.username

        usuario = UsuarioDAO.obtener_por_telegram_id(telegram_id)

        if not usuario:
            UsuarioDAO.crear_usuario(telegram_id, username)

            await update.message.reply_text(
                "👋 Bienvenido a *SalonFlow*\n\n"
                "Necesitamos registrarte.\n"
                "Por favor, escribe tu nombre:",
                parse_mode="Markdown"
            )

            context.user_data["registro"] = "nombre"
            return

        if not usuario["registrado"]:
            await update.message.reply_text(
                "📋 Completa tu registro.\n"
                "Escribe tu nombre:"
            )
            context.user_data["registro"] = "nombre"
            return

        await update.message.reply_text(
            "👋 Bienvenido de nuevo a *SalonFlow*\n\n"
            "Usa /servicios para ver los servicios disponibles.",
            parse_mode="Markdown"
        )

    # HELP
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "📋 *Comandos disponibles:*\n\n"
            "/servicios - Ver servicios disponibles\n"
            "/book - Reservar cita\n"
            "/cancel - Cancelar cita\n"
            "/help - Mostrar ayuda",
            parse_mode="Markdown"
        )

    # SERVICIOS
    async def servicios(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        servicios = ServicioDAO.obtener_servicios()

        if not servicios:
            await update.message.reply_text("❌ No hay servicios disponibles.")
            return

        texto = "💅 *Servicios disponibles:*\n\n"

        for s in servicios:
            texto += f"{s.id_servicio}. {s.nombre} - {s.precio}€ ({s.duracion_minutos} min)\n"

        await update.message.reply_text(texto, parse_mode="Markdown")

    # MENSAJES NORMALES (REGISTRO)
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if "registro" in context.user_data:
            await RegistroHandler.procesar(update, context)
            return

        await update.message.reply_text(
            "❓ No entiendo el mensaje.\nUsa /help."
        )

    # COMANDOS DESCONOCIDOS
    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "❌ Comando no reconocido.\n\nUsa /help para ver las opciones."
        )