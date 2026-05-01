from app.dao.usuario_dao import UsuarioDAO


class RegistroHandler:

    @staticmethod
    async def procesar(update, context):
        telegram_id = update.effective_user.id
        texto = update.message.text

        estado = context.user_data.get("registro")

        if estado == "nombre":
            context.user_data["nombre"] = texto
            context.user_data["registro"] = "telefono"

            await update.message.reply_text("📞 Introduce tu teléfono:")
            return

        if estado == "telefono":
            context.user_data["telefono"] = texto
            context.user_data["registro"] = "email"

            await update.message.reply_text("📧 Introduce tu email:")
            return

        if estado == "email":
            nombre = context.user_data["nombre"]
            telefono = context.user_data["telefono"]
            email = texto

            UsuarioDAO.completar_registro(
                telegram_id, nombre, telefono, email
            )

            context.user_data.clear()

            await update.message.reply_text(
                "✅ Registro completado correctamente.\n\n"
                "Ya puedes usar el bot.\n"
                "Usa /servicios para empezar."
            )