# database.py
import psycopg2


class ConexionBD:
    def __init__(self):
        
        self.connection_uri = "postgresql://fabian:5oNmc26uhfos7MvJNG4VX0XnbMubKs8Z@dpg-d9c0bpr7uimc73cn0qu0-a.virginia-postgres.render.com/autopro_4qhf?sslmode=require"
        self.conn = None

    def conectar(self):
        try:
            
            self.conn = psycopg2.connect(self.connection_uri, connect_timeout=10)
        
            self.conn.autocommit = True
            print("¡Conexión exitosa a la base de datos de Render!")
            return self.conn
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")
            return None

    def desconectar(self):
        if self.conn:
            self.conn.close()
            print("Conexión cerrada.")

    def obtener_servicios(self):
        """Devuelve una lista de servicios para llenar el Combobox"""
        conn = self.conectar()
        servicios = []
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT nombre_servicio FROM servicios;"
            )  
            servicios = [fila[0] for fila in cursor.fetchall()]
            cursor.close()
            self.desconectar()
        return servicios

    def obtener_detalles_orden(self, id_orden):
        """Devuelve los servicios y repuestos de una orden específica"""
        conn = self.conectar()
        detalles = []
        if conn:
            cursor = conn.cursor()
            # Esta consulta es un ejemplo, ajústala según los nombres de tus tablas
            query = """
                SELECT 'Servicio' as tipo, nombre_servicio as descripcion, precio 
                FROM orden_servicios WHERE id_orden = %s
                UNION ALL
                SELECT 'Repuesto' as tipo, nombre_repuesto as descripcion, precio 
                FROM orden_repuestos WHERE id_orden = %s
            """
            cursor.execute(query, (id_orden, id_orden))
            detalles = cursor.fetchall()
            cursor.close()
            self.desonectar()
        return detalles

    def inicializar_datos_base(self):
        conn = self.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                # Insertar rol si no existe
                cursor.execute(
                    "INSERT INTO roles (nombre_rol) VALUES ('Administrador') ON CONFLICT DO NOTHING;"
                )

                # Insertar usuario administrador
                cursor.execute("""
                    INSERT INTO usuarios (id_usuario, id_rol, nombre, correo, contrasena) 
                    VALUES (1, 1, 'Administrador Base', 'admin@autopro.com', 'admin123') 
                    ON CONFLICT (id_usuario) DO NOTHING;
                """)

                conn.commit()
                print("Datos base inicializados correctamente.")
                cursor.close()
            except Exception as e:
                print(f"Error al inicializar datos: {e}")
            finally:
                self.desconectar()
