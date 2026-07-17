# controladores/controlador_vehiculo.py
"""Controlador para la entidad Vehículo."""
from controladores.base_controlador import ControladorBase
from modelos import Vehiculo


class ControladorVehiculo(ControladorBase):
    """Controlador que maneja la lógica de negocio para vehículos."""
    
    def obtener_todos_con_cliente(self):
        """Retorna todos los vehículos con el nombre del cliente."""
        query = """
            SELECT v.placa, v.marca, v.modelo, v.anio, v.kilometraje, c.nombre 
            FROM vehiculos v
            INNER JOIN clientes c ON v.id_cliente = c.id_cliente
            ORDER BY v.id_vehiculo DESC;
        """
        resultados = self.ejecutar_query(query)
        return resultados if resultados else []
    
    def crear(self, vehiculo):
        """Crea un nuevo vehículo en la base de datos.
        
        Args:
            vehiculo: Instancia del modelo Vehiculo
            
        Returns:
            bool: True si se creó exitosamente, False en caso contrario
        """
        valido, mensaje = vehiculo.validar()
        if not valido:
            print(f"Validación fallida: {mensaje}")
            return False
        
        query = """
            INSERT INTO vehiculos (id_cliente, placa, marca, modelo, anio, kilometraje) 
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        params = (vehiculo.id_cliente, vehiculo.placa, vehiculo.marca, 
                  vehiculo.modelo, vehiculo.anio, vehiculo.kilometraje)
        return self.ejecutar_insert(query, params)
    
    def obtener_para_combobox(self):
        """Retorna vehículos formateados para combobox (placa - marca modelo)."""
        query = "SELECT id_vehiculo, placa, marca, modelo FROM vehiculos ORDER BY placa ASC;"
        resultados = self.ejecutar_query(query)
        return resultados if resultados else []
