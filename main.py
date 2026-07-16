# main.py
import customtkinter as ctk
from vistas.vistas_vehiculos import VistaVehiculos
from vistas.vistas_mantenimiento import VistaMantenimiento
from vistas.vistasClientes import VistaClientes
from vistas.vistas_inventario import VistaInventario
from vistas.vistas_servicios import VistaServicios


class PanelPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AutoPro Taller - Panel Principal")
        self.geometry("1100x650")
        ctk.set_appearance_mode("dark")

        # ---- BARRA LATERAL (SIDEBAR) ----
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.lbl_logo = ctk.CTkLabel(
            self.sidebar, text="AUTOPRO", font=ctk.CTkFont(size=22, weight="bold")
        )
        self.lbl_logo.pack(pady=(30, 5))

        self.lbl_user = ctk.CTkLabel(
            self.sidebar,
            text="Usuario: Fabian\nRol: Administrador",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="gray",
        )
        self.lbl_user.pack(pady=(0, 30))

        #
        self.btn_mantenimiento = ctk.CTkButton(
            self.sidebar,
            text="Mantenimiento",
            command=self.mostrar_mantenimiento,
            height=35,
        )
        self.btn_mantenimiento.pack(pady=10, padx=20, fill="x")
        self.btn_servicios = ctk.CTkButton(
            self.sidebar,
            text="Catálogo Servicios",
            command=self.mostrar_servicios,
            height=35,
        )
        self.btn_servicios.pack(pady=10, padx=20, fill="x")
        self.btn_vehiculos = ctk.CTkButton(
            self.sidebar, text="Vehículos", command=self.mostrar_vehiculos, height=35
        )
        self.btn_vehiculos.pack(pady=10, padx=20, fill="x")

        self.btn_clientes = ctk.CTkButton(
            self.sidebar,
            text="Clientes",
            fg_color="#e67e22",
            hover_color="#d35400",
            command=self.mostrar_clientes,
            height=35,
        )
        self.btn_clientes.pack(pady=10, padx=20, fill="x")

        self.btn_logout = ctk.CTkButton(
            self.sidebar,
            text="Cerrar Sesión",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self.destroy,
            height=35,
        )
        self.btn_logout.pack(side="bottom", pady=20, padx=20, fill="x")

        # ---- CONTENEDOR PRINCIPAL ----
        self.contenedor_principal = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.contenedor_principal.pack(side="right", fill="both", expand=True)

        self.vista_actual = None

        # Cargamos Clientes por defecto para probar la nueva estructura modular
        self.mostrar_clientes()

    def limpiar_contenedor(self):
        if self.vista_actual is not None:
            self.vista_actual.destroy()

    def mostrar_mantenimiento(self):
        self.limpiar_contenedor()
        self.vista_actual = VistaMantenimiento(self.contenedor_principal)
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_vehiculos(self):
        self.limpiar_contenedor()
        self.vista_actual = VistaVehiculos(self.contenedor_principal)
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_clientes(self):
        self.limpiar_contenedor()
        self.vista_actual = VistaClientes(self.contenedor_principal)
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_servicios(self):
        self.limpiar_contenedor()
        self.vista_actual = VistaServicios(self.contenedor_principal)
        self.vista_actual.pack(fill="both", expand=True)

    def inicializar_base_datos(self):
        db = ConexionBD()
        db.inicializar_datos_base()


if __name__ == "__main__":
    app = PanelPrincipal()
    app.mainloop()
