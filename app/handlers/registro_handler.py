import re

from telegram import Update
from telegram.ext import ContextTypes

from app.dao.usuario_dao import UsuarioDAO


class RegistroHandler:
    _EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    _PHONE_RE = re.compile(r"^[6789]\d{8}$")

    @staticmethod
    async def procesar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Get the current user input and registration state.
        telegram_id = update.effective_user.id
        texto = update.message.text.strip()
        estado = context.user_data.get("registro")

        # Process the name step.
        if estado == "nombre":
            if len(texto) < 2:
                await update.message.reply_text("⚠️ El nombre es demasiado corto. Inténtalo de nuevo:")
                return

            context.user_data["nombre"] = texto
            context.user_data["registro"] = "telefono"

            await update.message.reply_text(
                "📞 Introduce tu número de teléfono móvil (9 dígitos):"
            )
            return

        # Process the phone number step.
        if estado == "telefono":
            limpio = texto.replace(" ", "").replace("-", "")

            if not RegistroHandler._PHONE_RE.match(limpio):
                await update.message.reply_text(
                    "⚠️ Formato incorrecto. Introduce un teléfono móvil español de 9 dígitos:"
                )
                return

            context.user_data["telefono"] = limpio
            context.user_data["registro"] = "email"

            await update.message.reply_text("📧 Introduce tu correo electrónico:")
            return

        # Process the email step and complete the registration.
        if estado == "email":
            if not RegistroHandler._EMAIL_RE.match(texto):
                await update.message.reply_text(
                    "⚠️ El correo no parece válido. Inténtalo de nuevo:"
                )
                return

            nombre = context.user_data.pop("nombre")
            telefono = context.user_data.pop("telefono")
            context.user_data.pop("registro")
            context.user_data.pop("flow", None)

            UsuarioDAO.completar_registro(telegram_id, nombre, telefono, texto)

            await update.message.reply_text(
                f"✅ *¡Registro completado, {nombre}!*\n\n"
                "Ya puedes disfrutar de todos los servicios del bot.\n\n"
                "💅 Usa /servicios para ver nuestros tratamientos\n"
                "📅 Usa /book para reservar tu primera cita\n"
                "📋 Usa /help para ver todos los comandos",
                parse_mode="Markdown",
            )