from config.db import Database


class FAQDAO:

    @staticmethod
    def obtener_todos():
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM faq")
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results