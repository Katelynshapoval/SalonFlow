"""
alert_service.py
Sends internal Telegram alerts to the employee group chat.

Design rules:
- Never raises: all exceptions are caught and logged so the caller's
  DB transaction is never affected by a failed alert.
- Requires no extra dependencies beyond python-telegram-bot.
- Group chat ID is read from settings; if absent, alerts are skipped silently.
"""

import logging
from telegram import Bot
from telegram.error import TelegramError

from config.settings import settings

logger = logging.getLogger(__name__)


def _build_display_name(username: str | None, first_name: str | None) -> str:
    """
    Returns a human-readable identifier for the employee alert.
    Prefers @username; falls back to '<first_name> (sin username)'.
    """
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
    """
    Sends a human-support alert to the configured employee group.

    Parameters
    ----------
    bot        : The running Bot instance (available as context.bot).
    username   : Telegram username of the requesting user (may be None).
    first_name : Telegram first name of the requesting user (may be None).
    mensaje    : The support request message stored in solicitudes_contacto.
    """
    group_id = settings.EMPLOYEE_GROUP_ID
    if not group_id:
        logger.debug("EMPLOYEE_GROUP_ID no configurado — alerta omitida.")
        return

    display = _build_display_name(username, first_name)

    texto = (
        "🔔 *Nueva solicitud de atención humana*\n\n"
        f"👤 Cliente: {display}\n"
        f"💬 Mensaje: {mensaje}"
    )

    try:
        await bot.send_message(
            chat_id=group_id,
            text=texto,
            parse_mode="Markdown",
        )
        logger.info("Alerta de contacto enviada al grupo %s para %s.", group_id, display)
    except TelegramError as exc:
        logger.error(
            "No se pudo enviar la alerta al grupo %s: %s", group_id, exc
        )
    except Exception as exc:  # noqa: BLE001
        logger.error(
            "Error inesperado al enviar la alerta de contacto: %s", exc
        )
