"""Aplicación principal del portfolio con Flask."""
import os
import uuid
from functools import wraps

import pymysql
from flask import (Flask, abort, flash, redirect, render_template, request,
                   send_from_directory, session, url_for)
from flask_wtf.csrf import CSRFProtect

from config import Config
from database import Database
from forms import LoginForm
from models import Educacion, Experiencia, Perfil, Proyecto, Red, Skill, Usuario

app = Flask(__name__)
app.config.from_object(Config)
CSRFProtect(app)

db = Database(Config)
usuarios = Usuario(db)
perfil = Perfil(db)

# Modelos de cada sección del portfolio
SECCIONES = {
    "redes": Red(db),
    "experiencia": Experiencia(db),
    "educacion": Educacion(db),
    "skills": Skill(db),
    "proyectos": Proyecto(db),
}

os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)


# Funciones auxiliares
def solo_admin(vista):
    """Permite el acceso solo si hay sesión iniciada."""
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get("admin"):
            flash("Tenés que iniciar sesión para editar.", "error")
            return redirect(url_for("login"))
        return vista(*args, **kwargs)
    return envoltura


def guardar_archivo(archivo, permitidas):
    """Guarda un archivo subido y devuelve su ruta relativa."""
    if not archivo or archivo.filename == "":
        return None
    extension = archivo.filename.rsplit(".", 1)[-1].lower()
    if extension not in permitidas:
        return None
    nombre = f"{uuid.uuid4().hex[:12]}.{extension}"
    archivo.save(os.path.join(Config.UPLOAD_FOLDER, nombre))
    return f"uploads/{nombre}"


def leer_formulario(modelo):
    """Obtiene los datos del formulario según los campos del modelo."""
    datos = {}
    for campo in modelo.campos:
        if campo in modelo.archivos:
            ruta = guardar_archivo(request.files.get(campo), modelo.archivos[campo])
            if ruta:
                datos[campo] = ruta
        else:
            datos[campo] = request.form.get(campo, "")
    return datos


def guardar_item(modelo, item_id):
    """Crea o actualiza un elemento del portfolio."""
    datos = leer_formulario(modelo)
    if modelo.faltantes(datos):
        flash("Completá los campos obligatorios.", "error")
        return
    if item_id:
        modelo.actualizar(item_id, datos)
    else:
        modelo.crear(datos)
    flash(f"{modelo.nombre_legible()} guardado.", "ok")


@app.context_processor
def datos_globales():
    """Datos que se usan en todas las plantillas."""
    return {
        "admin": session.get("admin", False),
        "perfil": perfil.obtener(1) or {},
        "redes": SECCIONES["redes"].listar(),
    }


@app.errorhandler(pymysql.MySQLError)
def error_base_de_datos(error):
    return "No se pudo conectar con la base de datos. Revisá el archivo .env.", 500


# Rutas principales
@app.route("/")
def index():
    skills = SECCIONES["skills"].listar()
    grupos = [("hard", "Hard skills"), ("soft", "Soft skills"), ("idioma", "Idiomas")]
    skills_por_tipo = [(titulo, [s for s in skills if s["tipo"] == clave]) for clave, titulo in grupos]
    return render_template(
        "index.html",
        experiencias=SECCIONES["experiencia"].listar(),
        estudios=SECCIONES["educacion"].listar(),
        skills_por_tipo=skills_por_tipo,
        proyectos=SECCIONES["proyectos"].listar(),
    )


@app.route("/cv")
def descargar_cv():
    datos = perfil.obtener(1)
    if not datos or not datos["cv"]:
        flash("Todavía no hay un CV cargado.", "error")
        return redirect(url_for("index"))
    return send_from_directory(app.static_folder, datos["cv"], as_attachment=True,
                               download_name="CV.pdf")


# Login y sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if usuarios.autenticar(form.username.data, form.password.data):
            session.clear()
            session["admin"] = True
            return redirect(url_for("index"))
        flash("Usuario o contraseña incorrectos.", "error")
    return render_template("login.html", form=form)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))


# Edición del contenido
@app.route("/perfil/guardar", methods=["POST"])
@solo_admin
def guardar_perfil():
    guardar_item(perfil, 1)
    return redirect(url_for("index"))


@app.route("/<seccion>/guardar", methods=["POST"])
@solo_admin
def guardar(seccion):
    modelo = SECCIONES.get(seccion)
    if modelo is None:
        abort(404)
    item_id = request.form.get("id", type=int)
    guardar_item(modelo, item_id)
    ancla = "contacto" if seccion == "redes" else seccion
    return redirect(url_for("index") + "#" + ancla)


@app.route("/<seccion>/<int:item_id>/eliminar", methods=["POST"])
@solo_admin
def eliminar(seccion, item_id):
    modelo = SECCIONES.get(seccion)
    if modelo is None:
        abort(404)
    modelo.eliminar(item_id)
    flash(f"{modelo.nombre_legible()} eliminado.", "ok")
    ancla = "contacto" if seccion == "redes" else seccion
    return redirect(url_for("index") + "#" + ancla)


if __name__ == "__main__":
    app.run(debug=True)
