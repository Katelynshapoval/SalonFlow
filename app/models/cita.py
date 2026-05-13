class Cita:
    def __init__(self, id_cita, id_usuario, id_servicio, id_empleado,
                 fecha, hora, estado,
                 nombre_servicio=None, nombre_empleado=None):
        self.id_cita = id_cita
        self.id_usuario = id_usuario
        self.id_servicio = id_servicio
        self.id_empleado = id_empleado
        self.fecha = fecha
        self.hora = hora
        self.estado = estado
        self.nombre_servicio = nombre_servicio
        self.nombre_empleado = nombre_empleado
