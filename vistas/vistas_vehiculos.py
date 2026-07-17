# vistas/vistas_vehiculos.py
import customtkinter as ctk
from tkinter import messagebox, ttk
from database import ConexionBD
from vistas.base_vista import VistaBase
from modelos import Vehiculo


class VistaVehiculos(VistaBase):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.titulo = ctk.CTkLabel(
            self, text="Registro de Vehículos", font=ctk.CTkFont(size=22, weight="bold")
        )
        self.titulo.pack(pady=(15, 5), padx=30, anchor="w")

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Diccionario para mapear la opción del menú ("DNI - Nombre") con su id_cliente real
        self.clientes_map = {}

        # ---- COLUMNA IZQUIERDA: FORMULARIO ----
        self.left_frame = ctk.CTkFrame(self.main_container, width=320, corner_radius=10)
        self.left_frame.pack(side="left", fill="y", padx=(10, 20), pady=10)

        self.lbl_form_title = ctk.CTkLabel(
            self.left_frame,
            text="Nuevo Vehículo",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.lbl_form_title.pack(pady=15)

        # Selector de Cliente Asociado
        self.lbl_cliente = ctk.CTkLabel(
            self.left_frame, text="Propietario / Cliente:", font=ctk.CTkFont(size=12)
        )
        self.lbl_cliente.pack(anchor="w", padx=40, pady=(5, 0))

        self.cmb_cliente = ctk.CTkOptionMenu(
            self.left_frame, values=["Cargando clientes..."], width=240
        )
        self.cmb_cliente.pack(pady=(0, 10))

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

        self.txt_kilometraje = ctk.CTkEntry(
            self.left_frame, placeholder_text="Kilometraje Inicial", width=240
        )
        self.txt_kilometraje.pack(pady=10)

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

        # Estructura del Treeview para Vehículos según tu esquema SQL
        self.tabla = ttk.Treeview(
            self.right_frame,
            columns=("Placa", "Marca", "Modelo", "Año", "Kilometraje", "Propietario"),
            show="headings",
        )
        self.tabla.heading("Placa", text="Placa")
        self.tabla.heading("Marca", text="Marca")
        self.tabla.heading("Modelo", text="Modelo")
        self.tabla.heading("Año", text="Año")
        self.tabla.heading("Kilometraje", text="Kilometraje")
        self.tabla.heading("Propietario", text="Propietario")

        self.tabla.column("Placa", width=80, anchor="center")
        self.tabla.column("Marca", width=100, anchor="center")
        self.tabla.column("Modelo", width=120, anchor="center")
        self.tabla.column("Año", width=60, anchor="center")
        self.tabla.column("Kilometraje", width=90, anchor="center")
        self.tabla.column("Propietario", width=180, anchor="w")

        self.tabla.pack(fill="both", expand=True, padx=15, pady=15)

        # Cargar datos iniciales
        self.cargar_clientes_combobox()
        self.cargar_vehiculos()

    def cargar_clientes_combobox(self):
        """Busca los clientes en Render y los carga en el CTkOptionMenu"""
        db, conn = self.obtener_conexion_bd()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_cliente, ruc, nombre FROM clientes ORDER BY nombre ASC;"
            )
            filas = cursor.fetchall()

            opciones = []
            self.clientes_map.clear()

            for fila in filas:
                id_cli, ruc, nombre = fila
                # Formateamos usando la variable ruc en lugar de dni
                label = f"{ruc} - {nombre}"
                opciones.append(label)
                self.clientes_map[label] = id_cli

            if opciones:
                self.cmb_cliente.configure(values=opciones)
                self.cmb_cliente.set(opciones[0])
            else:
                self.cmb_cliente.configure(values=["No hay clientes registrados"])
                self.cmb_cliente.set("No hay clientes registrados")

            cursor.close()
        except Exception as e:
            print(f"Error cargando combo de clientes: {e}")
        finally:
            self.cerrar_conexion_bd(db)

    def cargar_vehiculos(self):
        """Carga la lista de vehículos cruzando el nombre del dueño desde 'clientes'"""
        self.limpiar_tabla(self.tabla)
        db, conn = self.obtener_conexion_bd()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            # Hacemos un INNER JOIN para traer el nombre del cliente propietario
            query = """
                SELECT v.placa, v.marca, v.modelo, v.anio, v.kilometraje, c.nombre 
                FROM vehiculos v
                INNER JOIN clientes c ON v.id_cliente = c.id_cliente
                ORDER BY v.id_vehiculo DESC;
            """
            cursor.execute(query)
            for fila in cursor.fetchall():
                self.tabla.insert("", "end", values=fila)
            cursor.close()
        except Exception as e:
            print(f"Error cargando vehículos: {e}")
        finally:
            self.cerrar_conexion_bd(db)

    def guardar_vehiculo(self):
        cliente_seleccionado = self.cmb_cliente.get()
        placa = self.txt_placa.get().strip().upper()
        marca = self.txt_marca.get().strip()
        modelo = self.txt_modelo.get().strip()
        anio = self.txt_anio.get().strip()
        km_texto = self.txt_kilometraje.get().strip()

        # Validar si hay un cliente seleccionado válido
        if cliente_seleccionado in [
            "Cargando clientes...",
            "No hay clientes registrados",
        ]:
            messagebox.showwarning(
                "Falta Cliente", "Debes registrar y seleccionar un cliente primero."
            )
            return

        id_cliente = self.clientes_map.get(cliente_seleccionado)

        # Si el kilometraje está vacío, lo dejamos en 0 por defecto
        kilometraje = int(km_texto) if km_texto.isdigit() else 0

        # Usamos el modelo Vehiculo para validación
        vehiculo = Vehiculo(
            id_cliente=id_cliente,
            placa=placa,
            marca=marca,
            modelo=modelo,
            anio=int(anio) if anio.isdigit() else None,
            kilometraje=kilometraje,
        )
        valido, mensaje = vehiculo.validar()

        if not valido:
            messagebox.showwarning("Campos Incompletos", mensaje)
            return

        db, conn = self.obtener_conexion_bd()
        if conn is None:
            messagebox.showerror("Error", "Error al conectar con Supabase.")
            return

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO vehiculos (id_cliente, placa, marca, modelo, anio, kilometraje) 
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(
                query, (id_cliente, placa, marca, modelo, int(anio), kilometraje)
            )
            conn.commit()

            messagebox.showinfo(
                "¡Éxito!",
                f"Vehículo con placa {placa} guardado y asignado correctamente.",
            )
            self.limpiar_formulario()
            self.cargar_vehiculos()
            cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al guardar vehículo:\n{e}")
        finally:
            self.cerrar_conexion_bd(db)

    def limpiar_formulario(self):
        self.txt_placa.delete(0, "end")
        self.txt_marca.delete(0, "end")
        self.txt_modelo.delete(0, "end")
        self.txt_anio.delete(0, "end")
        self.txt_kilometraje.delete(0, "end")
