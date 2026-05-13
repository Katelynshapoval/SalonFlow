class Usuario:
    def __init__(self, id_usuario, telegram_id, username, nombre=None,
                 telefono=None, email=None, registrado=False, fecha_registro=None):
        self.id_usuario = id_usuario
        self.telegram_id = telegram_id
        self.username = username
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.registrado = registrado
        self.fecha_registro = fecha_registro
