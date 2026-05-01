from config.settings import settings
from app.services.bot_service import BotService


def main():
    bot_service = BotService(settings.TELEGRAM_TOKEN)
    app = bot_service.build()

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()