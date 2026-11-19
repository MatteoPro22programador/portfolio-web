"""Crea las tablas de la base de datos ejecutando schema.sql.

Uso:
    python crear_tablas.py            -> solo crea las tablas
    python crear_tablas.py ejemplo    -> además carga datos de ejemplo
"""
import sys

from config import Config
from database import Database


def correr_sql(db, archivo):
    with open(archivo, encoding="utf-8") as f:
        # sacamos los comentarios y separamos las sentencias por ";"
        lineas = [l for l in f.read().splitlines() if not l.strip().startswith("--")]
    for sentencia in "\n".join(lineas).split(";"):
        if sentencia.strip():
            db.ejecutar(sentencia)


if __name__ == "__main__":
    db = Database(Config)
    correr_sql(db, "schema.sql")
    print("Tablas creadas.")
    if len(sys.argv) > 1 and sys.argv[1] == "ejemplo":
        correr_sql(db, "datos_ejemplo.sql")
        print("Datos de ejemplo cargados.")
