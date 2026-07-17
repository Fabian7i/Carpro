import customtkinter as ctk
from tkinter import messagebox, ttk
from database import ConexionBD
from vistas.base_vista import VistaBase
from modelos import Cliente


class VistaClientes(VistaBase):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.titulo = ctk.CTkLabel(
            self, text="Gestión de Clientes", font=ctk.CTkFont(size=22, weight="bold")
        )
        self.titulo.pack(pady=(15, 5), padx=30, anchor="w")

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # ---- COLUMNA IZQUIERDA ----
        self.left_frame = ctk.CTkFrame(self.main_container, width=320, corner_radius=10)
        self.left_frame.pack(side="left", fill="y", padx=(10, 20), pady=10)

        self.txt_dni_ruc = ctk.CTkEntry(
            self.left_frame, placeholder_text="DNI o RUC", width=240
        )
        self.txt_dni_ruc.pack(pady=10)
        self.txt_nombre = ctk.CTkEntry(
            self.left_frame, placeholder_text="Nombre", width=240
        )
        self.txt_nombre.pack(pady=10)
        self.txt_telefono = ctk.CTkEntry(
            self.left_frame, placeholder_text="Teléfono", width=240
        )
        self.txt_telefono.pack(pady=10)
        self.txt_correo = ctk.CTkEntry(
            self.left_frame, placeholder_text="Correo", width=240
        )
        self.txt_correo.pack(pady=10)

        self.btn_guardar = ctk.CTkButton(
            self.left_frame,
            text="Registrar",
            fg_color="#e67e22",
            command=self.guardar_cliente,
        )
        self.btn_guardar.pack(pady=20)

        # ---- COLUMNA DERECHA ----
        self.right_frame = ctk.CTkFrame(self.main_container, corner_radius=10)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.tabla = ttk.Treeview(
            self.right_frame,
            columns=("ID", "DNI/RUC", "Nombre", "Teléfono", "Correo"),
            show="headings",
        )
        for col in ("ID", "DNI/RUC", "Nombre", "Teléfono", "Correo"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=80)
        self.tabla.pack(fill="both", expand=True, padx=15, pady=15)

        self.btn_editar = ctk.CTkButton(
            self.right_frame,
            text="Editar Seleccionado",
            fg_color="#3498db",
            command=self.abrir_ventana_edicion,
        )
        self.btn_editar.pack(pady=10)

        self.cargar_clientes()

    def abrir_ventana_edicion(self):
        selected_item = self.tabla.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, selecciona un cliente.")
            return

        item_data = self.tabla.item(selected_item)["values"]
        id_cliente, ruc, nombre, telefono, correo = item_data

        ventana_edit = ctk.CTkToplevel(self)
        ventana_edit.title("Editar Cliente")
        ventana_edit.geometry("300x400")

        txt_ruc = ctk.CTkEntry(ventana_edit)
        txt_ruc.insert(0, ruc)
        txt_ruc.pack(pady=5)
        txt_nombre = ctk.CTkEntry(ventana_edit)
        txt_nombre.insert(0, nombre)
        txt_nombre.pack(pady=5)
        txt_telefono = ctk.CTkEntry(ventana_edit)
        txt_telefono.insert(0, telefono)
        txt_telefono.pack(pady=5)
        txt_correo = ctk.CTkEntry(ventana_edit)
        txt_correo.insert(0, correo)
        txt_correo.pack(pady=5)

        def guardar_cambios():
            db = ConexionBD()
            conn = db.conectar()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE clientes SET ruc=%s, nombre=%s, telefono=%s, correo=%s WHERE id_cliente=%s",
                        (
                            txt_ruc.get(),
                            txt_nombre.get(),
                            txt_telefono.get(),
                            txt_correo.get(),
                            id_cliente,
                        ),
                    )
                    conn.commit()
                    cursor.close()
                    messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"No se pudieron guardar los cambios:\n{e}"
                    )
                finally:
                    db.desconectar()
            ventana_edit.destroy()
            self.cargar_clientes()

        ctk.CTkButton(ventana_edit, text="Guardar", command=guardar_cambios).pack(
            pady=20
        )

    def cargar_clientes(self):
        self.limpiar_tabla(self.tabla)
        db, conn = self.obtener_conexion_bd()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id_cliente, ruc, nombre, telefono, correo FROM clientes"
                )
                for fila in cursor.fetchall():
                    self.tabla.insert("", "end", values=fila)
                cursor.close()
            except Exception as e:
                print(f"Error cargando clientes: {e}")
            finally:
                self.cerrar_conexion_bd(db)

    def guardar_cliente(self):
        ruc = self.txt_dni_ruc.get().strip()
        nombre = self.txt_nombre.get().strip()
        telefono = self.txt_telefono.get().strip()
        correo = self.txt_correo.get().strip()

        # Usamos el modelo Cliente para validación
        cliente = Cliente(ruc=ruc, nombre=nombre, telefono=telefono, correo=correo)
        valido, mensaje = cliente.validar()

        if not valido:
            messagebox.showwarning("Campos Incompletos", mensaje)
            return

        db, conn = self.obtener_conexion_bd()
        if conn is None:
            messagebox.showerror("Error", "Error al conectar con la base de datos.")
            return

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO clientes (ruc, nombre, telefono, correo) 
                VALUES (%s, %s, %s, %s);
            """
            cursor.execute(query, (ruc, nombre, telefono, correo))
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
            self.cerrar_conexion_bd(db)

    def limpiar_formulario(self):
        self.txt_dni_ruc.delete(0, "end")
        self.txt_nombre.delete(0, "end")
        self.txt_telefono.delete(0, "end")
        self.txt_correo.delete(0, "end")
