# crear_tablas.py
import psycopg2


def crear_estructura():
    # Tu conexión externa directa a Render
    connection_uri = "postgresql://fabian:5oNmc26uhfos7MvJNG4VX0XnbMubKs8Z@dpg-d9c0bpr7uimc73cn0qu0-a.virginia-postgres.render.com/autopro_4qhf?sslmode=require"

    sql_script = """
    -- 1. Crear tabla de Roles
    CREATE TABLE IF NOT EXISTS roles (
        id_role SERIAL PRIMARY KEY,
        nombre_rol VARCHAR(50) NOT NULL
    );

    -- 2. Crear tabla de Usuarios
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario SERIAL PRIMARY KEY,
        id_rol INT REFERENCES roles(id_role) ON DELETE SET NULL,
        nombre VARCHAR(100) NOT NULL,
        correo VARCHAR(100) UNIQUE NOT NULL,
        contrasena VARCHAR(255) NOT NULL
    );

    -- 3. Crear tabla de Clientes (Con la columna 'ruc' corregida)
    CREATE TABLE IF NOT EXISTS clientes (
        id_cliente SERIAL PRIMARY KEY,
        ruc VARCHAR(20) UNIQUE NOT NULL,
        nombre VARCHAR(100) NOT NULL,
        telefono VARCHAR(20),
        correo VARCHAR(100)
    );

    -- 4. Crear tabla de Vehículos
    CREATE TABLE IF NOT EXISTS vehiculos (
        id_vehiculo SERIAL PRIMARY KEY,
        id_cliente INT REFERENCES clientes(id_cliente) ON DELETE CASCADE,
        placa VARCHAR(15) UNIQUE NOT NULL,
        marca VARCHAR(50) NOT NULL,
        modelo VARCHAR(50) NOT NULL,
        anio INT,
        kilometraje INT
    );

    -- 5. Crear tabla de Catálogo de Servicios
    CREATE TABLE IF NOT EXISTS servicios_catalogo (
        id_servicio_cat SERIAL PRIMARY KEY,
        nombre_servicio VARCHAR(150) NOT NULL,
        precio_mano_obra NUMERIC(10, 2) NOT NULL
    );

    -- 6. Crear tabla de Repuestos
    CREATE TABLE IF NOT EXISTS repuestos (
        id_repuesto SERIAL PRIMARY KEY,
        nombre_repuesto VARCHAR(150) NOT NULL,
        codigo_parte VARCHAR(50) UNIQUE,
        precio_venta NUMERIC(10, 2) NOT NULL,
        stock_actual INT DEFAULT 0
    );

    -- 7. Crear tabla de Órdenes de Trabajo
    CREATE TABLE IF NOT EXISTS ordenes_trabajo (
        id_orden SERIAL PRIMARY KEY,
        id_vehiculo INT REFERENCES vehiculos(id_vehiculo) ON DELETE CASCADE,
        id_usuario INT REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
        fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        estado VARCHAR(50) DEFAULT 'Pendiente',
        diagnostico_inicial TEXT,
        total_pagar NUMERIC(10, 2) DEFAULT 0.00
    );

    -- 8. Crear tabla de Detalle de Servicios
    CREATE TABLE IF NOT EXISTS detalle_services (
        id_detalle_serv SERIAL PRIMARY KEY,
        id_orden INT REFERENCES ordenes_trabajo(id_orden) ON DELETE CASCADE,
        id_servicio_cat INT REFERENCES servicios_catalogo(id_servicio_cat) ON DELETE RESTRICT,
        observaciones_tecnicas TEXT
    );

    -- 9. Crear tabla de Detalle de Repuestos
    CREATE TABLE IF NOT EXISTS detalle_repuestos (
        id_det_repuesto SERIAL PRIMARY KEY,
        id_orden INT REFERENCES ordenes_trabajo(id_orden) ON DELETE CASCADE,
        id_repuesto INT REFERENCES repuestos(id_repuesto) ON DELETE RESTRICT,
        cantidad_usada INT NOT NULL,
        precio_unitario_aplicado NUMERIC(10, 2) NOT NULL
    );
    """

    print("Conectando a Render para configurar la base de datos...")
    try:
        conn = psycopg2.connect(connection_uri)
        conn.autocommit = True
        cursor = conn.cursor()

        # Ejecutar la creación de todas las tablas
        cursor.execute(sql_script)
        print("¡Tablas creadas exitosamente en tu base de datos de Render!")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Ocurrió un error al crear las tablas: {e}")


if __name__ == "__main__":
    crear_estructura()
