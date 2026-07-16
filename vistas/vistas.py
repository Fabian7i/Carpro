# vistas.py
import customtkinter as ctk
from tkinter import messagebox, ttk
from database import ConexionBD


# Estilo personalizado para las tablas (Treeview)
def aplicar_estilo_tabla():
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


# ==========================================
# VISTA: MANTENIMIENTO
# ==========================================
class VistaMantenimiento(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        aplicar_estilo_tabla()

        self.titulo = ctk.CTkLabel(
            self,
            text="Gestión de Mantenimientos",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        self.titulo.pack(pady=(15, 5), padx=30, anchor="w")

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # ---- COLUMNA IZQUIERDA: FORMULARIO ----
        self.left_frame = ctk.CTkFrame(self.main_container, width=320, corner_radius=10)
        self.left_frame.pack(side="left", fill="y", padx=(10, 20), pady=10)

        self.lbl_form_title = ctk.CTkLabel(
            self.left_frame,
            text="Nueva Orden",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.lbl_form_title.pack(pady=15)

        self.txt_placa = ctk.CTkEntry(
            self.left_frame, placeholder_text="Placa del Vehículo", width=240
        )
        self.txt_placa.pack(pady=10)

        self.txt_descripcion = ctk.CTkEntry(
            self.left_frame, placeholder_text="Descripción / Falla", width=240
        )
        self.txt_descripcion.pack(pady=10)

        self.txt_costo = ctk.CTkEntry(
            self.left_frame, placeholder_text="Costo Estimado ($)", width=240
        )
        self.txt_costo.pack(pady=10)

        self.cmb_estado = ctk.CTkOptionMenu(
            self.left_frame, values=["Pendiente", "En Proceso", "Completado"], width=240
        )
        self.cmb_estado.pack(pady=10)

        self.btn_guardar_maint = ctk.CTkButton(
            self.left_frame,
            text="Crear Orden",
            fg_color="#3498db",
            hover_color="#2980b9",
            command=self.guardar_mantenimiento,
            width=200,
        )
        self.btn_guardar_maint.pack(pady=20)

        # ---- COLUMNA DERECHA: TABLA ----
        self.right_frame = ctk.CTkFrame(self.main_container, corner_radius=10)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.lbl_table_title = ctk.CTkLabel(
            self.right_frame,
            text="Órdenes de Trabajo Activas",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.lbl_table_title.pack(pady=10)

        self.tabla = ttk.Treeview(
            self.right_frame,
            columns=("ID", "Placa", "Descripción", "Costo", "Estado"),
            show="headings",
        )
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Placa", text="Placa")
        self.tabla.heading("Descripción", text="Descripción")
        self.tabla.heading("Costo", text="Costo")
        self.tabla.heading("Estado", text="Estado")

        self.tabla.column("ID", width=50, anchor="center")
        self.tabla.column("Placa", width=100, anchor="center")
        self.tabla.column("Descripción", width=250, anchor="w")
        self.tabla.column("Costo", width=80, anchor="center")
        self.tabla.column("Estado", width=100, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=15, pady=15)

        self.cargar_mantenimientos()

    def cargar_mantenimientos(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)

        db = ConexionBD()
        conn = db.conectar()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_mantenimiento, placa_vehiculo, descripcion, costo, estado FROM mantenimientos ORDER BY id_mantenimiento DESC;"
            )
            for fila in cursor.fetchall():
                self.tabla.insert("", "end", values=fila)
            cursor.close()
        except Exception as e:
            print(f"Error cargando mantenimientos: {e}")
        finally:
            db.desconectar()

    def guardar_mantenimiento(self):
        placa = self.txt_placa.get().strip().upper()
        descripcion = self.txt_descripcion.get().strip()
        costo = self.txt_costo.get().strip()
        estado = self.cmb_estado.get()

        if not placa or not descripcion or not costo:
            messagebox.showwarning(
                "Campos Incompletos", "Por favor, completa todos los campos."
            )
            return

        db = ConexionBD()
        conn = db.conectar()
        if conn is None:
            messagebox.showerror("Error", "Error al conectar a base de datos.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT placa FROM vehiculos WHERE placa = %s;", (placa,))
            if not cursor.fetchone():
                messagebox.showerror(
                    "No Encontrado", f"La placa '{placa}' no existe en el sistema."
                )
                cursor.close()
                return

            cursor.execute(
                "INSERT INTO mantenimientos (placa_vehiculo, descripcion, costo, estado) VALUES (%s, %s, %s, %s);",
                (placa, descripcion, costo, estado),
            )
            conn.commit()
            messagebox.showinfo("¡Éxito!", "Orden creada correctamente.")
            self.limpiar_formulario()
            self.cargar_mantenimientos()
            cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al guardar:\n{e}")
        finally:
            db.desconectar()

    def limpiar_formulario(self):
        self.txt_placa.delete(0, "end")
        self.txt_descripcion.delete(0, "end")
        self.txt_costo.delete(0, "end")
        self.cmb_estado.set("Pendiente")


# ==========================================
# VISTA: VEHÍCULOS (PARCHE APLICADO)
# ==========================================
class VistaVehiculos(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        aplicar_estilo_tabla()

        self.titulo = ctk.CTkLabel(
            self, text="Registro de Vehículos", font=ctk.CTkFont(size=22, weight="bold")
        )
        self.titulo.pack(pady=(15, 5), padx=30, anchor="w")

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # ---- COLUMNA IZQUIERDA: FORMULARIO ----
        self.left_frame = ctk.CTkFrame(self.main_container, width=320, corner_radius=10)
        self.left_frame.pack(side="left", fill="y", padx=(10, 20), pady=10)

        self.lbl_form_title = ctk.CTkLabel(
            self.left_frame,
            text="Nuevo Vehículo",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.lbl_form_title.pack(pady=15)

        self.txt_placa = ctk.CTkEntry(
            self.left_frame, placeholder_text="Placa (Ej: ABC-123)", width=240
        )
        self.txt_placa.pack(pady=10)

        self.txt_marca = ctk.CTkEntry(
            self.left_frame, placeholder_text="Marca (Ej: Toyota)", width=240
        )
        self.txt_marca.pack(pady=10)

        self.txt_modelo = ctk.CTkEntry(
            self.left_frame, placeholder_text="Modelo (Ej: Hilux)", width=240
        )
        self.txt_modelo.pack(pady=10)

        self.txt_anio = ctk.CTkEntry(
            self.left_frame, placeholder_text="Año (Ej: 2024)", width=240
        )
        self.txt_anio.pack(pady=10)

        self.btn_guardar = ctk.CTkButton(
            self.left_frame,
            text="Guardar Vehículo",
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=self.guardar_vehiculo,
            width=200,
        )
        self.btn_guardar.pack(pady=20)

        # ---- COLUMNA DERECHA: TABLA ----
        self.right_frame = ctk.CTkFrame(self.main_container, corner_radius=10)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.lbl_table_title = ctk.CTkLabel(
            self.right_frame,
            text="Flota Registrada",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.lbl_table_title.pack(pady=10)

        self.tabla = ttk.Treeview(
            self.right_frame,
            columns=("Placa", "Marca", "Modelo", "Año"),
            show="headings",
        )
        self.tabla.heading("Placa", text="Placa")
        self.tabla.heading("Marca", text="Marca")
        self.tabla.heading("Modelo", text="Modelo")
        self.tabla.heading("Año", text="Año")

        self.tabla.column("Placa", width=100, anchor="center")
        self.tabla.column("Marca", width=120, anchor="center")
        self.tabla.column("Modelo", width=150, anchor="center")
        self.tabla.column("Año", width=100, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=15, pady=15)

        self.cargar_vehiculos()

    def cargar_vehiculos(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)

        db = ConexionBD()
        conn = db.conectar()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT placa, marca, modelo, anio FROM vehiculos ORDER BY placa ASC;"
            )
            for fila in cursor.fetchall():
                self.tabla.insert("", "end", values=fila)
            cursor.close()
        except Exception as e:
            print(f"Error cargando vehículos: {e}")
        finally:
            db.desconectar()

    def guardar_vehiculo(self):
        placa = self.txt_placa.get().strip().upper()
        marca = self.txt_marca.get().strip()
        modelo = self.txt_modelo.get().strip()
        anio = self.txt_anio.get().strip()

        if not placa or not marca or not modelo or not anio:
            messagebox.showwarning(
                "Campos Incompletos", "Por favor, llena todos los campos."
            )
            return

        db = ConexionBD()
        conn = db.conectar()
        if conn is None:
            messagebox.showerror("Error", "Error al conectar con Supabase.")
            return

        try:
            cursor = conn.cursor()

            # PARCHE: Insertamos id_cliente = 1 de forma temporal para evitar el error de restricción (NOT NULL)
            # NOTA: Asegúrate de que el id_cliente '1' exista en tu tabla de clientes de Supabase.
            # Si usas otro id, simplemente cambia el '1' de abajo por tu ID real.
            query = """
                INSERT INTO vehiculos (placa, marca, modelo, anio, id_cliente) 
                VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(query, (placa, marca, modelo, anio, 1))

            conn.commit()
            messagebox.showinfo("¡Éxito!", f"Vehículo {placa} guardado.")
            self.limpiar_formulario()
            self.cargar_vehiculos()
            cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al guardar:\n{e}")
        finally:
            db.desconectar()

    def limpiar_formulario(self):
        self.txt_placa.delete(0, "end")
        self.txt_marca.delete(0, "end")
        self.txt_modelo.delete(0, "end")
        self.txt_anio.delete(0, "end")

        # ==========================================


# VISTA: CLIENTES (NUEVO MÓDULO)
# ==========================================
class VistaClientes(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        aplicar_estilo_tabla()

        self.titulo = ctk.CTkLabel(
            self, text="Gestión de Clientes", font=ctk.CTkFont(size=22, weight="bold")
        )
        self.titulo.pack(pady=(15, 5), padx=30, anchor="w")

        # Contenedor Principal (Formulario a la izquierda, Tabla a la derecha)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # ---- COLUMNA IZQUIERDA: FORMULARIO ----
        self.left_frame = ctk.CTkFrame(self.main_container, width=320, corner_radius=10)
        self.left_frame.pack(side="left", fill="y", padx=(10, 20), pady=10)

        self.lbl_form_title = ctk.CTkLabel(
            self.left_frame,
            text="Nuevo Cliente",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.lbl_form_title.pack(pady=15)

        self.txt_nombre = ctk.CTkEntry(
            self.left_frame, placeholder_text="Nombre Completo", width=240
        )
        self.txt_nombre.pack(pady=10)

        self.txt_telefono = ctk.CTkEntry(
            self.left_frame, placeholder_text="Teléfono / Celular", width=240
        )
        self.txt_telefono.pack(pady=10)

        self.txt_correo = ctk.CTkEntry(
            self.left_frame, placeholder_text="Correo Electrónico", width=240
        )
        self.txt_correo.pack(pady=10)

        self.btn_guardar = ctk.CTkButton(
            self.left_frame,
            text="Registrar Cliente",
            fg_color="#e67e22",
            hover_color="#d35400",
            command=self.guardar_cliente,
            width=200,
        )
        self.btn_guardar.pack(pady=20)

        # ---- COLUMNA DERECHA: TABLA ----
        self.right_frame = ctk.CTkFrame(self.main_container, corner_radius=10)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.lbl_table_title = ctk.CTkLabel(
            self.right_frame,
            text="Clientes Registrados",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.lbl_table_title.pack(pady=10)

        # Estructura del Treeview para Clientes
        self.tabla = ttk.Treeview(
            self.right_frame,
            columns=("ID", "Nombre", "Teléfono", "Correo"),
            show="headings",
        )
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Teléfono", text="Teléfono")
        self.tabla.heading("Correo", text="Correo")

        self.tabla.column("ID", width=60, anchor="center")
        self.tabla.column("Nombre", width=200, anchor="w")
        self.tabla.column("Teléfono", width=120, anchor="center")
        self.tabla.column("Correo", width=200, anchor="w")

        self.tabla.pack(fill="both", expand=True, padx=15, pady=15)

        self.cargar_clientes()

    def cargar_clientes(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)

        db = ConexionBD()
        conn = db.conectar()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            # Asegúrate de que los nombres de las columnas coincidan con tu tabla de clientes
            cursor.execute(
                "SELECT id_cliente, nombre, telefono, correo FROM clientes ORDER BY id_cliente ASC;"
            )
            for fila in cursor.fetchall():
                self.tabla.insert("", "end", values=fila)
            cursor.close()
        except Exception as e:
            print(f"Error cargando clientes: {e}")
        finally:
            db.desconectar()

    def guardar_cliente(self):
        nombre = self.txt_nombre.get().strip()
        telefono = self.txt_telefono.get().strip()
        correo = self.txt_correo.get().strip()

        if not nombre or not telefono:
            messagebox.showwarning(
                "Campos Incompletos",
                "Por favor, ingresa al menos el Nombre y Teléfono.",
            )
            return

        db = ConexionBD()
        conn = db.conectar()
        if conn is None:
            messagebox.showerror("Error", "Error al conectar con la base de datos.")
            return

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO clientes (nombre, telefono, correo) 
                VALUES (%s, %s, %s);
            """
            cursor.execute(query, (nombre, telefono, correo))
            conn.commit()

            messagebox.showinfo(
                "¡Éxito!", f"Cliente '{nombre}' registrado correctamente."
            )
            self.limpiar_formulario()
            self.cargar_clientes()
            cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar al cliente:\n{e}")
        finally:
            db.desconectar()

    def limpiar_formulario(self):
        self.txt_nombre.delete(0, "end")
        self.txt_telefono.delete(0, "end")
        self.txt_correo.delete(0, "end")
