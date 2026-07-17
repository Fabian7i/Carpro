# controladores/controlador_servicio.py
"""Controlador para la entidad Servicio."""
from controladores.base_controlador import ControladorBase
from modelos import ServicioCatalogo


class ControladorServicio(ControladorBase):
    """Controlador que maneja la lógica de negocio para servicios."""
    
    def obtener_todos(self):
        """Retorna todos los servicios del catálogo."""
        query = "SELECT id_servicio, nombre_servicio, rubro, precio_mano_obra FROM servicios_catalogo"
        resultados = self.ejecutar_query(query)
        return resultados if resultados else []
    
    def crear(self, servicio):
        """Crea un nuevo servicio en el catálogo.
        
        Args:
            servicio: Instancia del modelo ServicioCatalogo
            
        Returns:
            bool: True si se creó exitosamente, False en caso contrario
        """
        valido, mensaje = servicio.validar()
        if not valido:
            print(f"Validación fallida: {mensaje}")
            return False
        
        query = """
            INSERT INTO servicios_catalogo (nombre_servicio, rubro, precio_mano_obra) 
            VALUES (%s, %s, %s);
        """
        params = (servicio.nombre_servicio, servicio.rubro, servicio.precio_mano_obra)
        return self.ejecutar_insert(query, params)
    
    def eliminar(self, id_servicio):
        """Elimina un servicio del catálogo.
        
        Args:
            id_servicio: ID del servicio a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente, False en caso contrario
        """
        query = "DELETE FROM servicios_catalogo WHERE id_servicio = %s"
        return self.ejecutar_insert(query, (id_servicio,))
