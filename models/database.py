import sqlite3
from pathlib import Path
from tkinter import messagebox

class Database:
    def __init__(self, db_file='database.db', sql_folder='SQL', schema_file='schema.sql'):
        self.sql_folder = Path(sql_folder).resolve()
        self.sql_folder.mkdir(exist_ok=True)
        self.db_file = self.sql_folder / db_file
        self.conn = None
        self.connect()
        self.load_schema(schema_file)

    def connect(self):
        #Establece la conexión con SQLite"""
        self.conn = sqlite3.connect(self.db_file)
        self.conn.execute("PRAGMA foreign_keys = ON")

    def close(self):
        #Cierra la conexión"""
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute(self, sql_file, params=None):
        #Ejecuta un archivo SQL tipo stored procedure"""
        file_path = self.sql_folder / sql_file
        with open(file_path, 'r', encoding='utf-8') as f:
            sql = f.read()
        cursor = self.conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        self.conn.commit()
        return cursor

    def query(self, sql_file, params=None):
        #Ejecuta un SQL de consulta y devuelve resultados"""
        cursor = self.execute(sql_file, params)
        return cursor.fetchall()

    def load_schema(self, schema_file):
        #Carga el schema inicial de la base si no existe"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            # Primer mensaje
            messagebox.showinfo("Database", "Base de datos no encontrada, Creando Base de datos..")
            
            # Ejecuta el schema
            schema_path = self.sql_folder / schema_file
            with open(schema_path, 'r', encoding='utf-8') as f:
                sql = f.read()
            cursor.executescript(sql)
            self.conn.commit()

            # Mensaje de éxito
            messagebox.showinfo("Base de datos", "Base de datos Creada Satisfactoriamente.")
        else:
            # Mensaje si ya existe
            messagebox.showinfo("Base de datos", "Base de datos Cargada Previamente.")
