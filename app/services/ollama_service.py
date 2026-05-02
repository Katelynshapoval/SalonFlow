import requests

from config.db import Database


class OllamaService:

    OLLAMA_URL = "http://localhost:11434/api/generate"
    MODEL = "minimax-m2.5:cloud"

    @staticmethod
    def _get_db_context():

        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)

        # FAQ
        cursor.execute("SELECT pregunta, respuesta FROM faq")
        faqs = cursor.fetchall()

        faq_text = ""
        for f in faqs:
            faq_text += f"Pregunta: {f['pregunta']}\nRespuesta: {f['respuesta']}\n\n"

        # Servicios
        cursor.execute("SELECT nombre, duracion_minutos, precio FROM servicios")
        servicios = cursor.fetchall()

        servicios_text = ""
        for s in servicios:
            servicios_text += (
                f"{s['nombre']} - {s['precio']}€ ({s['duracion_minutos']} min)\n"
            )

        # Empleados
        cursor.execute("SELECT nombre, especialidad FROM empleados")
        empleados = cursor.fetchall()

        empleados_text = ""
        for e in empleados:
            empleados_text += f"{e['nombre']} - {e['especialidad']}\n"

        cursor.close()
        conn.close()

        return faq_text, servicios_text, empleados_text

    @staticmethod
    def generar_respuesta(mensaje: str) -> str:

        faq_text, servicios_text, empleados_text = OllamaService._get_db_context()

        prompt = f"""
Eres un asistente de un centro de estética llamado SalonFlow.

Tu trabajo es ayudar a clientes respondiendo preguntas de forma clara, breve y profesional.

INFORMACIÓN DEL NEGOCIO:

FAQ:
{faq_text}

SERVICIOS:
{servicios_text}

EMPLEADOS:
{empleados_text}

REGLAS:
- Usa SOLO la información proporcionada
- No inventes datos
- Si no sabes algo, di que el cliente contacte con el centro
- Sé breve y claro

Pregunta del cliente:
{mensaje}
"""

        try:
            response = requests.post(
                OllamaService.OLLAMA_URL,
                json={
                    "model": OllamaService.MODEL,
                    "prompt": prompt,
                    "stream": False
                }
            )

            data = response.json()
            return data.get("response", "No he podido responder en este momento.")

        except Exception:
            return "⚠️ Error al conectar con el asistente."