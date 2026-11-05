-- =========================================
-- BASE DE DATOS: SISTEMA DE NOTAS
-- Motor: MySQL 8.0.16 o superior
-- =========================================

CREATE DATABASE IF NOT EXISTS sistema_notas
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE sistema_notas;

-- =========================================
-- 1. TABLA: ESTUDIANTES
-- =========================================

CREATE TABLE IF NOT EXISTS estudiantes (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    cedula VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(120) NOT NULL UNIQUE,
    fecha_nacimiento DATE,
    estado ENUM('Activo', 'Inactivo') NOT NULL DEFAULT 'Activo',
    fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =========================================
-- 2. TABLA: DOCENTES
-- =========================================

CREATE TABLE IF NOT EXISTS docentes (
    id_docente INT AUTO_INCREMENT PRIMARY KEY,
    cedula VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(120) NOT NULL UNIQUE,
    especialidad VARCHAR(100),
    estado ENUM('Activo', 'Inactivo') NOT NULL DEFAULT 'Activo'
) ENGINE=InnoDB;

-- =========================================
-- 3. TABLA: ASIGNATURAS
-- =========================================

CREATE TABLE IF NOT EXISTS asignaturas (
    id_asignatura INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    nivel VARCHAR(50),
    id_docente INT NOT NULL,

    CONSTRAINT fk_asignatura_docente
    FOREIGN KEY (id_docente)
    REFERENCES docentes(id_docente)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,

    CONSTRAINT uq_asignatura_docente
    UNIQUE (nombre, id_docente)
) ENGINE=InnoDB;

-- =========================================
-- 4. TABLA: NOTAS
-- Una fila por estudiante y asignatura
-- =========================================

CREATE TABLE IF NOT EXISTS notas (
    id_nota INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_asignatura INT NOT NULL,

    nota1 DECIMAL(4,2) NOT NULL,
    nota2 DECIMAL(4,2) NOT NULL,
    examen DECIMAL(4,2) NOT NULL,

    promedio DECIMAL(4,2)
    GENERATED ALWAYS AS (
        ROUND((nota1 + nota2 + examen) / 3, 2)
    ) STORED,

    observacion VARCHAR(255),
    fecha_actualizacion TIMESTAMP NOT NULL
    DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_nota_estudiante
    FOREIGN KEY (id_estudiante)
    REFERENCES estudiantes(id_estudiante)
    ON UPDATE CASCADE
    ON DELETE CASCADE,

    CONSTRAINT fk_nota_asignatura
    FOREIGN KEY (id_asignatura)
    REFERENCES asignaturas(id_asignatura)
    ON UPDATE CASCADE
    ON DELETE CASCADE,

    CONSTRAINT uq_estudiante_asignatura
    UNIQUE (id_estudiante, id_asignatura),

    CONSTRAINT chk_nota1
    CHECK (nota1 BETWEEN 0 AND 10),

    CONSTRAINT chk_nota2
    CHECK (nota2 BETWEEN 0 AND 10),

    CONSTRAINT chk_examen
    CHECK (examen BETWEEN 0 AND 10)
) ENGINE=InnoDB;

-- =========================================
-- FIN DEL SCRIPT
-- =========================================
