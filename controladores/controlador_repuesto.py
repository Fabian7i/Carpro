# controladores/controlador_repuesto.py
"""Controlador para la entidad Repuesto."""
from controladores.base_controlador import ControladorBase
from modelos import Repuesto


class ControladorRepuesto(ControladorBase):
    """Controlador que maneja la lógica de negocio para repuestos."""
    
    def obtener_todos(self):
        """Retorna todos los repuestos ordenados por stock."""
        query = "SELECT codigo_parte, nombre_repuesto, precio_venta, stock_actual FROM repuestos ORDER BY stock_actual ASC;"
        resultados = self.ejecutar_query(query)
        return resultados if resultados else []
    
    def crear(self, repuesto):
        """Crea un nuevo repuesto en la base de datos.
        
        Args:
            repuesto: Instancia del modelo Repuesto
            
        Returns:
            bool: True si se creó exitosamente, False en caso contrario
        """
        valido, mensaje = repuesto.validar()
        if not valido:
            print(f"Validación fallida: {mensaje}")
            return False
        
        query = """
            INSERT INTO repuestos (nombre_repuesto, codigo_parte, precio_venta, stock_actual) 
            VALUES (%s, %s, %s, %s);
        """
        params = (repuesto.nombre_repuesto, repuesto.codigo_parte, 
                  repuesto.precio_venta, repuesto.stock_actual)
        return self.ejecutar_insert(query, params)
    
    def eliminar(self, id_repuesto):
        """Elimina un repuesto de la base de datos.
        
        Args:
            id_repuesto: ID del repuesto a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente, False en caso contrario
        """
        query = "DELETE FROM repuestos WHERE id_repuesto = %s"
        return self.ejecutar_insert(query, (id_repuesto,))
