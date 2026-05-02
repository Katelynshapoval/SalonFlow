from telegram import Update
from telegram.ext import ContextTypes

from app.controllers.user_controller import UserController
from app.controllers.booking_controller import BookingController
from app.dao.usuario_dao import UsuarioDAO
from app.services.ollama_service import OllamaService

class BotController:

    def __init__(self):
        self.user_controller = UserController()
        self.booking_controller = BookingController()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.user_controller.start(update, context)

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
        await self.booking_controller.servicios(update, context)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        # Registro primero
        if "registro" in context.user_data:
            await self.user_controller.handle_registro(update, context)
            return

        # Si no está registrado → no permitir uso
        telegram_id = update.effective_user.id
        usuario = UsuarioDAO.obtener_por_telegram_id(telegram_id)

        if not usuario or not usuario["registrado"]:
            await update.message.reply_text(
                "⚠️ Debes registrarte primero usando /start."
            )
            return

        # IA responde preguntas
        mensaje = update.message.text

        respuesta = OllamaService.generar_respuesta(mensaje)

        await update.message.reply_text(respuesta)

    async def handle_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.user_controller.handle_button(update, context)

    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "❌ Comando no reconocido.\n\n"
            "Usa /help para ver todos los comandos disponibles."
        )