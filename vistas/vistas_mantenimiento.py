# vistas/vistas_mantenimiento.py
import customtkinter as ctk
from tkinter import messagebox, ttk
from database import ConexionBD
from vistas.vistasClientes import aplicar_estilo_tabla


class VistaMantenimiento(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        aplicar_estilo_tabla()

        self.titulo = ctk.CTkLabel(
            self,
            text="Gestión de Órdenes de Trabajo",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        self.titulo.pack(pady=(15, 5), padx=30, anchor="w")

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Mapeos en memoria
        self.vehiculos_map = {}

        # ---- COLUMNA IZQUIERDA: FORMULARIO ----
        self.left_frame = ctk.CTkFrame(self.main_container, width=320, corner_radius=10)
        self.left_frame.pack(side="left", fill="y", padx=(10, 20), pady=10)

        self.lbl_form_title = ctk.CTkLabel(
            self.left_frame,
            text="Nueva Orden",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.lbl_form_title.pack(pady=15)

        self.lbl_vehiculo = ctk.CTkLabel(
            self.left_frame, text="Seleccionar Vehículo:", font=ctk.CTkFont(size=12)
        )
        self.lbl_vehiculo.pack(anchor="w", padx=40, pady=(5, 0))

        self.cmb_vehiculo = ctk.CTkOptionMenu(
            self.left_frame, values=["Cargando vehículos..."], width=240
        )
        self.cmb_vehiculo.pack(pady=(0, 10))

        self.txt_diagnostico = ctk.CTkEntry(
            self.left_frame, placeholder_text="Diagnóstico Inicial / Falla", width=240
        )
        self.txt_diagnostico.pack(pady=10)

        self.cmb_estado = ctk.CTkOptionMenu(
            self.left_frame,
            values=["Pendiente", "En Proceso", "Finalizado", "Entregado"],
            width=240,
        )
        self.cmb_estado.pack(pady=10)

        self.btn_guardar_maint = ctk.CTkButton(
            self.left_frame,
            text="Crear Orden",
            fg_color="#3498db",
            hover_color="#2980b9",
            command=self.guardar_orden,
            width=200,
        )
        self.btn_guardar_maint.pack(pady=15)

        # ---- COLUMNA DERECHA: TABLA Y ACCIONES ----
        self.right_frame = ctk.CTkFrame(self.main_container, corner_radius=10)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.lbl_table_title = ctk.CTkLabel(
            self.right_frame,
            text="Historial de Órdenes",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.lbl_table_title.pack(pady=10)

        # Tabla de Órdenes
        self.tabla = ttk.Treeview(
            self.right_frame,
            columns=("ID", "Placa", "Diagnóstico", "Total", "Estado", "Fecha"),
            show="headings",
        )
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Placa", text="Placa")
        self.tabla.heading("Diagnóstico", text="Diagnóstico")
        self.tabla.heading("Total", text="Total")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.heading("Fecha", text="Fecha Ingreso")

        self.tabla.column("ID", width=50, anchor="center")
        self.tabla.column("Placa", width=90, anchor="center")
        self.tabla.column("Diagnóstico", width=180, anchor="w")
        self.tabla.column("Total", width=90, anchor="center")
        self.tabla.column("Estado", width=100, anchor="center")
        self.tabla.column("Fecha", width=120, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=15, pady=10)

        # ---- BARRA DE BOTONES DE ACCIÓN RÁPIDA ----
        self.action_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.action_frame.pack(fill="x", padx=15, pady=(0, 15))

        self.btn_add_servicio = ctk.CTkButton(
            self.action_frame,
            text="+ Agregar Servicio",
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=self.abrir_agregar_servicio,
            width=140,
        )
        self.btn_add_servicio.pack(side="left", padx=5)

        self.btn_add_repuesto = ctk.CTkButton(
            self.action_frame,
            text="+ Agregar Repuesto",
            fg_color="#e67e22",
            hover_color="#d35400",
            command=self.abrir_agregar_repuesto,
            width=140,
        )
        self.btn_add_repuesto.pack(side="left", padx=5)

        self.btn_ver_detalles = ctk.CTkButton(
            self.action_frame,
            text="Ver Resumen / Boleta",
            fg_color="#9b59b6",
            hover_color="#8e44ad",
            command=self.abrir_resumen_orden,
            width=150,
        )
        self.btn_ver_detalles.pack(side="right", padx=5)
        self.btn_ver_detalle = ctk.CTkButton(
            self.action_frame,
            text="Ver Detalle Completo",
            command=self.abrir_ventana_detalle,
        )
        self.btn_ver_detalle.pack(side="right", padx=5)
        # Cargar datos iniciales
        self.cargar_vehiculos_combobox()
        self.cargar_ordenes()

   
    def abrir_ventana_detalle(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una orden de la lista.")
            return
        
        id_orden = self.tabla.item(seleccion[0])["values"][0]

        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Detalle Completo - Orden #{id_orden}")
        ventana.geometry("750x700")
        ventana.grab_set()

        db = ConexionBD()
        conn = db.conectar()
        if conn:
            cursor = conn.cursor()
            
            # --- TABLA SERVICIOS (Usando nombres exactos de tus entidades) ---
            ctk.CTkLabel(ventana, text="Servicios Realizados:", font=("Arial", 14, "bold")).pack(anchor="w", padx=25, pady=(15, 5))
            tabla_serv = ttk.Treeview(ventana, columns=("Servicio", "Obs", "Costo"), show="headings", height=5)
            tabla_serv.heading("Servicio", text="Servicio")
            tabla_serv.heading("Obs", text="Observaciones")
            tabla_serv.heading("Costo", text="Costo")
            tabla_serv.column("Costo", width=80, anchor="center")
            tabla_serv.pack(fill="x", padx=20)

            # Consulta ajustada a: id_servicio_cat, observaciones_tecnicas y precio_mano_obra
            cursor.execute("""
                SELECT s.nombre_servicio, d.observaciones_tecnicas, s.precio_mano_obra 
                FROM detalle_servicios d 
                JOIN servicios_catalogo s ON d.id_servicio_cat = s.id_servicio_cat 
                WHERE d.id_orden = %s
            """, (id_orden,))
            
            for row in cursor.fetchall(): 
                # row[0]: nombre, row[1]: observaciones_tecnicas, row[2]: precio_mano_obra
                tabla_serv.insert("", "end", values=(row[0], row[1], f"S/. {float(row[2]):.2f}"))

            # --- TABLA REPUESTOS ---
            ctk.CTkLabel(ventana, text="Repuestos Utilizados:", font=("Arial", 14, "bold")).pack(anchor="w", padx=25, pady=(15, 5))
            tabla_rep = ttk.Treeview(ventana, columns=("Rep", "Cant", "Precio"), show="headings", height=5)
            tabla_rep.heading("Rep", text="Repuesto")
            tabla_rep.heading("Cant", text="Cantidad")
            tabla_rep.heading("Precio", text="Precio Unit.")
            tabla_rep.column("Cant", width=80, anchor="center")
            tabla_rep.pack(fill="x", padx=20)

            # Consulta ajustada a: id_repuesto y precio_unitario_aplicado
            cursor.execute("""
                SELECT r.nombre_repuesto, d.cantidad_usada, d.precio_unitario_aplicado 
                FROM detalle_repuestos d 
                JOIN repuestos r ON d.id_repuesto = r.id_repuesto 
                WHERE d.id_orden = %s
            """, (id_orden,))
            for row in cursor.fetchall(): 
                tabla_rep.insert("", "end", values=(row[0], row[1], f"S/. {float(row[2]):.2f}"))

            cursor.close()
            db.desconectar()

        ctk.CTkButton(ventana, text="Cerrar", command=ventana.destroy).pack(pady=20)
   
   
        # 1. Obtener la orden seleccionada
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una orden de la lista.")
            return
        
        id_orden = self.tabla.item(seleccion[0])["values"][0]

        # 2. Configuración de la ventana
        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Detalle Completo - Orden #{id_orden}")
        ventana.geometry("750x700")
        ventana.grab_set()

        db = ConexionBD()
        conn = db.conectar()
        if conn:
            cursor = conn.cursor()
            
            # --- CABECERA ---
            # (Mantén aquí tu lógica de consulta de datos del cliente)
            
            # --- TABLA SERVICIOS (CORREGIDA CON SUS CAMPOS REALES) ---
            ctk.CTkLabel(ventana, text="Servicios Realizados:", font=("Arial", 14, "bold")).pack(anchor="w", padx=25, pady=(15, 5))
            tabla_serv = ttk.Treeview(ventana, columns=("Servicio", "Obs", "Costo"), show="headings", height=5)
            tabla_serv.heading("Servicio", text="Servicio")
            tabla_serv.heading("Obs", text="Observaciones")
            tabla_serv.heading("Costo", text="Costo")
            tabla_serv.column("Costo", width=80, anchor="center")
            tabla_serv.pack(fill="x", padx=20)

            # Consulta usando los nombres de tu DDL: precio_mano_obra y observaciones
            cursor.execute("""
                SELECT s.nombre_servicio, d.observaciones, s.precio_mano_obra 
                FROM detalle_servicios d 
                JOIN servicios_catalogo s ON d.id_servicio_cat = s.id_servicio 
                WHERE d.id_orden = %s
            """, (id_orden,))
            
            for row in cursor.fetchall(): 
                # row[2] es el precio_mano_obra
                tabla_serv.insert("", "end", values=(row[0], row[1], f"S/. {float(row[2]):.2f}"))

            # --- TABLA REPUESTOS ---
            # (Asegúrate de que los campos en tu tabla repuestos coincidan)
            ctk.CTkLabel(ventana, text="Repuestos Utilizados:", font=("Arial", 14, "bold")).pack(anchor="w", padx=25, pady=(15, 5))
            tabla_rep = ttk.Treeview(ventana, columns=("Rep", "Cant"), show="headings", height=5)
            tabla_rep.heading("Rep", text="Repuesto")
            tabla_rep.heading("Cant", text="Cantidad")
            tabla_rep.column("Cant", width=80, anchor="center")
            tabla_rep.pack(fill="x", padx=20)

            cursor.execute("""
                SELECT r.nombre_repuesto, d.cantidad_usada 
                FROM detalle_repuestos d 
                JOIN repuestos r ON d.id_repuesto = r.id_repuesto 
                WHERE d.id_orden = %s
            """, (id_orden,))
            for row in cursor.fetchall(): 
                tabla_rep.insert("", "end", values=row)

            cursor.close()
            db.desconectar()

        ctk.CTkButton(ventana, text="Cerrar", command=ventana.destroy).pack(pady=20)
   
   
   
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una orden de la lista.")
            return
        
        id_orden = self.tabla.item(seleccion[0])["values"][0]

        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Detalle Completo - Orden #{id_orden}")
        ventana.geometry("750x700")
        ventana.grab_set()

        db = ConexionBD()
        conn = db.conectar()
        if conn:
            cursor = conn.cursor()
            
            # --- CABECERA ---
            query_cabecera = """
                SELECT v.placa, v.modelo, u.nombre, c.nombre AS nombre_cliente, o.fecha_ingreso
                FROM ordenes_trabajo o
                JOIN vehiculos v ON o.id_vehiculo = v.id_vehiculo
                JOIN usuarios u ON o.id_usuario = u.id_usuario
                JOIN clientes c ON v.id_cliente = c.id_cliente
                WHERE o.id_orden = %s;
            """
            cursor.execute(query_cabecera, (id_orden,))
            datos = cursor.fetchone()

            if datos:
                ctk.CTkLabel(ventana, text="Detalles del Servicio", font=("Arial", 18, "bold")).pack(pady=10)
                info_text = f"Cliente: {datos[3]}  |  Vehículo: {datos[0]} ({datos[1]})\nAtendido por: {datos[2]}  |  Fecha: {datos[4]}"
                ctk.CTkLabel(ventana, text=info_text, font=("Arial", 13)).pack(pady=5, padx=20)

                # --- TABLA SERVICIOS (CON COSTO) ---
                ctk.CTkLabel(ventana, text="Servicios Realizados:", font=("Arial", 14, "bold")).pack(anchor="w", padx=25, pady=(15, 5))
                tabla_serv = ttk.Treeview(ventana, columns=("Servicio", "Obs", "Costo"), show="headings", height=5)
                tabla_serv.heading("Servicio", text="Servicio")
                tabla_serv.heading("Obs", text="Observaciones")
                tabla_serv.heading("Costo", text="Costo")
                tabla_serv.column("Costo", width=80, anchor="center")
                tabla_serv.pack(fill="x", padx=20)

                cursor.execute("""
                    SELECT s.nombre_servicio, d.observaciones_tecnicas, s.precio 
                    FROM detalle_servicios d 
                    JOIN servicios_catalogo s ON d.id_servicio_cat = s.id_servicio 
                    WHERE d.id_orden = %s
                """, (id_orden,))
                for row in cursor.fetchall(): 
                    # Formateamos el precio aquí mismo
                    tabla_serv.insert("", "end", values=(row[0], row[1], f"S/. {row[2]:.2f}"))

                # --- TABLA REPUESTOS ---
                ctk.CTkLabel(ventana, text="Repuestos Utilizados:", font=("Arial", 14, "bold")).pack(anchor="w", padx=25, pady=(15, 5))
                tabla_rep = ttk.Treeview(ventana, columns=("Rep", "Cant"), show="headings", height=5)
                tabla_rep.heading("Rep", text="Repuesto")
                tabla_rep.heading("Cant", text="Cantidad")
                tabla_rep.column("Cant", width=80, anchor="center")
                tabla_rep.pack(fill="x", padx=20)

                cursor.execute("""
                    SELECT r.nombre_repuesto, d.cantidad_usada 
                    FROM detalle_repuestos d 
                    JOIN repuestos r ON d.id_repuesto = r.id_repuesto 
                    WHERE d.id_orden = %s
                """, (id_orden,))
                for row in cursor.fetchall(): 
                    tabla_rep.insert("", "end", values=row)

            cursor.close()
            db.desconectar()

        ctk.CTkButton(ventana, text="Cerrar", command=ventana.destroy).pack(pady=20)
    
    
        # 1. Obtener la orden seleccionada (asegura que tu método existe)
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una orden de la lista.")
            return
        
        id_orden = self.tabla.item(seleccion[0])["values"][0]

        # 2. Configuración de la ventana
        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Detalle Completo - Orden #{id_orden}")
        ventana.geometry("750x650")
        ventana.grab_set()

        # 3. Conexión y consulta principal
        db = ConexionBD()
        conn = db.conectar()
        if conn:
            cursor = conn.cursor()
            
            # --- Consulta Cabecera ---
            query_cabecera = """
                SELECT v.placa, v.modelo, u.nombre, c.nombre AS nombre_cliente, o.fecha_ingreso
                FROM ordenes_trabajo o
                JOIN vehiculos v ON o.id_vehiculo = v.id_vehiculo
                JOIN usuarios u ON o.id_usuario = u.id_usuario
                JOIN clientes c ON v.id_cliente = c.id_cliente
                WHERE o.id_orden = %s;
            """
            cursor.execute(query_cabecera, (id_orden,))
            datos = cursor.fetchone()

            if datos:
                # Mostrar datos del cliente
                info_text = f"Cliente: {datos[3]}  |  Vehículo: {datos[0]} ({datos[1]})\nAtendido por: {datos[2]}  |  Fecha: {datos[4]}"
                ctk.CTkLabel(ventana, text="Detalles del Servicio", font=("Arial", 18, "bold")).pack(pady=10)
                ctk.CTkLabel(ventana, text=info_text, font=("Arial", 13)).pack(pady=5, padx=20)

                # --- TABLA SERVICIOS ---
                ctk.CTkLabel(ventana, text="Servicios Realizados:", font=("Arial", 14, "bold")).pack(anchor="w", padx=25, pady=(15, 5))
                tabla_serv = ttk.Treeview(ventana, columns=("Servicio", "Obs"), show="headings", height=5)
                tabla_serv.heading("Servicio", text="Servicio")
                tabla_serv.heading("Obs", text="Observaciones")
                tabla_serv.column("Servicio", width=200)
                tabla_serv.pack(fill="x", padx=20)

                cursor.execute("""
                    SELECT s.nombre_servicio, d.observaciones_tecnicas 
                    FROM detalle_servicios d 
                    JOIN servicios_catalogo s ON d.id_servicio_cat = s.id_servicio 
                    WHERE d.id_orden = %s
                """, (id_orden,))
                for row in cursor.fetchall(): tabla_serv.insert("", "end", values=row)

                # --- TABLA REPUESTOS ---
                ctk.CTkLabel(ventana, text="Repuestos Utilizados:", font=("Arial", 14, "bold")).pack(anchor="w", padx=25, pady=(15, 5))
                tabla_rep = ttk.Treeview(ventana, columns=("Rep", "Cant"), show="headings", height=5)
                tabla_rep.heading("Rep", text="Repuesto")
                tabla_rep.heading("Cant", text="Cantidad")
                tabla_rep.column("Cant", width=80, anchor="center")
                tabla_rep.pack(fill="x", padx=20)

                cursor.execute("""
                    SELECT r.nombre_repuesto, d.cantidad_usada 
                    FROM detalle_repuestos d 
                    JOIN repuestos r ON d.id_repuesto = r.id_repuesto 
                    WHERE d.id_orden = %s
                """, (id_orden,))
                for row in cursor.fetchall(): tabla_rep.insert("", "end", values=row)

            cursor.close()
            db.desconectar()

        ctk.CTkButton(ventana, text="Cerrar", command=ventana.destroy).pack(pady=20)
    
    
    
        id_orden = self.obtener_orden_seleccionada()
        if not id_orden: return

        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Detalle Completo - Orden #{id_orden}")
        ventana.geometry("700x600")
        ventana.grab_set()

        # --- CABECERA: Datos del Cliente y Vehículo ---
        db = ConexionBD()
        conn = db.conectar()
        if conn:
            cursor = conn.cursor()
            query = """
                SELECT v.placa, v.modelo, u.nombre, c.nombre AS nombre_cliente, o.fecha_ingreso
                FROM ordenes_trabajo o
                JOIN vehiculos v ON o.id_vehiculo = v.id_vehiculo
                JOIN usuarios u ON o.id_usuario = u.id_usuario
                JOIN clientes c ON v.id_cliente = c.id_cliente
                WHERE o.id_orden = %s;
            """
            cursor.execute(query, (id_orden,))
            datos = cursor.fetchone()

            if datos:
                ctk.CTkLabel(ventana, text="Información de la Orden", font=("Arial", 16, "bold")).pack(pady=10)
                info_frame = ctk.CTkFrame(ventana)
                info_frame.pack(fill="x", padx=20, pady=5)
                
                txt = f"Cliente: {datos[3]}  |  Vehículo: {datos[0]} ({datos[1]})\nAtendido por: {datos[2]}  |  Fecha: {datos[4]}"
                ctk.CTkLabel(info_frame, text=txt, justify="left").pack(pady=10, padx=10)

                # --- TABLA SERVICIOS ---
                ctk.CTkLabel(ventana, text="Servicios:", font=("Arial", 13, "bold")).pack(anchor="w", padx=25, pady=(10,0))
                tabla_serv = ttk.Treeview(ventana, columns=("Servicio", "Obs"), show="headings", height=5)
                tabla_serv.heading("Servicio", text="Servicio")
                tabla_serv.heading("Obs", text="Observaciones")
                tabla_serv.pack(fill="x", padx=20, pady=5)

                cursor.execute("SELECT s.nombre_servicio, d.observaciones_tecnicas FROM detalle_servicios d JOIN servicios_catalogo s ON d.id_servicio = s.id_servicio WHERE d.id_orden = %s", (id_orden,))
                for row in cursor.fetchall(): tabla_serv.insert("", "end", values=row)

                # --- TABLA REPUESTOS ---
                ctk.CTkLabel(ventana, text="Repuestos:", font=("Arial", 13, "bold")).pack(anchor="w", padx=25, pady=(10,0))
                tabla_rep = ttk.Treeview(ventana, columns=("Rep", "Cant"), show="headings", height=5)
                tabla_rep.heading("Rep", text="Repuesto")
                tabla_rep.heading("Cant", text="Cantidad")
                tabla_rep.column("Cant", width=80, anchor="center")
                tabla_rep.pack(fill="x", padx=20, pady=5)

                cursor.execute("SELECT r.nombre_repuesto, d.cantidad_usada FROM detalle_repuestos d JOIN repuestos r ON d.id_repuesto = r.id_repuesto WHERE d.id_orden = %s", (id_orden,))
                for row in cursor.fetchall(): tabla_rep.insert("", "end", values=row)

            cursor.close()
            db.desconectar()

        ctk.CTkButton(ventana, text="Cerrar", command=ventana.destroy).pack(pady=20)
    
        id_orden = self.obtener_orden_seleccionada()
        if not id_orden: return

        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Detalle Completo - Orden #{id_orden}")
        ventana.geometry("700x550")
        
        # --- Cabecera con datos del cliente ---
        # (Aquí ejecuta la consulta SQL nueva de arriba y guarda en 'datos')
        header_frame = ctk.CTkFrame(ventana)
        header_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(header_frame, text=f"Cliente: {datos[3]} | Vehículo: {datos[0]} ({datos[1]})", font=("Arial", 14, "bold")).pack(pady=5)

        # --- Cuadrícula de Servicios ---
        ctk.CTkLabel(ventana, text="Servicios Realizados:").pack(anchor="w", padx=20)
        tabla_serv = ttk.Treeview(ventana, columns=("Servicio"), show="headings", height=5)
        tabla_serv.heading("Servicio", text="Servicio")
        tabla_serv.pack(fill="x", padx=20, pady=5)

        # --- Cuadrícula de Repuestos ---
        ctk.CTkLabel(ventana, text="Repuestos Utilizados:").pack(anchor="w", padx=20)
        tabla_rep = ttk.Treeview(ventana, columns=("Repuesto", "Cant"), show="headings", height=5)
        tabla_rep.heading("Repuesto", text="Repuesto")
        tabla_rep.heading("Cant", text="Cantidad")
        tabla_rep.column("Cant", width=80, anchor="center")
        tabla_rep.pack(fill="x", padx=20, pady=5)

        # Carga los datos en tabla_serv y tabla_rep usando cursor.fetchall()
        # ... (Tu lógica de llenado de tablas aquí) ...
    def cargar_vehiculos_combobox(self):
        db = ConexionBD()
        conn = db.conectar()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_vehiculo, placa, marca, modelo FROM vehiculos ORDER BY placa ASC;"
            )
            filas = cursor.fetchall()

            opciones = []
            self.vehiculos_map.clear()

            for fila in filas:
                id_veh, placa, marca, modelo = fila
                label = f"{placa} ({marca} {modelo})"
                opciones.append(label)
                self.vehiculos_map[label] = id_veh

            if opciones:
                self.cmb_vehiculo.configure(values=opciones)
                self.cmb_vehiculo.set(opciones[0])
            else:
                self.cmb_vehiculo.configure(values=["No hay vehículos registrados"])
                self.cmb_vehiculo.set("No hay vehículos registrados")

            cursor.close()
        except Exception as e:
            print(f"Error cargando combobox de vehículos: {e}")
        finally:
            db.desconectar()

    def cargar_ordenes(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)

        db = ConexionBD()
        conn = db.conectar()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            query = """
                SELECT o.id_orden, v.placa, o.diagnostico_inicial, o.total_pagar, o.estado, 
                       TO_CHAR(o.fecha_ingreso, 'DD-MM-YYYY HH24:MI') as fecha
                FROM ordenes_trabajo o
                INNER JOIN vehiculos v ON o.id_vehiculo = v.id_vehiculo
                ORDER BY o.id_orden DESC;
            """
            cursor.execute(query)
            for fila in cursor.fetchall():
                # Formatear el total para mostrarlo como moneda local
                id_o, placa, diag, total, est, fec = fila
                self.tabla.insert(
                    "", "end", values=(id_o, placa, diag, f"S/. {total:.2f}", est, fec)
                )
            cursor.close()
        except Exception as e:
            print(f"Error cargando órdenes: {e}")
        finally:
            db.desconectar()

    def guardar_orden(self):
        vehiculo_seleccionado = self.cmb_vehiculo.get()
        diagnostico = self.txt_diagnostico.get().strip()
        estado = self.cmb_estado.get()

        if vehiculo_seleccionado in [
            "Cargando vehículos...",
            "No hay vehículos registrados",
        ]:
            messagebox.showwarning(
                "Falta Vehículo", "Debes registrar y seleccionar un vehículo primero."
            )
            return

        id_vehiculo = self.vehiculos_map.get(vehiculo_seleccionado)

        if not diagnostico:
            messagebox.showwarning(
                "Campos Incompletos", "Por favor, ingresa el diagnóstico inicial."
            )
            return

        db = ConexionBD()
        conn = db.conectar()
        if conn is None:
            messagebox.showerror("Error", "Error al conectar con la base de datos.")
            return

        try:
            cursor = conn.cursor()
            # El total_pagar inicia en 0.00 y se irá calculando dinámicamente con los servicios/repuestos
            query = """
                INSERT INTO ordenes_trabajo (id_vehiculo, id_usuario, diagnostico_inicial, total_pagar, estado) 
                VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(query, (id_vehiculo, 1, diagnostico, 0.00, estado))
            conn.commit()

            messagebox.showinfo(
                "¡Éxito!",
                "Orden de trabajo inicial creada. Ahora puedes agregarle servicios y repuestos.",
            )
            self.txt_diagnostico.delete(0, "end")
            self.cargar_ordenes()
            cursor.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la orden:\n{e}")
        finally:
            db.desconectar()

    # ---- OBTENER SELECCIÓN ACTIVA DE LA TABLA ----
    def obtener_orden_seleccionada(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Atención", "Por favor, selecciona una orden de la lista primero."
            )
            return None
        valores = self.tabla.item(seleccion[0], "values")
        return valores[0]  # Retorna el id_orden

    # ---- VENTANA EMERGENTE: AGREGAR SERVICIO ----
    def abrir_agregar_servicio(self):
        id_orden = self.obtener_orden_seleccionada()
        if not id_orden:
            return

        ventana = ctk.CTkToplevel(self)
        ventana.title("Agregar Servicio a Orden")
        ventana.geometry("400x350")
        ventana.resizable(False, False)
        ventana.grab_set()  # Bloquea la ventana de atrás

        lbl_tit = ctk.CTkLabel(
            ventana,
            text=f"Agregar Servicio (Orden #{id_orden})",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        lbl_tit.pack(pady=15)

        # Cargar catálogo de servicios
        db = ConexionBD()
        conn = db.conectar()
        servicios_map = {}
        opciones = []
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_servicio, nombre_servicio, precio_mano_obra FROM servicios_catalogo ORDER BY nombre_servicio ASC;"
            )
            for fila in cursor.fetchall():
                id_s, nom, precio = fila
                label = f"{nom} (S/. {precio:.2f})"
                opciones.append(label)
                servicios_map[label] = (id_s, precio)
            cursor.close()
            db.desconectar()

        if not opciones:
            opciones = ["No hay servicios en catálogo"]

        cmb_serv = ctk.CTkOptionMenu(ventana, values=opciones, width=300)
        cmb_serv.pack(pady=15)

        txt_obs = ctk.CTkEntry(
            ventana, placeholder_text="Observaciones técnicas (opcional)", width=300
        )
        txt_obs.pack(pady=15)

        def registrar_servicio_detalle():
            sel = cmb_serv.get()
            if sel == "No hay servicios en catálogo":
                return

            id_serv_cat, precio = servicios_map[sel]
            obs = txt_obs.get().strip()

            db_conn = ConexionBD()
            conn_ins = db_conn.conectar()
            if conn_ins:
                try:
                    cursor = conn_ins.cursor()
                    # 1. Insertar detalle
                    cursor.execute(
                        "INSERT INTO detalle_servicios (id_orden, id_servicio_cat, observaciones_tecnicas) VALUES (%s, %s, %s);",
                        (id_orden, id_serv_cat, obs),
                    )
                    # 2. Actualizar costo total en la cabecera
                    cursor.execute(
                        "UPDATE ordenes_trabajo SET total_pagar = total_pagar + %s WHERE id_orden = %s;",
                        (precio, id_orden),
                    )
                    conn_ins.commit()
                    cursor.close()
                    messagebox.showinfo("¡Éxito!", "Servicio añadido correctamente.")
                    self.cargar_ordenes()
                    ventana.destroy()
                except Exception as ex:
                    messagebox.showerror(
                        "Error", f"No se pudo guardar el detalle:\n{ex}"
                    )
                finally:
                    db_conn.desonectar()

        btn_add = ctk.CTkButton(
            ventana,
            text="Confirmar y Guardar",
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=registrar_servicio_detalle,
        )
        btn_add.pack(pady=20)

    def ver_resumen_orden(self, id_orden):
        db = ConexionBD()
        conn = db.conectar()
        if conn:
            cursor = conn.cursor()
            # Consulta que trae toda la info solicitada
            query = """SELECT v.placa, v.modelo, u.nombre_usuario, o.fecha_ingreso, o.total_pagar 
                       FROM ordenes_trabajo o
                       JOIN vehiculos v ON o.id_vehiculo = v.id_vehiculo
                       JOIN usuarios u ON o.id_usuario = u.id_usuario
                       WHERE o.id_orden = %s;"""
            cursor.execute(query, (id_orden,))
            datos_orden = cursor.fetchone()

            # Consulta para listar los servicios incluidos
            cursor.execute(
                "SELECT nombre_servicio FROM detalle_servicios d JOIN servicios_catalogo s ON d.id_servicio_cat = s.id_servicio WHERE d.id_orden = %s;",
                (id_orden,),
            )
            servicios = cursor.fetchall()

            # Aquí puedes poblar tu interfaz
            print(
                f"Orden: {id_orden}, Vehículo: {datos_orden[0]}, Usuario: {datos_orden[2]}, Fecha: {datos_orden[3]}"
            )
            print(f"Servicios incluidos: {len(servicios)}")

            cursor.close()
            db.desconectar()

    # ---- VENTANA EMERGENTE: AGREGAR REPUESTO ----
    def abrir_agregar_repuesto(self):
        id_orden = self.obtener_orden_seleccionada()
        if not id_orden:
            return

        ventana = ctk.CTkToplevel(self)
        ventana.title("Agregar Repuesto a Orden")
        ventana.geometry("400x400")
        ventana.resizable(False, False)
        ventana.grab_set()

        lbl_tit = ctk.CTkLabel(
            ventana,
            text=f"Agregar Repuesto (Orden #{id_orden})",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        lbl_tit.pack(pady=15)

        # Cargar catálogo de repuestos
        db = ConexionBD()
        conn = db.conectar()
        repuestos_map = {}
        opciones = []
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_repuesto, nombre_repuesto, precio_venta, stock_actual FROM repuestos WHERE stock_actual > 0 ORDER BY nombre_repuesto ASC;"
            )
            for fila in cursor.fetchall():
                id_r, nom, precio, stock = fila
                label = f"{nom} (Stock: {stock} | S/. {precio:.2f})"
                opciones.append(label)
                repuestos_map[label] = (id_r, precio, stock)
            cursor.close()
            db.desconectar()

        if not opciones:
            opciones = ["No hay repuestos con stock disponible"]

        cmb_rep = ctk.CTkOptionMenu(ventana, values=opciones, width=300)
        cmb_rep.pack(pady=15)

        txt_cant = ctk.CTkEntry(
            ventana, placeholder_text="Cantidad a usar (Ej: 1)", width=300
        )
        txt_cant.pack(pady=15)

        def registrar_repuesto_detalle():
            sel = cmb_rep.get()
            if sel == "No hay repuestos con stock disponible":
                return

            id_rep, precio, stock = repuestos_map[sel]
            cant_txt = txt_cant.get().strip()

            if not cant_txt.isdigit() or int(cant_txt) <= 0:
                messagebox.showwarning(
                    "Cantidad Inválida", "Por favor ingresa un número entero positivo."
                )
                return

            cantidad = int(cant_txt)
            if cantidad > stock:
                messagebox.showerror(
                    "Sin Stock",
                    f"No puedes usar {cantidad} unidades. El stock disponible es {stock}.",
                )
                return

            costo_adicional = precio * cantidad

            db_conn = ConexionBD()
            conn_ins = db_conn.conectar()
            if conn_ins:
                try:
                    cursor = conn_ins.cursor()
                    # 1. Insertar en detalle_repuestos
                    cursor.execute(
                        "INSERT INTO detalle_repuestos (id_orden, id_repuesto, cantidad_usada, precio_unitario_aplicado) VALUES (%s, %s, %s, %s);",
                        (id_orden, id_rep, cantidad, precio),
                    )
                    # 2. Descontar del inventario de repuestos
                    cursor.execute(
                        "UPDATE repuestos SET stock_actual = stock_actual - %s WHERE id_repuesto = %s;",
                        (cantidad, id_rep),
                    )
                    # 3. Actualizar costo total de la cabecera
                    cursor.execute(
                        "UPDATE ordenes_trabajo SET total_pagar = total_pagar + %s WHERE id_orden = %s;",
                        (costo_adicional, id_orden),
                    )
                    conn_ins.commit()
                    cursor.close()
                    messagebox.showinfo(
                        "¡Éxito!", "Repuesto asignado y stock actualizado."
                    )
                    self.cargar_ordenes()
                    ventana.destroy()
                except Exception as ex:
                    messagebox.showerror(
                        "Error", f"Fallo al procesar el repuesto:\n{ex}"
                    )
                finally:
                    db_conn.desonectar()

        btn_add = ctk.CTkButton(
            ventana,
            text="Agregar e Inventariar",
            fg_color="#e67e22",
            hover_color="#d35400",
            command=registrar_repuesto_detalle,
        )
        btn_add.pack(pady=20)

    # ---- VENTANA EMERGENTE: RESUMEN / BOLETA DE LA ORDEN ----
    def abrir_resumen_orden(self):
        id_orden = self.obtener_orden_seleccionada()
        if not id_orden:
            return

        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Resumen de Cuenta - Orden #{id_orden}")
        ventana.geometry("550x500")
        ventana.resizable(True, True)
        ventana.grab_set()

        lbl_tit = ctk.CTkLabel(
            ventana,
            text=f"Boleta / Detalles - Trabajo #{id_orden}",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        lbl_tit.pack(pady=15)

        # Caja de texto para dar un formato clásico y profesional de ticket
        txt_resumen = ctk.CTkTextbox(
            ventana, width=500, height=350, font=("Consolas", 12)
        )
        txt_resumen.pack(pady=10, padx=20)

        db = ConexionBD()
        conn = db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                # 1. Obtener cabecera y datos del auto/cliente
                query_info = """
                    SELECT v.placa, v.marca, v.modelo, c.nombre, o.diagnostico_inicial, o.total_pagar, o.estado
                    FROM ordenes_trabajo o
                    INNER JOIN vehiculos v ON o.id_vehiculo = v.id_vehiculo
                    INNER JOIN clientes c ON v.id_cliente = c.id_cliente
                    WHERE o.id_orden = %s;
                """
                cursor.execute(query_info, (id_orden,))
                cabecera = cursor.fetchone()

                # 2. Obtener servicios asociados
                query_serv = """
                    SELECT s.nombre_servicio, s.precio_mano_obra 
                    FROM detalle_servicios d
                    INNER JOIN servicios_catalogo s ON d.id_servicio_cat = s.id_servicio_cat
                    WHERE d.id_orden = %s;
                """
                cursor.execute(query_serv, (id_orden,))
                servicios = cursor.fetchall()

                # 3. Obtener repuestos aplicados
                query_rep = """
                    SELECT r.nombre_repuesto, d.cantidad_usada, d.precio_unitario_aplicado, (d.cantidad_usada * d.precio_unitario_aplicado) as total
                    FROM detalle_repuestos d
                    INNER JOIN repuestos r ON d.id_repuesto = r.id_repuesto
                    WHERE d.id_orden = %s;
                """
                cursor.execute(query_rep, (id_orden,))
                repuestos = cursor.fetchall()

                # Formatear el ticket
                placa, marca, mod, cliente, diag, total, est = cabecera
                ticket = "==================================================\n"
                ticket += "                 AUTOPRO TALLER                   \n"
                ticket += "==================================================\n"
                ticket += f" ORDEN DE TRABAJO: #{id_orden}\n"
                ticket += f" CLIENTE:         {cliente}\n"
                ticket += f" VEHÍCULO:        {marca} {mod} [{placa}]\n"
                ticket += f" ESTADO ACTUAL:   {est.upper()}\n"
                ticket += f" DIAGNÓSTICO:     {diag}\n"
                ticket += "--------------------------------------------------\n"
                ticket += " SERVICIOS / MANO DE OBRA:\n"

                if servicios:
                    for s in servicios:
                        ticket += f"  - {s[0]:<30} S/. {s[1]:>8.2f}\n"
                else:
                    ticket += "  * Ninguno asignado todavía.\n"

                ticket += "--------------------------------------------------\n"
                ticket += " REPUESTOS UTILIZADOS:\n"
                if repuestos:
                    for r in repuestos:
                        item = f"{r[1]}x {r[0]}"
                        ticket += f"  - {item:<30} S/. {r[3]:>8.2f}\n"
                else:
                    ticket += "  * Ninguno asignado todavía.\n"

                ticket += "==================================================\n"
                ticket += f" TOTAL A PAGAR:                  S/. {total:>8.2f}\n"
                ticket += "==================================================\n"

                txt_resumen.insert("0.0", ticket)
                txt_resumen.configure(state="disabled")  # Bloquear escritura

                cursor.close()
            except Exception as e:
                print(f"Error cargando el resumen: {e}")
            finally:
                db.desconectar()

        btn_cerrar = ctk.CTkButton(
            ventana, text="Cerrar Resumen", command=ventana.destroy
        )
        btn_cerrar.pack(pady=10)
