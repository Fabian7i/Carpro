import customtkinter as ctk
from tkinter import messagebox, ttk
from database import ConexionBD

class VistaServicios(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Título
        self.titulo = ctk.CTkLabel(self, text="Gestión de Catálogo de Servicios", font=ctk.CTkFont(size=22, weight="bold"))
        self.titulo.pack(pady=(15, 10), padx=30, anchor="w")

        # Contenedor principal dividido en dos
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # ==========================================
        # PANEL IZQUIERDO: FORMULARIO
        # ==========================================
        self.left_frame = ctk.CTkFrame(self.main_container, width=300, corner_radius=10)
        self.left_frame.pack(side="left", fill="y", padx=(0, 10))

        ctk.CTkLabel(self.left_frame, text="Datos del Servicio", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

        # Campos
        self.txt_nombre = ctk.CTkEntry(self.left_frame, placeholder_text="Nombre del servicio", width=250)
        self.txt_nombre.pack(pady=10, padx=20)

        self.cmb_rubro = ctk.CTkComboBox(self.left_frame, values=["Mecánica General", "Sistema Eléctrico", "Frenos", "Suspensión", "Estética/Pintura"], width=250)
        self.cmb_rubro.set("Mecánica General")
        self.cmb_rubro.pack(pady=10, padx=20)

        self.txt_costo = ctk.CTkEntry(self.left_frame, placeholder_text="Costo (S/.)", width=250)
        self.txt_costo.pack(pady=10, padx=20)

        # Botones de acción
        self.btn_guardar = ctk.CTkButton(self.left_frame, text="Registrar Servicio", fg_color="#2ecc71", hover_color="#27ae60", command=self.guardar_servicio)
        self.btn_guardar.pack(pady=(20, 10), padx=20)

        self.btn_eliminar = ctk.CTkButton(self.left_frame, text="Eliminar Seleccionado", fg_color="#e74c3c", hover_color="#c0392b", command=self.eliminar_servicio)
        self.btn_eliminar.pack(pady=10, padx=20)

        self.btn_limpiar = ctk.CTkButton(self.left_frame, text="Limpiar Campos", fg_color="#7f8c8d", hover_color="#95a5a6", command=self.limpiar_formulario)
        self.btn_limpiar.pack(pady=10, padx=20)

        # ==========================================
        # PANEL DERECHO: TABLA
        # ==========================================
        self.right_frame = ctk.CTkFrame(self.main_container, corner_radius=10)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Configuración del Treeview
        columnas = ("ID", "Nombre", "Rubro", "Costo")
        self.tabla = ttk.Treeview(self.right_frame, columns=columnas, show="headings")
        
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre del Servicio")
        self.tabla.heading("Rubro", text="Rubro")
        self.tabla.heading("Costo", text="Costo (S/.)")

        self.tabla.column("ID", width=50, anchor="center")
        self.tabla.column("Nombre", width=200, anchor="w")
        self.tabla.column("Rubro", width=150, anchor="center")
        self.tabla.column("Costo", width=100, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Cargar datos al iniciar
        self.cargar_servicios()

    # ==========================================
    # LÓGICA DE BASE DE DATOS
    # ==========================================
    def cargar_servicios(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        db = ConexionBD()
        conn = db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                # Asegúrate de que los nombres de las columnas coincidan con tu BD real
                cursor.execute("SELECT id_servicio, nombre_servicio, rubro, precio_mano_obra FROM servicios_catalogo")
                for fila in cursor.fetchall():
                    self.tabla.insert("", "end", values=fila)
                cursor.close()
            except Exception as e:
                print(f"Error al cargar servicios: {e}")
            finally:
                db.desconectar()

    def guardar_servicio(self):
        nombre = self.txt_nombre.get().strip()
        rubro = self.cmb_rubro.get()
        costo_txt = self.txt_costo.get().strip()

        if not nombre or not costo_txt:
            messagebox.showwarning("Faltan datos", "El nombre y el costo son obligatorios.")
            return

        try:
            costo = float(costo_txt)
        except ValueError:
            messagebox.showwarning("Error", "El costo debe ser un número válido.")
            return

        db = ConexionBD()
        conn = db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                # Ajusta la consulta si tus columnas se llaman distinto en MySQL
                cursor.execute(
                    "INSERT INTO servicios_catalogo (nombre_servicio, rubro, precio_mano_obra) VALUES (%s, %s, %s)",
                    (nombre, rubro, costo)
                )
                conn.commit()
                cursor.close()
                messagebox.showinfo("Éxito", "Servicio guardado correctamente.")
                self.limpiar_formulario()
                self.cargar_servicios()
            except Exception as e:
                messagebox.showerror("Error BD", f"Error: {e}")
            finally:
                db.desonectar()

    def eliminar_servicio(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Selecciona un servicio para eliminar.")
            return
            
        if messagebox.askyesno("Confirmar", "¿Eliminar este servicio del catálogo?"):
            id_servicio = self.tabla.item(seleccion, "values")[0]
            
            db = ConexionBD()
            conn = db.conectar()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM servicios_catalogo WHERE id_servicio = %s", (id_servicio,))
                    conn.commit()
                    cursor.close()
                    self.cargar_servicios()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar: {e}")
                finally:
                    db.desonectar()

    def limpiar_formulario(self):
        self.txt_nombre.delete(0, 'end')
        self.txt_costo.delete(0, 'end')
        self.cmb_rubro.set("Mecánica General")