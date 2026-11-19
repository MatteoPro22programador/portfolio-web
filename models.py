"""Modelos y acceso a datos del portfolio."""
from abc import ABC, abstractmethod
from werkzeug.security import generate_password_hash, check_password_hash

# Extensiones permitidas para archivos
IMAGENES = {"png", "jpg", "jpeg", "webp", "gif"}
PDF = {"pdf"}


def url_valida(texto):
    """Devuelve la URL solo si es válida."""
    texto = (texto or "").strip()
    return texto if texto.startswith(("http://", "https://")) else ""


class ItemPortfolio(ABC):
    """Clase base para las secciones del portfolio."""
    tabla = ""
    campos = []
    archivos = {}
    requeridos = []
    orden = "id"

    def __init__(self, db):
        self._db = db

    @abstractmethod
    def nombre_legible(self):
        """Nombre para mostrar en mensajes."""

    def limpiar(self, datos):
        """Filtra y limpia los datos recibidos."""
        return {c: str(datos[c]).strip() for c in self.campos if c in datos}

    def faltantes(self, datos):
        """Comprueba si faltan campos obligatorios."""
        return [c for c in self.requeridos if not str(datos.get(c, "")).strip()]

    def listar(self):
        return self._db.consultar(f"SELECT * FROM {self.tabla} ORDER BY {self.orden}")

    def obtener(self, item_id):
        return self._db.uno(f"SELECT * FROM {self.tabla} WHERE id = %s", (item_id,))

    def crear(self, datos):
        datos = self.limpiar(datos)
        columnas = ", ".join(datos.keys())
        marcas = ", ".join(["%s"] * len(datos))
        sql = f"INSERT INTO {self.tabla} ({columnas}) VALUES ({marcas})"
        return self._db.ejecutar(sql, list(datos.values()))

    def actualizar(self, item_id, datos):
        datos = self.limpiar(datos)
        if not datos:
            return
        cambios = ", ".join(f"{c} = %s" for c in datos)
        sql = f"UPDATE {self.tabla} SET {cambios} WHERE id = %s"
        self._db.ejecutar(sql, list(datos.values()) + [item_id])

    def eliminar(self, item_id):
        self._db.ejecutar(f"DELETE FROM {self.tabla} WHERE id = %s", (item_id,))


# Clases de cada sección del portfolio
class Perfil(ItemPortfolio):
    tabla = "perfil"
    campos = ["nombre", "titulo", "descripcion", "email", "iframe_url", "foto", "banner", "cv"]
    archivos = {"foto": IMAGENES, "banner": IMAGENES, "cv": PDF}
    requeridos = ["nombre", "titulo"]

    def nombre_legible(self):
        return "Perfil"

    def limpiar(self, datos):
        datos = super().limpiar(datos)
        if "iframe_url" in datos:
            datos["iframe_url"] = url_valida(datos["iframe_url"])
        return datos


class Red(ItemPortfolio):
    tabla = "redes"
    campos = ["nombre", "url", "icono"]
    requeridos = ["nombre", "url"]

    def nombre_legible(self):
        return "Red social"

    def limpiar(self, datos):
        datos = super().limpiar(datos)
        if "url" in datos:
            datos["url"] = url_valida(datos["url"])
        return datos


class Experiencia(ItemPortfolio):
    tabla = "experiencia"
    campos = ["empresa", "puesto", "periodo", "descripcion", "logo"]
    archivos = {"logo": IMAGENES}
    requeridos = ["empresa", "puesto"]
    orden = "id DESC"

    def nombre_legible(self):
        return "Experiencia"


class Educacion(ItemPortfolio):
    tabla = "educacion"
    campos = ["institucion", "titulo", "periodo", "descripcion", "logo"]
    archivos = {"logo": IMAGENES}
    requeridos = ["institucion", "titulo"]
    orden = "id DESC"

    def nombre_legible(self):
        return "Estudio"


class Skill(ItemPortfolio):
    tabla = "skills"
    campos = ["nombre", "nivel", "tipo"]
    requeridos = ["nombre"]
    orden = "tipo, id"

    def nombre_legible(self):
        return "Habilidad"

    def limpiar(self, datos):
        datos = super().limpiar(datos)
        if "nivel" in datos:
            try:
                datos["nivel"] = max(0, min(100, int(datos["nivel"])))
            except ValueError:
                datos["nivel"] = 0
        if "tipo" in datos and datos["tipo"] not in ("hard", "soft", "idioma"):
            datos["tipo"] = "hard"
        return datos


class Proyecto(ItemPortfolio):
    tabla = "proyectos"
    campos = ["nombre", "fecha", "descripcion", "link", "imagen"]
    archivos = {"imagen": IMAGENES}
    requeridos = ["nombre"]
    orden = "fecha DESC, id DESC"

    def nombre_legible(self):
        return "Proyecto"

    def limpiar(self, datos):
        datos = super().limpiar(datos)
        if "fecha" in datos:
            datos["fecha"] = datos["fecha"] or None
        if "link" in datos:
            datos["link"] = url_valida(datos["link"])
        return datos

    def _preparar(self, fila):
        """Formatea la fecha para mostrarla y editarla."""
        if fila:
            fecha = fila["fecha"]
            fila["fecha"] = fecha.isoformat() if fecha else ""
            fila["fecha_fmt"] = fecha.strftime("%d/%m/%Y") if fecha else ""
        return fila

    def listar(self):
        return [self._preparar(f) for f in super().listar()]

    def obtener(self, item_id):
        return self._preparar(super().obtener(item_id))


class Usuario:
    """Usuario administrador del portfolio."""

    def __init__(self, db):
        self._db = db

    def autenticar(self, username, password):
        fila = self._db.uno("SELECT password_hash FROM usuarios WHERE username = %s", (username,))
        return bool(fila) and check_password_hash(fila["password_hash"], password)

    def crear(self, username, password):
        """Crea o actualiza el usuario administrador."""
        hash_ = generate_password_hash(password)
        self._db.ejecutar(
            "INSERT INTO usuarios (username, password_hash) VALUES (%s, %s) "
            "ON DUPLICATE KEY UPDATE password_hash = VALUES(password_hash)",
            (username, hash_),
        )
