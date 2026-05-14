from telegram import Update
from telegram.ext import ContextTypes

from app.controllers.user_controller import UserController
from app.controllers.booking_controller import BookingController
from app.dao.usuario_dao import UsuarioDAO
from app.services.ollama_service import OllamaService


class BotController:

    def __init__(self):
        self.user_ctrl = UserController()
        self.booking_ctrl = BookingController()

    # ------------------------------------------------------------------ #
    # Commands
    # ------------------------------------------------------------------ #
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.user_ctrl.start(update, context)

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.user_ctrl.help(update, context)

    async def servicios(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.booking_ctrl.servicios(update, context)

    async def book(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.booking_ctrl.book(update, context)

    async def mis_citas(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.booking_ctrl.mis_citas(update, context)

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.booking_ctrl.cancel(update, context)

    async def contacto_humano(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.user_ctrl.contacto_humano(update, context)

    # ------------------------------------------------------------------ #
    # Inline keyboard callbacks
    # ------------------------------------------------------------------ #
    async def handle_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        data = query.data

        if data == "registro":
            await self.user_ctrl.start_registro(update, context)

        elif data == "cmd_book":
            # Fake a message-based /book call from an inline button
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

    # ------------------------------------------------------------------ #
    # Free-text messages
    # ------------------------------------------------------------------ #
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        flow = context.user_data.get("flow")

        # ── Active registration flow ──────────────────────────────────
        if flow == "registro":
            await self.user_ctrl.handle_registro(update, context)
            return

        # ── Active booking flow (text fallback) ───────────────────────
        if flow == "booking":
            await update.message.reply_text(
                "📅 Usa los botones para continuar con tu reserva.\n"
                "Escribe /start si quieres cancelarla."
            )
            return

        # ── Active cancel flow (text fallback) ────────────────────────
        if flow == "cancel":
            await update.message.reply_text(
                "🗑 Usa los botones para seleccionar la cita a cancelar.\n"
                "Escribe /start si quieres salir."
            )
            return

        # ── Unregistered user ─────────────────────────────────────────
        telegram_id = update.effective_user.id
        if not UsuarioDAO.usuario_registrado(telegram_id):
            await update.message.reply_text(
                "⚠️ Necesitas registrarte para usar el bot.\n"
                "Escribe /start para comenzar."
            )
            return

        # ── AI assistant for everything else ─────────────────────────
        await update.message.chat.send_action("typing")
        respuesta = await OllamaService.generar_respuesta(update.message.text)
        await update.message.reply_text(respuesta)

    # ------------------------------------------------------------------ #
    # Unknown commands
    # ------------------------------------------------------------------ #
    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "❓ Comando no reconocido.\n"
            "Escribe /help para ver todos los comandos disponibles."
        )
