import mysql.connector
from config.settings import settings


class Database:

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="salonflow"
        )