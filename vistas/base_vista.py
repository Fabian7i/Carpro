# base_vista.py
import customtkinter as ctk
from tkinter import ttk
from database import ConexionBD


class VistaBase(ctk.CTkFrame):
    """Clase base para todas las vistas del sistema.
    Proporciona funcionalidad compartida: estilo de tablas, conexión a BD, etc."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.aplicar_estilo_tabla()
    
    @staticmethod
    def aplicar_estilo_tabla():
        """Aplica estilo personalizado a las tablas (Treeview)"""
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            rowheight=25,
            fieldbackground="#2b2b2b",
            bordercolor="#343b47",
            borderwidth=0,
        )
        style.map("Treeview", background=[("selected", "#1f538d")])
        style.configure(
            "Treeview.Heading", background="#1f1f1f", foreground="white", relief="flat"
        )
        style.map("Treeview.Heading", background=[("active", "#2b2b2b")])
    
    def obtener_conexion_bd(self):
        """Obtiene una conexión a la base de datos de forma centralizada"""
        db = ConexionBD()
        conn = db.conectar()
        return db, conn
    
    def cerrar_conexion_bd(self, db):
        """Cierra la conexión a la base de datos de forma centralizada"""
        if db:
            db.desconectar()
    
    def limpiar_tabla(self, tabla):
        """Limpia todos los elementos de una tabla"""
        for item in tabla.get_children():
            tabla.delete(item)
