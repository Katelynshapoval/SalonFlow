import mysql.connector
from config.settings import settings


class Database:

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            charset="utf8mb4",
            use_unicode=True,
        )
