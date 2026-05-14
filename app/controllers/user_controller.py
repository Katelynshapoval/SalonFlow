from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from app.dao.usuario_dao import UsuarioDAO
from app.dao.solicitud_contacto_dao import SolicitudContactoDAO
from app.handlers.registro_handler import RegistroHandler
from app.services.alert_service import enviar_alerta_contacto


class UserController:

    # ------------------------------------------------------------------ #
    # /start
    # ------------------------------------------------------------------ #
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        telegram_id = update.effective_user.id
        username = update.effective_user.username or ""

        # Clear any active flow so /start always resets state
        context.user_data.clear()

        usuario = UsuarioDAO.obtener_por_telegram_id(telegram_id)

        # ── New user ──────────────────────────────────────────────────
        if not usuario:
            UsuarioDAO.crear_usuario(telegram_id, username)

            keyboard = [
                [InlineKeyboardButton("📝 Registrarme", callback_data="registro")]
            ]

            await update.effective_message.reply_text(
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

        # ── Incomplete registration ───────────────────────────────────
        if not usuario["registrado"]:
            keyboard = [
                [InlineKeyboardButton("📝 Completar registro", callback_data="registro")]
            ]

            await update.effective_message.reply_text(
                "📋 *Registro incompleto*\n\n"
                "Todavía no hemos terminado tu registro. "
                "Pulsa el botón para continuarlo:",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown",
            )
            return

        # ── Registered user ───────────────────────────────────────────
        keyboard = [
            [
                InlineKeyboardButton("📅 Reservar cita", callback_data="cmd_book"),
                InlineKeyboardButton("📋 Mis citas", callback_data="cmd_mis_citas"),
            ],
            [
                InlineKeyboardButton("🧑‍💼 Hablar con una persona", callback_data="ch")
            ],
        ]

        await update.effective_message.reply_text(
            f"👋 *¡Hola, {usuario['nombre']}!*\n\n"
            "¿Qué quieres hacer hoy?\n\n"
            "📋 *Comandos útiles:*\n"
            "*/servicios* — Ver servicios y precios\n"
            "*/book* — Reservar una nueva cita\n"
            "*/mis\\_citas* — Ver tus próximas citas\n"
            "*/cancel* — Cancelar una cita o proceso activo\n"
            "*/help* — Ver ayuda completa",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    # ------------------------------------------------------------------ #
    # /help
    # ------------------------------------------------------------------ #
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
            [InlineKeyboardButton("🧑‍💼 Hablar con una persona", callback_data="ch")]
        ]

        await update.effective_message.reply_text(
            "📋 *Ayuda — SalonFlow*\n\n"
            "Aquí tienes todos los comandos disponibles:\n\n"
            "*/start* — Inicio y menú principal\n"
            "*/servicios* — Ver catálogo de servicios y precios\n"
            "*/book* — Reservar una nueva cita\n"
            "*/mis\\_citas* — Ver tus próximas citas\n"
            "*/cancel* — Cancelar una cita existente\n"
            "*/contacto\\_humano* — Hablar con el equipo del salón\n"
            "*/help* — Mostrar esta ayuda\n\n"
            "💬 También puedes escribirme cualquier pregunta y te responderé "
            "con ayuda de nuestro asistente inteligente.\n\n"
            "📍 *Dirección:* Paseo de Calanda 69, Zaragoza\n"
            "📞 *Teléfono:* 976 123 456\n"
            "🕐 *Horario:* Lunes a viernes, 9:00 – 20:00",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    # ------------------------------------------------------------------ #
    # Registration flow
    # ------------------------------------------------------------------ #
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

    # ------------------------------------------------------------------ #
    # /contacto_humano or "Hablar con una persona" button
    # ------------------------------------------------------------------ #
    async def contacto_humano(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        telegram_id = update.effective_user.id
        id_usuario = UsuarioDAO.obtener_id_usuario(telegram_id)

        if not id_usuario:
            await update.effective_message.reply_text(
                "⚠️ Debes registrarte primero con /start para poder solicitar atención."
            )
            return

        context.user_data["flow"] = "contacto_humano"
        context.user_data["id_usuario_contacto"] = id_usuario

        await update.effective_message.reply_text(
            "🧑‍💼 *Hablar con una persona*\n\n"
            "Cuéntanos brevemente qué problema tienes o en qué podemos ayudarte.\n\n"
            "Escribe tu mensaje aquí abajo.\n"
            "Si quieres cancelar, usa /cancel.",
            parse_mode="Markdown",
        )

    # ------------------------------------------------------------------ #
    # Human contact message flow
    # ------------------------------------------------------------------ #
    async def handle_contacto_humano(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if context.user_data.get("flow") != "contacto_humano":
            return

        if not update.message or not update.message.text:
            await update.effective_message.reply_text(
                "Por favor, escribe un mensaje de texto explicando qué necesitas.\n\n"
                "También puedes usar /cancel para cancelar."
            )
            return

        mensaje = update.message.text.strip()

        if not mensaje:
            await update.effective_message.reply_text(
                "Por favor, escribe un mensaje explicando qué necesitas.\n\n"
                "También puedes usar /cancel para cancelar."
            )
            return

        id_usuario = context.user_data.get("id_usuario_contacto")

        if not id_usuario:
            context.user_data.clear()
            await update.effective_message.reply_text(
                "⚠️ Ha ocurrido un problema con la solicitud. "
                "Por favor, inténtalo de nuevo con /contacto_humano."
            )
            return

        db_ok = SolicitudContactoDAO.crear_solicitud(id_usuario, mensaje)

        if db_ok:
            await enviar_alerta_contacto(
                context.bot,
                username=update.effective_user.username,
                first_name=update.effective_user.first_name,
                mensaje=mensaje,
            )

            context.user_data.clear()

            await update.effective_message.reply_text(
                "🧑‍💼 *Solicitud enviada*\n\n"
                "Hemos enviado tu mensaje al equipo del salón.\n"
                "Alguien se pondrá en contacto contigo lo antes posible.\n\n"
                "📞 976 123 456\n"
                "📍 Paseo de Calanda 69, Zaragoza\n"
                "🕐 Lunes a viernes, 9:00 – 20:00\n\n"
                "¡Gracias por confiar en SalonFlow! 💅",
                parse_mode="Markdown",
            )
        else:
            await update.effective_message.reply_text(
                "⚠️ No hemos podido registrar tu solicitud ahora mismo.\n"
                "Por favor, inténtalo de nuevo más tarde o llama al 976 123 456."
            )