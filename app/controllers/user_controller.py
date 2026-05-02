from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.dao.usuario_dao import UsuarioDAO
from app.handlers.registro_handler import RegistroHandler


class UserController:

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
            "Usa /servicios para ver los tratamientos disponibles.",
            parse_mode="Markdown"
        )

    async def handle_registro(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await RegistroHandler.procesar(update, context)

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