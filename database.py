"""Acceso a la base de datos MySQL."""
import pymysql


class Database:
    def __init__(self, config):
        self._host = config.DB_HOST
        self._port = config.DB_PORT
        self._user = config.DB_USER
        self._password = config.DB_PASSWORD
        self._name = config.DB_NAME

    def _conectar(self):
        return pymysql.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database=self._name,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

    def consultar(self, sql, params=None):
        """SELECT que devuelve una lista de filas."""
        conexion = self._conectar()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        finally:
            conexion.close()

    def uno(self, sql, params=None):
        """SELECT que devuelve solo una fila (o None)."""
        filas = self.consultar(sql, params)
        return filas[0] if filas else None

    def ejecutar(self, sql, params=None):
        """INSERT / UPDATE / DELETE. Devuelve el id insertado."""
        conexion = self._conectar()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.lastrowid
        finally:
            conexion.close()
