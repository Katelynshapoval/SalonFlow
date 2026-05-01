from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.dao.servicio_dao import ServicioDAO
from app.dao.usuario_dao import UsuarioDAO
from app.handlers.registro_handler import RegistroHandler


class BotController:

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        username = update.effective_user.username

        usuario = UsuarioDAO.obtener_por_telegram_id(telegram_id)

        if not usuario:
            UsuarioDAO.crear_usuario(telegram_id, username)

            keyboard = [
                [InlineKeyboardButton("📝 Registrarme", callback_data="registro")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                "👋 *Bienvenido a SalonFlow*\n\n"
                "💅 Sistema de gestión de citas para centros de estética.\n\n"
                "Desde aquí podrás:\n"
                "• Reservar citas fácilmente\n"
                "• Consultar servicios disponibles\n"
                "• Gestionar tus reservas\n\n"
                "Para comenzar, regístrate pulsando el botón:",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            return

        if not usuario["registrado"]:
            keyboard = [
                [InlineKeyboardButton("📝 Completar registro", callback_data="registro")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                "📋 *Registro incompleto*\n\n"
                "Necesitamos algunos datos para poder gestionar tus citas correctamente.\n\n"
                "Pulsa el botón para continuar:",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            return

        await update.message.reply_text(
            "👋 *Bienvenido de nuevo a SalonFlow*\n\n"
            "Puedes gestionar tus citas de forma rápida y sencilla.\n\n"
            "Usa /servicios para ver los tratamientos disponibles o /help para más opciones.",
            parse_mode="Markdown"
        )

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "📋 *Ayuda - SalonFlow*\n\n"
            "Este bot te permite gestionar tus citas en el centro de estética.\n\n"
            "*Comandos disponibles:*\n"
            "/servicios → Ver lista de servicios\n"
            "/book → Reservar una cita\n"
            "/cancel → Cancelar una cita\n"
            "/help → Mostrar esta ayuda\n\n"
            "💡 Consejo: Empieza viendo los servicios disponibles.",
            parse_mode="Markdown"
        )

    async def servicios(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        servicios = ServicioDAO.obtener_servicios()

        if not servicios:
            await update.message.reply_text("❌ No hay servicios disponibles en este momento.")
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

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if "registro" in context.user_data:
            await RegistroHandler.procesar(update, context)
            return

        await update.message.reply_text(
            "❓ No he entendido tu mensaje.\n\n"
            "Puedes usar /help para ver las opciones disponibles."
        )

    async def handle_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        if query.data == "registro":
            context.user_data["registro"] = "nombre"

            await query.message.reply_text(
                "📝 *Registro de usuario*\n\n"
                "Vamos a empezar.\n"
                "Por favor, escribe tu nombre:",
                parse_mode="Markdown"
            )

    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "❌ Comando no reconocido.\n\n"
            "Usa /help para ver todos los comandos disponibles."
        )

