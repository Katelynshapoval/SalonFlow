from telegram import Update
from telegram.ext import ContextTypes

class BotController:

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "👋 Welcome to SalonFlow!\n\n"
            "Use /book to schedule an appointment."
        )

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Available commands:\n"
            "/book - Book appointment\n"
            "/cancel - Cancel appointment\n"
            "/help - Show this message"
        )

    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "❌ Sorry, I didn't understand that command."
        )