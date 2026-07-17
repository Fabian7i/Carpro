# controladores/controlador_orden.py
"""Controlador para la entidad Orden de Trabajo."""
from controladores.base_controlador import ControladorBase
from modelos import OrdenTrabajo


class ControladorOrden(ControladorBase):
    """Controlador que maneja la lógica de negocio para órdenes de trabajo."""
    
    def obtener_todos(self):
        """Retorna todas las órdenes con información del vehículo."""
        query = """
            SELECT o.id_orden, v.placa, o.diagnostico_inicial, o.total_pagar, o.estado, 
                   TO_CHAR(o.fecha_ingreso, 'DD-MM-YYYY HH24:MI') as fecha
            FROM ordenes_trabajo o
            INNER JOIN vehiculos v ON o.id_vehiculo = v.id_vehiculo
            ORDER BY o.id_orden DESC;
        """
        resultados = self.ejecutar_query(query)
        return resultados if resultados else []
    
    def crear(self, orden):
        """Crea una nueva orden de trabajo.
        
        Args:
            orden: Instancia del modelo OrdenTrabajo
            
        Returns:
            bool: True si se creó exitosamente, False en caso contrario
        """
        valido, mensaje = orden.validar()
        if not valido:
            print(f"Validación fallida: {mensaje}")
            return False
        
        query = """
            INSERT INTO ordenes_trabajo (id_vehiculo, id_usuario, diagnostico_inicial, total_pagar, estado) 
            VALUES (%s, %s, %s, %s, %s);
        """
        params = (orden.id_vehiculo, orden.id_usuario, orden.diagnostico_inicial, 
                  orden.total_pagar, orden.estado)
        return self.ejecutar_insert(query, params)
    
    def obtener_detalle_orden(self, id_orden):
        """Retorna el detalle de una orden específica."""
        query = """
            SELECT o.id_orden, v.placa, c.nombre, o.diagnostico_inicial, o.total_pagar, o.estado,
                   TO_CHAR(o.fecha_ingreso, 'DD-MM-YYYY HH24:MI') as fecha
            FROM ordenes_trabajo o
            INNER JOIN vehiculos v ON o.id_vehiculo = v.id_vehiculo
            INNER JOIN clientes c ON v.id_cliente = c.id_cliente
            WHERE o.id_orden = %s;
        """
        resultados = self.ejecutar_query(query, (id_orden,))
        return resultados[0] if resultados else None
    
    def obtener_servicios_orden(self, id_orden):
        """Retorna los servicios asociados a una orden."""
        query = """
            SELECT s.nombre_servicio, ds.cantidad, s.precio_mano_obra
            FROM detalle_services ds
            INNER JOIN servicios_catalogo s ON ds.id_servicio_cat = s.id_servicio_cat
            WHERE ds.id_orden = %s;
        """
        resultados = self.ejecutar_query(query, (id_orden,))
        return resultados if resultados else []
    
    def obtener_repuestos_orden(self, id_orden):
        """Retorna los repuestos asociados a una orden."""
        query = """
            SELECT r.nombre_repuesto, dr.cantidad, r.precio_venta
            FROM detalle_repuestos dr
            INNER JOIN repuestos r ON dr.id_repuesto = r.id_repuesto
            WHERE dr.id_orden = %s;
        """
        resultados = self.ejecutar_query(query, (id_orden,))
        return resultados if resultados else []
