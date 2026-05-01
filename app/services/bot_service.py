from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)

from app.controllers.bot_controller import BotController


class BotService:

    def __init__(self, token: str):
        self.token = token
        self.controller = BotController()

    def build(self):
        app = ApplicationBuilder().token(self.token).build()

        # Commands
        app.add_handler(CommandHandler("start", self.controller.start))
        app.add_handler(CommandHandler("help", self.controller.help))

        # Unknown commands
        app.add_handler(MessageHandler(filters.COMMAND, self.controller.unknown))

        return app