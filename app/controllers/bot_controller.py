from telegram import Update
from telegram.ext import ContextTypes

from app.controllers.booking_controller import BookingController
from app.controllers.user_controller import UserController
from app.dao.usuario_dao import UsuarioDAO
from app.services.ollama_service import OllamaService


class BotController:
    def __init__(self):
        self.user_ctrl = UserController()
        self.booking_ctrl = BookingController()

    # Handle user-related commands
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.user_ctrl.start(update, context)

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.user_ctrl.help(update, context)

    async def contacto_humano(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.user_ctrl.contacto_humano(update, context)

    # Handle booking-related commands
    async def servicios(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.booking_ctrl.servicios(update, context)

    async def book(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.booking_ctrl.book(update, context)

    async def mis_citas(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.booking_ctrl.mis_citas(update, context)

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        flow = context.user_data.get("flow")

        # Cancel the active human contact flow
        if flow == "contacto_humano":
            context.user_data.clear()

            await update.effective_message.reply_text(
                "✅ Solicitud cancelada.\n\n"
                "No se ha enviado ningún mensaje al equipo."
            )
            return

        # Delegate appointment cancellation to the booking controller
        await self.booking_ctrl.cancel(update, context)

    # Route inline keyboard callbacks
    async def handle_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        data = query.data

        if data == "registro":
            await self.user_ctrl.start_registro(update, context)

        elif data == "cmd_book":
            await self.booking_ctrl.book(update, context)

        elif data == "cmd_mis_citas":
            await self.booking_ctrl.mis_citas(update, context)

        elif data.startswith("sv:"):
            await self.booking_ctrl.seleccionar_servicio(update, context)

        elif data.startswith("sl:"):
            await self.booking_ctrl.seleccionar_slot(update, context)

        elif data == "cn":
            await self.booking_ctrl.confirmar_booking(update, context)

        elif data == "cb":
            await self.booking_ctrl.cancelar_booking_flow(update, context)

        elif data.startswith("cc:"):
            await self.booking_ctrl.seleccionar_cancelacion(update, context)

        elif data.startswith("cy:"):
            await self.booking_ctrl.confirmar_cancelacion(update, context)

        elif data == "ch":
            await self.user_ctrl.contacto_humano(update, context)

    # Route free-text messages based on the active flow
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        flow = context.user_data.get("flow")

        # Continue the active human contact flow
        if flow == "contacto_humano":
            await self.user_ctrl.handle_contacto_humano(update, context)
            return

        # Continue the active registration flow
        if flow == "registro":
            await self.user_ctrl.handle_registro(update, context)
            return

        # Ask the user to continue the booking flow with buttons
        if flow == "booking":
            await update.message.reply_text(
                "📅 Usa los botones para continuar con tu reserva.\n"
                "Escribe /start si quieres cancelarla."
            )
            return

        # Ask the user to continue the cancellation flow with buttons
        if flow == "cancel":
            await update.message.reply_text(
                "🗑 Usa los botones para seleccionar la cita a cancelar.\n"
                "Escribe /start si quieres salir."
            )
            return

        telegram_id = update.effective_user.id

        # Block unregistered users from using free-text features
        if not UsuarioDAO.usuario_registrado(telegram_id):
            await update.message.reply_text(
                "⚠️ Necesitas registrarte para usar el bot.\n"
                "Escribe /start para comenzar."
            )
            return

        # Send registered free-text messages to the AI assistant
        await update.message.chat.send_action("typing")

        respuesta = await OllamaService.generar_respuesta(update.message.text)

        await update.message.reply_text(respuesta)

    # Reply to unknown commands
    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "❓ Comando no reconocido.\n"
            "Escribe /help para ver todos los comandos disponibles."
        )