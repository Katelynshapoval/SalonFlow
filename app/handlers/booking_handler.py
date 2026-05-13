"""
Booking text fallback handler.
The main booking interaction uses InlineKeyboardButtons (handled in BookingController).
This module handles edge cases where text is received mid-flow.
"""
from telegram import Update
from telegram.ext import ContextTypes


class BookingHandler:

    @staticmethod
    async def procesar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Called when user sends text while in 'booking' flow.
        await update.message.reply_text(
            "📅 Para reservar, usa los botones que aparecen en pantalla.\n"
            "Si quieres cancelar la reserva en curso, escribe /start."
        )
