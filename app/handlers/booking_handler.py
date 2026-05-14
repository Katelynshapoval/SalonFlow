from telegram import Update
from telegram.ext import ContextTypes


class BookingHandler:

    @staticmethod
    async def procesar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Handle text messages received during the booking flow.
        await update.message.reply_text(
            "📅 Para reservar, usa los botones que aparecen en pantalla.\n"
            "Si quieres cancelar la reserva en curso, escribe /start."
        )