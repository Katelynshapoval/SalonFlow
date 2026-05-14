import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "salonflow")
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "minimax-m2.5:cloud")
    # Telegram group chat ID for internal employee alerts.
    # Leave empty to disable alerts (bot will still work normally).
    EMPLOYEE_GROUP_ID: str = os.getenv("EMPLOYEE_GROUP_ID", "")


settings = Settings()
