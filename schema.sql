-- Diseño físico de la base de datos (MySQL)
-- Antes de correrlo, creá la base:  CREATE DATABASE portfolio CHARACTER SET utf8mb4;
-- (en Clever Cloud la base ya viene creada)

CREATE TABLE IF NOT EXISTS usuarios (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50)  NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS perfil (
    id          INT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    titulo      VARCHAR(100) NOT NULL,
    descripcion TEXT,
    email       VARCHAR(120) NOT NULL DEFAULT '',
    foto        VARCHAR(255) NOT NULL DEFAULT 'img/avatar.svg',
    banner      VARCHAR(255) NOT NULL DEFAULT 'img/banner.svg',
    cv          VARCHAR(255) NOT NULL DEFAULT '',
    iframe_url  VARCHAR(500) NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS redes (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    perfil_id INT NOT NULL DEFAULT 1,
    nombre    VARCHAR(50)  NOT NULL,
    url       VARCHAR(255) NOT NULL,
    icono     VARCHAR(60)  NOT NULL DEFAULT 'fa-solid fa-globe',
    FOREIGN KEY (perfil_id) REFERENCES perfil(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS experiencia (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    perfil_id   INT NOT NULL DEFAULT 1,
    empresa     VARCHAR(100) NOT NULL,
    puesto      VARCHAR(100) NOT NULL,
    periodo     VARCHAR(50)  NOT NULL DEFAULT '',
    descripcion TEXT,
    logo        VARCHAR(255) NOT NULL DEFAULT '',
    FOREIGN KEY (perfil_id) REFERENCES perfil(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS educacion (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    perfil_id   INT NOT NULL DEFAULT 1,
    institucion VARCHAR(100) NOT NULL,
    titulo      VARCHAR(150) NOT NULL,
    periodo     VARCHAR(50)  NOT NULL DEFAULT '',
    descripcion TEXT,
    logo        VARCHAR(255) NOT NULL DEFAULT '',
    FOREIGN KEY (perfil_id) REFERENCES perfil(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS skills (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    perfil_id INT NOT NULL DEFAULT 1,
    nombre    VARCHAR(60) NOT NULL,
    nivel     TINYINT UNSIGNED NOT NULL DEFAULT 50,
    tipo      ENUM('hard', 'soft', 'idioma') NOT NULL DEFAULT 'hard',
    FOREIGN KEY (perfil_id) REFERENCES perfil(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS proyectos (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    perfil_id   INT NOT NULL DEFAULT 1,
    nombre      VARCHAR(100) NOT NULL,
    fecha       DATE NULL,
    descripcion TEXT,
    link        VARCHAR(255) NOT NULL DEFAULT '',
    imagen      VARCHAR(255) NOT NULL DEFAULT '',
    FOREIGN KEY (perfil_id) REFERENCES perfil(id) ON DELETE CASCADE
);

-- Fila inicial del perfil (se edita desde la web con el modo edición)
INSERT IGNORE INTO perfil (id, nombre, titulo, descripcion, email, iframe_url) VALUES
(1, 'Tu Nombre', 'Full Stack Developer Jr',
 'Contá acá quién sos, qué estudiás y qué tipo de trabajo estás buscando. Podés editar este texto desde el modo edición.',
 'tuemail@ejemplo.com',
 'https://www.openstreetmap.org/export/embed.html?bbox=-74.0%2C-56.0%2C-52.0%2C-21.0&layer=mapnik');
