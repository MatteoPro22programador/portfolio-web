# Modelo relacional (diseño lógico)

Todas las secciones del portfolio dependen de la tabla `perfil` (relación 1 a N).
La tabla `usuarios` es independiente: solo sirve para el login.

```
usuarios (id PK, username UNIQUE, password_hash)

perfil (id PK, nombre, titulo, descripcion, email, foto, banner, cv, iframe_url)

redes       (id PK, perfil_id FK -> perfil.id, nombre, url, icono)
experiencia (id PK, perfil_id FK -> perfil.id, empresa, puesto, periodo, descripcion, logo)
educacion   (id PK, perfil_id FK -> perfil.id, institucion, titulo, periodo, descripcion, logo)
skills      (id PK, perfil_id FK -> perfil.id, nombre, nivel 0-100, tipo ENUM(hard, soft, idioma))
proyectos   (id PK, perfil_id FK -> perfil.id, nombre, fecha, descripcion, link, imagen)
```

## Relaciones

| Tabla padre | Tabla hija  | Tipo |
|-------------|-------------|------|
| perfil      | redes       | 1 a N |
| perfil      | experiencia | 1 a N |
| perfil      | educacion   | 1 a N |
| perfil      | skills      | 1 a N |
| perfil      | proyectos   | 1 a N |

El diseño físico (tipos de dato, claves, valores por defecto) está en `schema.sql`.
