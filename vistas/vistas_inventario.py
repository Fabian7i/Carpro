# vistas/vistas_inventario.py
import customtkinter as ctk
from tkinter import messagebox, ttk
from database import ConexionBD
from vistas.base_vista import VistaBase
from modelos import Repuesto, ServicioCatalogo


class VistaInventario(VistaBase):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.titulo = ctk.CTkLabel(
            self,
            text="Inventario de Repuestos & Catálogo de Servicios",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        self.titulo.pack(pady=(15, 5), padx=30, anchor="w")

        # Contenedor con dos columnas (Izquierda: Repuestos, Derecha: Servicios)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # =========================================================================
        # SECCIÓN IZQUIERDA: REPUESTOS
        # =========================================================================
        self.frame_repuestos = ctk.CTkFrame(self.main_container, corner_radius=10)
        self.frame_repuestos.pack(
            side="left", fill="both", expand=True, padx=(0, 10), pady=10
        )

        self.lbl_rep = ctk.CTkLabel(
            self.frame_repuestos,
            text="Gestión de Repuestos",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.lbl_rep.pack(pady=10)

        # Formulario interno de repuestos
        self.form_rep = ctk.CTkFrame(self.frame_repuestos, fg_color="transparent")
        self.form_rep.pack(fill="x", padx=15, pady=5)

        self.txt_rep_nombre = ctk.CTkEntry(
            self.form_rep, placeholder_text="Nombre del repuesto", width=180
        )
        self.txt_rep_nombre.grid(row=0, column=0, padx=5, pady=5)

        self.txt_rep_codigo = ctk.CTkEntry(
            self.form_rep, placeholder_text="Código de parte", width=120
        )
        self.txt_rep_codigo.grid(row=0, column=1, padx=5, pady=5)

        self.txt_rep_precio = ctk.CTkEntry(
            self.form_rep, placeholder_text="Precio Venta (S/.)", width=120
        )
        self.txt_rep_precio.grid(row=1, column=0, padx=5, pady=5)

        self.txt_rep_stock = ctk.CTkEntry(
            self.form_rep, placeholder_text="Stock Inicial", width=120
        )
        self.txt_rep_stock.grid(row=1, column=1, padx=5, pady=5)

        self.btn_guardar_rep = ctk.CTkButton(
            self.frame_repuestos,
            text="Registrar Repuesto",
            fg_color="#e67e22",
            hover_color="#d35400",
            command=self.guardar_repuesto,
            width=180,
        )
        self.btn_guardar_rep.pack(pady=10)

        # Tabla de repuestos
        self.tabla_repuestos = ttk.Treeview(
            self.frame_repuestos,
            columns=("Código", "Nombre", "Precio", "Stock"),
            show="headings",
            height=10,
        )
        self.tabla_repuestos.heading("Código", text="Código")
        self.tabla_repuestos.heading("Nombre", text="Nombre")
        self.tabla_repuestos.heading("Precio", text="Precio")
        self.tabla_repuestos.heading("Stock", text="Stock")

        self.tabla_repuestos.column("Código", width=80, anchor="center")
        self.tabla_repuestos.column("Nombre", width=150, anchor="w")
        self.tabla_repuestos.column("Precio", width=80, anchor="center")
        self.tabla_repuestos.column("Stock", width=60, anchor="center")
        self.tabla_repuestos.pack(fill="both", expand=True, padx=15, pady=10)

        # =========================================================================
        # SECCIÓN DERECHA: SERVICIOS CATALOGO
        # =========================================================================
        self.frame_servicios = ctk.CTkFrame(self.main_container, corner_radius=10)
        self.frame_servicios.pack(
            side="right", fill="both", expand=True, padx=(10, 0), pady=10
        )

        self.lbl_serv = ctk.CTkLabel(
            self.frame_servicios,
            text="Catálogo de Servicios (Tarifas)",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.lbl_serv.pack(pady=10)

        # Formulario interno de servicios
        self.form_serv = ctk.CTkFrame(self.frame_servicios, fg_color="transparent")
        self.form_serv.pack(fill="x", padx=15, pady=5)

        self.txt_serv_nombre = ctk.CTkEntry(
            self.form_serv,
            placeholder_text="Nombre del servicio (Ej: Cambio de Aceite)",
            width=200,
        )
        self.txt_serv_nombre.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        self.txt_serv_precio = ctk.CTkEntry(
            self.form_serv, placeholder_text="Costo Mano de Obra", width=120
        )
        self.txt_serv_precio.pack(side="left", padx=5, pady=5)

        self.btn_guardar_serv = ctk.CTkButton(
            self.frame_servicios,
            text="Registrar Servicio",
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=self.guardar_servicio,
            width=180,
        )
        self.btn_guardar_serv.pack(pady=10)

        # Tabla de servicios
        self.tabla_servicios = ttk.Treeview(
            self.frame_servicios,
            columns=("Nombre", "Costo"),
            show="headings",
            height=10,
        )
        self.tabla_servicios.heading("Nombre", text="Nombre del Servicio")
        self.tabla_servicios.heading("Costo", text="Mano de Obra")

        self.tabla_servicios.column("Nombre", width=220, anchor="w")
        self.tabla_servicios.column("Costo", width=100, anchor="center")
        self.tabla_servicios.pack(fill="both", expand=True, padx=15, pady=10)

        # Cargar datos iniciales
        self.cargar_repuestos()
        self.cargar_servicios()

    def cargar_repuestos(self):
        self.limpiar_tabla(self.tabla_repuestos)
        db, conn = self.obtener_conexion_bd()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT codigo_parte, nombre_repuesto, precio_venta, stock_actual FROM repuestos ORDER BY stock_actual ASC;"
                )
                for fila in cursor.fetchall():
                    self.tabla_repuestos.insert(
                        "",
                        "end",
                        values=(fila[0], fila[1], f"S/. {fila[2]:.2f}", fila[3]),
                    )
                cursor.close()
            except Exception as e:
                print(f"Error al cargar repuestos: {e}")
            finally:
                self.cerrar_conexion_bd(db)

    def eliminar_servicio(self):
        item_seleccionado = self.tabla_servicios.selection()
        if not item_seleccionado:
            messagebox.showwarning(
                "Selección", "Selecciona un servicio de la tabla para eliminar."
            )
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este servicio?"):
            valores = self.tabla_servicios.item(item_seleccionado, "values")
            nombre_servicio = valores[0]

            db = ConexionBD()
            conn = db.conectar()
            if conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM servicios_catalogo WHERE nombre_servicio = %s;",
                    (nombre_servicio,),
                )
                conn.commit()
                cursor.close()
                db.desconectar()
                self.cargar_servicios()

    def guardar_servicio(self):
        nombre = self.txt_serv_nombre.get().strip()
        precio_txt = self.txt_serv_precio.get().strip()

        if not nombre or not precio_txt:
            messagebox.showwarning(
                "Campos vacíos", "Por favor completa todos los datos del servicio."
            )
            return

        try:
            precio = float(precio_txt)
        except ValueError:
            messagebox.showwarning("Error", "El costo debe ser un número válido.")
            return

        db = ConexionBD()
        conn = db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                # Insertamos en la tabla de servicios
                cursor.execute(
                    "INSERT INTO servicios_catalogo (nombre_servicio, precio_mano_obra) VALUES (%s, %s);",
                    (nombre, precio),
                )
                conn.commit()
                cursor.close()
                messagebox.showinfo("Éxito", "Servicio registrado en el catálogo.")

                # Limpiar y refrescar
                self.txt_serv_nombre.delete(0, "end")
                self.txt_serv_precio.delete(0, "end")
                self.cargar_servicios()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}")
            finally:
                db.desonectar()

    def obtener_servicios_catalogo(self):
        servicios = []
        db = ConexionBD()
        conn = db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                # Esta consulta trae los nombres de los servicios que registras en VistaInventario
                cursor.execute(
                    "SELECT nombre_servicio FROM servicios_catalogo ORDER BY nombre_servicio ASC;"
                )
                servicios = [fila[0] for fila in cursor.fetchall()]
                cursor.close()
            except Exception as e:
                print(f"Error al obtener catálogo: {e}")
            finally:
                db.desconectar()
        return servicios

    def guardar_repuesto(self):
        nombre = self.txt_rep_nombre.get().strip()
        codigo = self.txt_rep_codigo.get().strip().upper()
        precio_txt = self.txt_rep_precio.get().strip()
        stock_txt = self.txt_rep_stock.get().strip()

        try:
            precio = float(precio_txt)
            stock = int(stock_txt)
        except ValueError:
            messagebox.showwarning(
                "Error de formato",
                "Precio debe ser un número decimal y el Stock un entero.",
            )
            return

        # Usamos el modelo Repuesto para validación
        repuesto = Repuesto(
            nombre_repuesto=nombre,
            codigo_parte=codigo,
            precio_venta=precio,
            stock_actual=stock,
        )
        valido, mensaje = repuesto.validar()

        if not valido:
            messagebox.showwarning("Campos vacíos", mensaje)
            return

        db, conn = self.obtener_conexion_bd()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO repuestos (nombre_repuesto, codigo_parte, precio_venta, stock_actual) VALUES (%s, %s, %s, %s);",
                    (nombre, codigo, precio, stock),
                )
                conn.commit()
                cursor.close()
                messagebox.showinfo("Completado", "Repuesto guardado con éxito.")
                self.txt_rep_nombre.delete(0, "end")
                self.txt_rep_codigo.delete(0, "end")
                self.txt_rep_precio.delete(0, "end")
                self.txt_rep_stock.delete(0, "end")
                self.cargar_repuestos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el repuesto: {e}")
            finally:
                self.cerrar_conexion_bd(db)

    def cargar_servicios(self):
        self.limpiar_tabla(self.tabla_servicios)
        db, conn = self.obtener_conexion_bd()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT nombre_servicio, precio_mano_obra FROM servicios_catalogo ORDER BY nombre_servicio ASC;"
                )
                for fila in cursor.fetchall():
                    self.tabla_servicios.insert(
                        "", "end", values=(fila[0], f"S/. {fila[1]:.2f}")
                    )
                cursor.close()
            except Exception as e:
                print(f"Error al cargar servicios: {e}")
            finally:
                self.cerrar_conexion_bd(db)

    def guardar_servicio(self):
        nombre = self.txt_serv_nombre.get().strip()
        precio_txt = self.txt_serv_precio.get().strip()

        try:
            precio = float(precio_txt)
        except ValueError:
            messagebox.showwarning(
                "Error de formato",
                "El costo de la mano de obra debe ser un número válido.",
            )
            return

        # Usamos el modelo ServicioCatalogo para validación
        servicio = ServicioCatalogo(nombre_servicio=nombre, precio_mano_obra=precio)
        valido, mensaje = servicio.validar()

        if not valido:
            messagebox.showwarning("Campos vacíos", mensaje)
            return

        db, conn = self.obtener_conexion_bd()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO servicios_catalogo (nombre_servicio, precio_mano_obra) VALUES (%s, %s);",
                    (nombre, precio),
                )
                conn.commit()
                cursor.close()
                messagebox.showinfo(
                    "Completado", "Servicio agregado al tarifario base."
                )
                self.txt_serv_nombre.delete(0, "end")
                self.txt_serv_precio.delete(0, "end")
                self.cargar_servicios()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el servicio: {e}")
            finally:
                self.cerrar_conexion_bd(db)
