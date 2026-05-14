from config.db import Database


class FAQDAO:
    # Get all FAQ entries ordered by id
    @staticmethod
    def obtener_todos() -> list[dict]:
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT pregunta, respuesta FROM faq ORDER BY id_faq")

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    # Get all FAQ entries as text for assistant context
    @staticmethod
    def obtener_todos_texto() -> str:
        faqs = FAQDAO.obtener_todos()

        return "\n".join(
            f"P: {f['pregunta']}\nR: {f['respuesta']}"
            for f in faqs
        )