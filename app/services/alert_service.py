import logging

from telegram import Bot
from telegram.error import TelegramError

from config.settings import settings

logger = logging.getLogger(__name__)


def _build_display_name(username: str | None, first_name: str | None) -> str:
    # Build a readable user name for the employee alert.
    if username:
        return f"@{username}"

    name = (first_name or "").strip()

    if name:
        return f"{name} (sin username)"

    return "Usuario desconocido (sin username)"


async def enviar_alerta_contacto(
    bot: Bot,
    *,
    username: str | None,
    first_name: str | None,
    mensaje: str,
) -> None:
    # Get the configured employee group chat.
    group_id = settings.EMPLOYEE_GROUP_ID

    if not group_id:
        logger.debug("EMPLOYEE_GROUP_ID no configurado — alerta omitida.")
        return

    # Build the alert message.
    display = _build_display_name(username, first_name)
    texto = (
        "🔔 *Nueva solicitud de atención humana*\n\n"
        f"👤 Cliente: {display}\n"
        f"💬 Mensaje: {mensaje}"
    )

    # Send the alert without affecting the caller if Telegram fails.
    try:
        await bot.send_message(
            chat_id=group_id,
            text=texto,
            parse_mode="Markdown",
        )
        logger.info("Alerta de contacto enviada al grupo %s para %s.", group_id, display)

    except TelegramError as exc:
        logger.error("No se pudo enviar la alerta al grupo %s: %s", group_id, exc)

    except Exception as exc:  # noqa: BLE001
        logger.error("Error inesperado al enviar la alerta de contacto: %s", exc)