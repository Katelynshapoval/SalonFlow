from config.db import Database


class FAQDAO:

    @staticmethod
    def obtener_todos() -> list[dict]:
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT pregunta, respuesta FROM faq ORDER BY id_faq")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def obtener_todos_texto() -> str:
        # Returns formatted FAQ for AI context injection.
        faqs = FAQDAO.obtener_todos()
        return "\n".join(
            f"P: {f['pregunta']}\nR: {f['respuesta']}"
            for f in faqs
        )
