DROP DATABASE IF EXISTS salonflow;

CREATE DATABASE salonflow;
USE salonflow;

-- USUARIOS (CLIENTES TELEGRAM)
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT UNIQUE,
    username VARCHAR(100),
    nombre VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100),
    registrado BOOLEAN DEFAULT FALSE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- EMPLEADOS
CREATE TABLE empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    especialidad VARCHAR(100)
);

-- =========================
-- SERVICIOS
-- =========================
CREATE TABLE servicios (
    id_servicio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    duracion_minutos INT,
    precio DECIMAL(6,2)
);

-- DISPONIBILIDAD DE EMPLEADOS
CREATE TABLE disponibilidad_empleado (
    id_disponibilidad INT AUTO_INCREMENT PRIMARY KEY,
    id_empleado INT,
    fecha DATE,
    hora_inicio TIME,
    hora_fin TIME,
    disponible BOOLEAN DEFAULT TRUE,

    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
);

-- CITAS
CREATE TABLE citas (
    id_cita INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    id_servicio INT,
    id_empleado INT,
    fecha DATE,
    hora TIME,
    estado VARCHAR(50),

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_servicio) REFERENCES servicios(id_servicio),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
);

-- FAQ
CREATE TABLE faq (
    id_faq INT AUTO_INCREMENT PRIMARY KEY,
    pregunta TEXT,
    respuesta TEXT
);

-- DATOS DE EJEMPLO

-- Empleados
INSERT INTO empleados (nombre, especialidad) VALUES
('Loli', 'Estética avanzada'),
('Alba', 'Tratamientos faciales'),
('Tania', 'Manicura y pedicura');

-- Servicios
INSERT INTO servicios (nombre, descripcion, duracion_minutos, precio) VALUES
('Limpieza facial profunda', 'Tratamiento facial completo', 60, 35.00),
('Depilación láser', 'Depilación con láser de diodo', 45, 50.00),
('Manicura', 'Cuidado y esmaltado de uñas', 30, 20.00),
('Masaje relajante', 'Masaje corporal anti-estrés', 60, 40.00),
('Tratamiento INDIBA', 'Rejuvenecimiento avanzado', 50, 70.00);

-- Disponibilidad empleados (slots reales)
INSERT INTO disponibilidad_empleado (id_empleado, fecha, hora_inicio, hora_fin) VALUES
(1, '2026-05-05', '09:00:00', '14:00:00'),
(1, '2026-05-05', '16:00:00', '20:00:00'),
(2, '2026-05-05', '10:00:00', '18:00:00'),
(3, '2026-05-05', '09:30:00', '13:30:00'),
(3, '2026-05-06', '15:00:00', '19:00:00');

-- Usuarios (simulación Telegram)
INSERT INTO usuarios (telegram_id, username, nombre, telefono, email, registrado) VALUES
(123456789, 'maria123', 'María López', '600123456', 'maria@gmail.com', TRUE),
(987654321, 'laura_g', 'Laura Gómez', '611222333', 'laura@gmail.com', TRUE);

-- Citas
INSERT INTO citas (id_usuario, id_servicio, id_empleado, fecha, hora, estado) VALUES
(1, 1, 2, '2026-05-05', '10:00:00', 'confirmada'),
(2, 3, 3, '2026-05-05', '11:00:00', 'confirmada');

-- FAQ
INSERT INTO faq (pregunta, respuesta) VALUES
('¿Cuál es el horario?', 'De lunes a viernes de 9:00 a 20:00'),
('¿Dónde estáis ubicados?', 'Paseo de Calanda 69, Zaragoza'),
('¿Qué servicios ofrecéis?', 'Tratamientos faciales, corporales, uñas y láser'),
('¿Cómo reservo cita?', 'Puedes hacerlo directamente desde este bot'),
('¿Puedo cancelar?', 'Sí, desde el bot o contactando con el centro');