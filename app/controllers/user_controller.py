from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.dao.usuario_dao import UsuarioDAO
from app.dao.solicitud_contacto_dao import SolicitudContactoDAO
from app.handlers.registro_handler import RegistroHandler


class UserController:

    # /start
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        telegram_id = update.effective_user.id
        username = update.effective_user.username or ""

        # Clear any active flow so /start always resets state
        context.user_data.clear()

        usuario = UsuarioDAO.obtener_por_telegram_id(telegram_id)

        # New user
        if not usuario:
            UsuarioDAO.crear_usuario(telegram_id, username)
            keyboard = [[InlineKeyboardButton("📝 Registrarme", callback_data="registro")]]
            await update.message.reply_text(
                "👋 *¡Bienvenido a SalonFlow!*\n\n"
                "💅 Somos tu centro de estética de confianza.\n"
                "Desde aquí podrás:\n"
                "• Reservar y gestionar citas\n"
                "• Consultar servicios y precios\n"
                "• Hablar con nuestro asistente\n\n"
                "Para empezar, necesitamos registrarte. "
                "Pulsa el botón y sólo te pediremos nombre, teléfono y email:",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown",
            )
            return

        # Incomplete registration
        if not usuario["registrado"]:
            keyboard = [[InlineKeyboardButton("📝 Completar registro", callback_data="registro")]]
            await update.message.reply_text(
                "📋 *Registro incompleto*\n\n"
                "Todavía no hemos terminado tu registro. "
                "Pulsa el botón para continuarlo:",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown",
            )
            return

        # Registered user
        keyboard = [
            [
                InlineKeyboardButton("📅 Reservar cita", callback_data="cmd_book"),
                InlineKeyboardButton("📋 Mis citas", callback_data="cmd_mis_citas"),
            ],
            [InlineKeyboardButton("🧑‍💼 Hablar con una persona", callback_data="ch")],
        ]
        await update.message.reply_text(
            f"👋 *¡Hola, {usuario['nombre']}!*\n\n"
            "¿Qué quieres hacer hoy?\n\n"
            "También puedes usar los comandos:\n"
            "/servicios · /book · /mis\\_citas · /cancel · /help",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    # /help
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [[InlineKeyboardButton("🧑‍💼 Hablar con una persona", callback_data="ch")]]
        await update.message.reply_text(
            "📋 *Ayuda — SalonFlow*\n\n"
            "Aquí tienes todos los comandos disponibles:\n\n"
            "*/start* — Inicio y menú principal\n"
            "*/servicios* — Ver catálogo de servicios y precios\n"
            "*/book* — Reservar una nueva cita\n"
            "*/mis_citas* — Ver tus próximas citas\n"
            "*/cancel* — Cancelar una cita existente\n"
            "*/contacto_humano* — Hablar con el equipo del salón\n"
            "*/help* — Mostrar esta ayuda\n\n"
            "💬 También puedes escribirme cualquier pregunta y te responderé "
            "con ayuda de nuestro asistente inteligente.\n\n"
            "📍 *Dirección:* Paseo de Calanda 69, Zaragoza\n"
            "📞 *Teléfono:* 976 123 456\n"
            "🕐 *Horario:* Lunes a viernes, 9:00 – 20:00",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    # Registration flow
    async def start_registro(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Triggered when user taps 'Registrarme' button."""
        context.user_data["flow"] = "registro"
        context.user_data["registro"] = "nombre"
        await update.effective_message.reply_text(
            "📝 *Registro de usuario*\n\n"
            "Sólo necesitamos tres datos para crear tu perfil.\n\n"
            "¿Cuál es tu nombre completo?",
            parse_mode="Markdown",
        )

    async def handle_registro(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await RegistroHandler.procesar(update, context)

    # /contacto_humano
    async def contacto_humano(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        telegram_id = update.effective_user.id
        id_usuario = UsuarioDAO.obtener_id_usuario(telegram_id)

        if not id_usuario:
            await update.effective_message.reply_text(
                "⚠️ Debes registrarte primero con /start para poder solicitar atención."
            )
            return

        SolicitudContactoDAO.crear_solicitud(id_usuario)

        await update.effective_message.reply_text(
            "🧑‍💼 *Solicitud registrada*\n\n"
            "Hemos anotado que deseas hablar con una persona de nuestro equipo.\n"
            "Te contactaremos lo antes posible.\n\n"
            "Si necesitas una respuesta urgente:\n"
            "📞 976 123 456\n"
            "📍 Paseo de Calanda 69, Zaragoza\n"
            "🕐 Lunes a viernes, 9:00 – 20:00\n\n"
            "¡Gracias por confiar en SalonFlow! 💅",
            parse_mode="Markdown",
        )
