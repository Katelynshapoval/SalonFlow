from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from app.controllers.bot_controller import BotController


class BotService:

    def __init__(self, token: str):
        # Store the bot token and initialize the main controller.
        self.token = token
        self.controller = BotController()

    def build(self):
        # Build the Telegram application and register all handlers.
        app = ApplicationBuilder().token(self.token).build()

        self._register_commands(app)
        self._register_general_handlers(app)

        return app

    def _register_commands(self, app) -> None:
        # Register command and callback query handlers.
        app.add_handler(CommandHandler("start", self.controller.start))
        app.add_handler(CommandHandler("help", self.controller.help))
        app.add_handler(CommandHandler("servicios", self.controller.servicios))
        app.add_handler(CommandHandler("book", self.controller.book))
        app.add_handler(CommandHandler("mis_citas", self.controller.mis_citas))
        app.add_handler(CommandHandler("cancel", self.controller.cancel))
        app.add_handler(CommandHandler("contacto_humano", self.controller.contacto_humano))
        app.add_handler(CallbackQueryHandler(self.controller.handle_button))

    def _register_general_handlers(self, app) -> None:
        # Register fallback handlers for text messages and unknown commands.
        app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.controller.handle_message)
        )
        app.add_handler(
            MessageHandler(filters.COMMAND, self.controller.unknown)
        )