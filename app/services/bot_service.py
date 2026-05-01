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

        self._registrar_comandos(app)
        self._registrar_handlers_generales(app)

        return app

    def _registrar_comandos(self, app):
        app.add_handler(CommandHandler("start", self.controller.start))
        app.add_handler(CommandHandler("help", self.controller.help))
        app.add_handler(CommandHandler("servicios", self.controller.servicios))

        # Próximos comandos que añadiré
        # app.add_handler(CommandHandler("book", self.controller.book))
        # app.add_handler(CommandHandler("cancel", self.controller.cancel))

    def _registrar_handlers_generales(self, app):
        # Comandos desconocidos
        app.add_handler(MessageHandler(filters.COMMAND, self.controller.unknown))