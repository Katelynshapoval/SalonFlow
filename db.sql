-- Base de datos
CREATE DATABASE salonflow;
USE salonflow;

-- Tabla de clientes
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de empleados
CREATE TABLE empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    especialidad VARCHAR(100)
);

-- Tabla de servicios
CREATE TABLE servicios (
    id_servicio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    duracion_minutos INT,
    precio DECIMAL(6,2)
);

-- Tabla de citas
CREATE TABLE citas (
    id_cita INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    id_servicio INT,
    id_empleado INT,
    fecha DATE,
    hora TIME,
    estado VARCHAR(50),
    
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_servicio) REFERENCES servicios(id_servicio),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
);

-- Tabla FAQ para el bot
CREATE TABLE faq (
    id_faq INT AUTO_INCREMENT PRIMARY KEY,
    pregunta TEXT,
    respuesta TEXT
);

-- DATOS DE EJEMPLO

-- Clientes
INSERT INTO clientes (nombre, telefono, email) VALUES
('María López', '600123456', 'maria@gmail.com'),
('Laura Gómez', '611222333', 'laura@gmail.com'),
('Ana Martínez', '622333444', 'ana@gmail.com'),
('Carmen Ruiz', '633444555', 'carmen@gmail.com');

-- Empleados
INSERT INTO empleados (nombre, especialidad) VALUES
('Loli', 'Estética avanzada'),
('Alba', 'Tratamientos faciales'),
('Tania', 'Manicura y pedicura');

-- Servicios (basados en Naos Estética)
INSERT INTO servicios (nombre, descripcion, duracion_minutos, precio) VALUES
('Limpieza facial profunda', 'Tratamiento facial para limpiar e hidratar la piel', 60, 35.00),
('Depilación láser', 'Depilación con láser de diodo', 45, 50.00),
('Manicura', 'Cuidado y esmaltado de uñas', 30, 20.00),
('Masaje relajante', 'Masaje corporal para reducir el estrés', 60, 40.00),
('Tratamiento INDIBA', 'Tratamiento avanzado para rejuvenecimiento', 50, 70.00);

-- Citas
INSERT INTO citas (id_cliente, id_servicio, id_empleado, fecha, hora, estado) VALUES
(1, 1, 2, '2026-05-05', '10:00:00', 'confirmada'),
(2, 3, 3, '2026-05-05', '11:00:00', 'confirmada'),
(3, 2, 1, '2026-05-06', '16:30:00', 'pendiente'),
(4, 4, 1, '2026-05-07', '18:00:00', 'confirmada');

-- FAQ (para el bot)
INSERT INTO faq (pregunta, respuesta) VALUES
('¿Cuál es el horario?', 'De lunes a viernes de 9:00 a 20:00, sábado hasta las 13:00'),
('¿Dónde estáis ubicados?', 'Paseo de Calanda 69, Zaragoza'),
('¿Qué servicios ofrecéis?', 'Tratamientos faciales, corporales, depilación, manicura y masajes'),
('¿Cómo puedo reservar cita?', 'Puedes reservar directamente a través de este bot'),
('¿Puedo cancelar una cita?', 'Sí, puedes cancelarla desde el bot o contactando con el centro');
