"""Script para crear o actualizar el usuario administrador."""
import getpass

from config import Config
from database import Database
from models import Usuario

if __name__ == "__main__":
    username = input("Usuario: ").strip()
    password = getpass.getpass("Contraseña: ")
    if not username or not password:
        print("Usuario y contraseña no pueden estar vacíos.")
    else:
        Usuario(Database(Config)).crear(username, password)
        print(f"Listo, el usuario '{username}' ya puede iniciar sesión.")
