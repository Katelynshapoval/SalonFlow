import re
import httpx

from config.settings import settings
from app.dao.faq_dao import FAQDAO
from app.dao.servicio_dao import ServicioDAO
from app.dao.empleado_dao import EmpleadoDAO
from app.dao.disponibilidad_dao import DisponibilidadDAO


class OllamaService:
    """
    Wraps the Ollama local LLM endpoint.
    Context is injected read-only from the DB via DAOs.
    The AI is never allowed to write to the DB.
    """

    @staticmethod
    def _build_system_prompt() -> str:
        faq_text = FAQDAO.obtener_todos_texto()
        servicios_text = ServicioDAO.obtener_todos_texto()
        empleados_text = EmpleadoDAO.obtener_todos_texto()
        disponibilidad_text = DisponibilidadDAO.obtener_proximos_slots_texto()

        return (
            "Eres el asistente virtual de SalonFlow, un centro de estética ubicado en Zaragoza.\n"
            "Tu misión es ayudar a los clientes de forma amable, clara y profesional.\n\n"
            "INFORMACIÓN DEL NEGOCIO (usa SÓLO esta información, no inventes datos):\n\n"
            f"== PREGUNTAS FRECUENTES ==\n{faq_text}\n\n"
            f"== SERVICIOS DISPONIBLES ==\n{servicios_text}\n\n"
            f"== EQUIPO ==\n{empleados_text}\n\n"
            f"== PRÓXIMA DISPONIBILIDAD (referencia) ==\n{disponibilidad_text}\n\n"
            "REGLAS ESTRICTAS:\n"
            "- Responde siempre en español.\n"
            "- Sé breve y directo (máximo 3-4 frases).\n"
            "- No uses Markdown, asteriscos, negritas, cursivas, títulos ni formato especial.\n"
            "- Responde en texto plano, limpio y natural.\n"
            "- Usa SÓLO la información anterior; si no sabes algo, dilo honestamente.\n"
            "- NUNCA modifiques datos ni hagas reservas; para eso el cliente usa los comandos del bot.\n"
            "- Si el cliente pregunta por reservas, citas o cancelaciones, indícale que use "
            "/book, /mis_citas o /cancel según el caso.\n"
            "- Si no puedes responder con certeza, sugiere que contacte con el equipo "
            "usando /contacto_humano o llamando al 976 123 456.\n"
        )

    @staticmethod
    def _limpiar_formato(texto: str) -> str:
        """
        Removes common Markdown/formatting symbols that local LLMs may generate.
        This keeps Telegram responses clean when sent as plain text.
        """
        if not texto:
            return ""

        # Remove common Markdown markers
        texto = texto.replace("**", "")
        texto = texto.replace("__", "")
        texto = texto.replace("`", "")

        # Remove Markdown headings like "# Title", "## Title", etc.
        texto = re.sub(r"^\s*#{1,6}\s*", "", texto, flags=re.MULTILINE)

        # Remove simple bullet formatting while keeping the text
        texto = re.sub(r"^\s*[-*]\s+", "", texto, flags=re.MULTILINE)

        # Remove Markdown links but keep the visible text: [texto](url) -> texto
        texto = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", texto)

        # Clean excessive spaces
        texto = re.sub(r"[ \t]+", " ", texto)

        # Clean too many blank lines
        texto = re.sub(r"\n{3,}", "\n\n", texto)

        return texto.strip()

    @staticmethod
    async def generar_respuesta(mensaje: str) -> str:
        system_prompt = OllamaService._build_system_prompt()

        payload = {
            "model": settings.OLLAMA_MODEL,
            "system": system_prompt,
            "prompt": mensaje,
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(settings.OLLAMA_URL, json=payload)
                response.raise_for_status()
                data = response.json()

                respuesta = data.get("response", "").strip()

                if not respuesta:
                    return (
                        "🤔 No he podido procesar tu pregunta ahora mismo.\n"
                        "Escribe /contacto_humano si necesitas ayuda urgente."
                    )

                return OllamaService._limpiar_formato(respuesta)

        except httpx.ConnectError:
            return (
                "⚠️ El asistente no está disponible en este momento.\n"
                "Puedes llamarnos al 976 123 456 o usar /contacto_humano."
            )

        except Exception:
            return (
                "⚠️ Ha ocurrido un error inesperado con el asistente.\n"
                "Usa /contacto_humano para hablar con una persona."
            )