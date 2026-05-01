from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)
from telegram.ext import CallbackQueryHandler
from app.controllers.bot_controller import BotController


class BotService:

    def __init__(self, token: str):
        self.token = token
        self.controller = BotController()

    def build(self):
        app = ApplicationBuilder().token(self.token).build()

        self._registrar_comandos(app)
        self._registrar_handlers_generales(app)

        return app

    # =========================
    # COMANDOS
    # =========================
    def _registrar_comandos(self, app):
        app.add_handler(CommandHandler("start", self.controller.start))
        app.add_handler(CommandHandler("help", self.controller.help))
        app.add_handler(CommandHandler("servicios", self.controller.servicios))
        app.add_handler(CallbackQueryHandler(self.controller.handle_button))

        # Próximos pasos
        # app.add_handler(CommandHandler("book", self.controller.book))
        # app.add_handler(CommandHandler("cancel", self.controller.cancel))

    # MENSAJES GENERALES
    def _registrar_handlers_generales(self, app):
        # Mensajes normales (registro)
        app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.controller.handle_message)
        )

        # Comandos desconocidos
        app.add_handler(
            MessageHandler(filters.COMMAND, self.controller.unknown)
        )