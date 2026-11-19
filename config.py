"""Configuración del proyecto."""
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "cambia-esta-clave-en-produccion")
    SESSION_COOKIE_SAMESITE = "Lax"

    # Base de datos
    DB_HOST = os.getenv("MYSQL_ADDON_HOST") or os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("MYSQL_ADDON_PORT") or os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("MYSQL_ADDON_USER") or os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("MYSQL_ADDON_PASSWORD") or os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("MYSQL_ADDON_DB") or os.getenv("DB_NAME", "portfolio")

    # Archivos subidos
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
