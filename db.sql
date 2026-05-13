-- ============================================================
--  SalonFlow — Base de datos completa
--  Charset: utf8mb4 (soporte completo de emojis y acentos)
-- ============================================================

DROP DATABASE IF EXISTS salonflow;
CREATE DATABASE salonflow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE salonflow;

-- ============================================================
--  TABLAS
-- ============================================================

-- Usuarios registrados vía Telegram
CREATE TABLE usuarios (
    id_usuario    INT          AUTO_INCREMENT PRIMARY KEY,
    telegram_id   BIGINT       NOT NULL UNIQUE,
    username      VARCHAR(100),
    nombre        VARCHAR(100),
    telefono      VARCHAR(20),
    email         VARCHAR(150),
    registrado    BOOLEAN      NOT NULL DEFAULT FALSE,
    fecha_registro DATETIME    DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Empleadas del salón
CREATE TABLE empleados (
    id_empleado   INT          AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    especialidad  VARCHAR(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Catálogo de servicios
CREATE TABLE servicios (
    id_servicio       INT            AUTO_INCREMENT PRIMARY KEY,
    nombre            VARCHAR(100)   NOT NULL,
    descripcion       TEXT,
    duracion_minutos  INT            NOT NULL,
    precio            DECIMAL(6,2)   NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Ventanas de disponibilidad de cada empleada
CREATE TABLE disponibilidad_empleado (
    id_disponibilidad INT     AUTO_INCREMENT PRIMARY KEY,
    id_empleado       INT     NOT NULL,
    fecha             DATE    NOT NULL,
    hora_inicio       TIME    NOT NULL,
    hora_fin          TIME    NOT NULL,
    disponible        BOOLEAN NOT NULL DEFAULT TRUE,

    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Citas confirmadas (referencia a usuarios, no a clientes)
CREATE TABLE citas (
    id_cita     INT          AUTO_INCREMENT PRIMARY KEY,
    id_usuario  INT          NOT NULL,
    id_servicio INT          NOT NULL,
    id_empleado INT          NOT NULL,
    fecha       DATE         NOT NULL,
    hora        TIME         NOT NULL,
    estado      VARCHAR(50)  NOT NULL DEFAULT 'confirmada',
    creada_en   DATETIME     DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario)  REFERENCES usuarios(id_usuario)  ON DELETE CASCADE,
    FOREIGN KEY (id_servicio) REFERENCES servicios(id_servicio),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Preguntas frecuentes para el asistente IA
CREATE TABLE faq (
    id_faq    INT  AUTO_INCREMENT PRIMARY KEY,
    pregunta  TEXT NOT NULL,
    respuesta TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Solicitudes de atención humana desde el bot
CREATE TABLE solicitudes_contacto (
    id_solicitud   INT      AUTO_INCREMENT PRIMARY KEY,
    id_usuario     INT      NOT NULL,
    mensaje        TEXT,
    fecha_solicitud DATETIME DEFAULT CURRENT_TIMESTAMP,
    atendida       BOOLEAN  NOT NULL DEFAULT FALSE,

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
--  DATOS DE EJEMPLO (realistas, en español)
-- ============================================================

-- Empleadas
INSERT INTO empleados (nombre, especialidad) VALUES
('Loli Martínez',  'Estética avanzada y tratamientos corporales'),
('Alba Fernández',  'Tratamientos faciales y mesoterapia'),
('Tania Serrano',   'Manicura, pedicura y nail art');

-- Servicios
INSERT INTO servicios (nombre, descripcion, duracion_minutos, precio) VALUES
('Limpieza facial profunda',
 'Limpieza completa con extracción, mascarilla y sérum hidratante.',
 60, 38.00),
('Depilación láser (zona pequeña)',
 'Depilación definitiva con láser de diodo. Zona axilas, bikini o labio.',
 30, 45.00),
('Manicura semipermanente',
 'Manicura con esmaltado semipermanente, incluye preparación y sellado.',
 45, 25.00),
('Masaje relajante',
 'Masaje corporal completo anti-estrés con aceites esenciales.',
 60, 42.00),
('Tratamiento INDIBA activ',
 'Radiofrecuencia de alta tecnología para rejuvenecimiento y firmeza.',
 50, 75.00),
('Pedicura completa',
 'Hidratación, corte, lima y esmaltado de pies.',
 50, 30.00),
('Diseño de cejas con hilo',
 'Definición y depilación de cejas con técnica de hilo árabe.',
 20, 12.00);

-- Disponibilidad (ventanas horarias — fechas a partir de hoy)
INSERT INTO disponibilidad_empleado (id_empleado, fecha, hora_inicio, hora_fin, disponible) VALUES
-- Loli: semana del 20 al 24 de mayo
(1, '2026-05-20', '09:00:00', '14:00:00', TRUE),
(1, '2026-05-20', '16:00:00', '20:00:00', TRUE),
(1, '2026-05-21', '09:00:00', '14:00:00', TRUE),
(1, '2026-05-22', '09:00:00', '14:00:00', TRUE),
(1, '2026-05-22', '16:00:00', '20:00:00', TRUE),
(1, '2026-05-23', '10:00:00', '14:00:00', TRUE),
(1, '2026-05-27', '09:00:00', '14:00:00', TRUE),
(1, '2026-05-27', '16:00:00', '20:00:00', TRUE),
-- Alba: semana del 20 al 24 de mayo
(2, '2026-05-20', '10:00:00', '18:00:00', TRUE),
(2, '2026-05-21', '10:00:00', '18:00:00', TRUE),
(2, '2026-05-22', '10:00:00', '15:00:00', TRUE),
(2, '2026-05-23', '09:00:00', '18:00:00', TRUE),
(2, '2026-05-26', '10:00:00', '18:00:00', TRUE),
(2, '2026-05-27', '10:00:00', '18:00:00', TRUE),
-- Tania: semana del 20 al 24 de mayo
(3, '2026-05-20', '09:30:00', '13:30:00', TRUE),
(3, '2026-05-20', '15:00:00', '19:00:00', TRUE),
(3, '2026-05-21', '09:30:00', '13:30:00', TRUE),
(3, '2026-05-21', '15:00:00', '19:00:00', TRUE),
(3, '2026-05-22', '09:30:00', '13:30:00', TRUE),
(3, '2026-05-26', '09:30:00', '14:00:00', TRUE),
(3, '2026-05-27', '15:00:00', '19:00:00', TRUE);

-- Usuarios de ejemplo (clientes registrados vía Telegram)
INSERT INTO usuarios (telegram_id, username, nombre, telefono, email, registrado) VALUES
(123456789, 'maria_lp',    'María López Pérez',    '612345678', 'maria.lopez@gmail.com',   TRUE),
(987654321, 'laura_gomez', 'Laura Gómez Ruiz',     '623456789', 'lauragomez@hotmail.com',  TRUE),
(111222333, 'carmen_mn',   'Carmen Molina Navas',  '634567890', 'carmen.molina@yahoo.es',  TRUE);

-- Citas de ejemplo (futuras)
INSERT INTO citas (id_usuario, id_servicio, id_empleado, fecha, hora, estado) VALUES
(1, 1, 2, '2026-05-20', '10:00:00', 'confirmada'),  -- María: Limpieza facial con Alba
(2, 3, 3, '2026-05-21', '09:30:00', 'confirmada'),  -- Laura: Manicura con Tania
(3, 5, 1, '2026-05-22', '09:00:00', 'confirmada');  -- Carmen: INDIBA con Loli

-- FAQ para el asistente IA
INSERT INTO faq (pregunta, respuesta) VALUES
('¿Cuál es el horario del salón?',
 'Atendemos de lunes a viernes de 9:00 a 20:00 h. Sábados con cita previa.'),
('¿Dónde estáis ubicados?',
 'Estamos en Paseo de Calanda 69, Zaragoza. Hay aparcamiento gratuito en la misma calle.'),
('¿Cómo puedo reservar una cita?',
 'Puedes reservar directamente desde este bot con el comando /book, de forma rápida y sencilla.'),
('¿Puedo cancelar mi cita?',
 'Sí. Usa /cancel en el bot o llámanos al 976 123 456 con al menos 24 horas de antelación.'),
('¿Qué métodos de pago aceptáis?',
 'Aceptamos efectivo, tarjeta de crédito/débito y Bizum.'),
('¿Los tratamientos de láser duelen?',
 'La depilación láser puede causar una leve molestia similar a un pequeño calambrazo. Es muy bien tolerada.'),
('¿Con qué frecuencia debo hacer las sesiones de láser?',
 'Para depilación láser se recomiendan sesiones cada 4-6 semanas según la zona a tratar.'),
('¿Qué es el tratamiento INDIBA?',
 'INDIBA activ usa radiofrecuencia de 448 kHz para estimular los tejidos, mejorar la circulación y reafirmar la piel.'),
('¿Hay algún bono o pack de sesiones?',
 'Sí, ofrecemos packs de 5 sesiones con un 15% de descuento. Consulta con nuestro equipo.'),
('¿Tenéis lista de espera?',
 'Si no hay disponibilidad, puedes escribirnos a hola@salonflow.es o llamarnos y te apuntamos en lista de espera.'),
('¿Necesito acudir en ayunas a algún tratamiento?',
 'No es necesario para ninguno de nuestros tratamientos habituales.'),
('¿Cuánto tiempo dura una limpieza facial?',
 'La limpieza facial profunda tiene una duración aproximada de 60 minutos.');
