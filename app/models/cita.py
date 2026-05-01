class Cita:
    def __init__(self, id_cita, id_cliente, id_servicio, fecha, hora, estado):
        self.id_cita = id_cita
        self.id_cliente = id_cliente
        self.id_servicio = id_servicio
        self.fecha = fecha
        self.hora = hora
        self.estado = estado