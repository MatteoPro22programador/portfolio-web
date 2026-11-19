# Portfolio web — Flask + MySQL

Proyecto integrador: portfolio con modo edición protegido por login.

## Cómo correrlo en VS Code

1. Abrí la carpeta en VS Code y abrí una terminal.
2. Entorno virtual e instalación:
   ```
   python -m venv venv
   venv\Scripts\activate        (Windows)   |   source venv/bin/activate   (Mac/Linux)
   pip install -r requirements.txt
   ```
3. Creá la base en MySQL:  `CREATE DATABASE portfolio CHARACTER SET utf8mb4;`
4. Copiá `.env.example` como `.env` y completá usuario/contraseña de MySQL.
5. Creá las tablas (con `ejemplo` carga datos de prueba):
   ```
   python crear_tablas.py ejemplo
   ```
6. Creá tu usuario para editar:
   ```
   python crear_admin.py
   ```
7. Arrancá:
   ```
   python app.py
   ```
   Abrí http://127.0.0.1:5000 — con **Login** entrás al modo edición.

## Estructura

| Archivo | Qué hace |
|---|---|
| `app.py` | Rutas de Flask |
| `models.py` | Clases (POO) que hablan con la base |
| `database.py` | Conexión a MySQL |
| `forms.py` | Formulario de login (Flask-WTF) |
| `config.py` | Configuración y variables de entorno |
| `schema.sql` | Diseño físico de la base |
| `docs/modelo_relacional.md` | Diseño lógico |
| `templates/` | HTML con Jinja2 |
| `static/css/style.css` | Estilos (colores en `:root`) |
| `static/js/main.js` | Modales y animaciones |

## Dónde está cada requisito del enunciado

- **Jinja2**: `templates/` (`base.html` se hereda en `index.html` y `login.html`).
- **Iframe**: sección Contacto de `index.html` (el link se edita desde el perfil).
- **Íconos / fuentes**: FontAwesome y Google Fonts en `base.html`. Favicon y logo en `static/img/`.
- **POO, 4 pilares**: `models.py`, cada uno marcado con comentario
  (ABSTRACCIÓN, HERENCIA, ENCAPSULAMIENTO, POLIMORFISMO).
- **Responsive**: al final de `style.css`, tres tamaños (escritorio / tablet ≤900px / mobile ≤640px).
- **Animaciones** (para indicar en la entrega):
  1. Círculos de skills que se llenan al aparecer (`.skill-barra` en CSS + `llenarSkill` en `main.js`).
  2. Secciones que aparecen con fade al hacer scroll (`.reveal`).
  3. Hover en botones, tarjetas de proyectos e ítems (transition en CSS).
- **Login**: hash de contraseña (werkzeug) + Flask-WTF (formulario y protección CSRF).
- **CV en PDF**: se sube desde el modal de editar perfil y aparece el botón "Descargar CV".
- **Base de datos**: MySQL, variables `MYSQL_ADDON_*` de Clever Cloud ya soportadas.

## Publicarlo

Flask necesita un servidor que ejecute Python, así que **GitHub Pages y Netlify no sirven para esta app**.
Opciones: Render, Railway o PythonAnywhere (el `Procfile` ya está listo para gunicorn).
Cargá en el panel las variables de entorno de `.env.example` con los datos de tu base de Clever Cloud.

Ojo: en servidores gratuitos la carpeta `static/uploads/` puede borrarse al reiniciar,
y las fotos/CV subidos se pierden. Si pasa, volvé a subirlos o consultá a tu profe cómo lo prefiere.

## Qué falta hacer vos

- Cambiar los datos de ejemplo y subir tu foto, banner, logos y CV (desde el modo edición).
- Reemplazar `static/img/logo.svg` y `favicon.svg` por tu logo.
- La documentación en PDF (planificación, objetivo, etc.) con las pautas que te dé el instituto.
