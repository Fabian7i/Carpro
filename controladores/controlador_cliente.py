# controladores/controlador_cliente.py
"""Controlador para la entidad Cliente."""
from controladores.base_controlador import ControladorBase
from modelos import Cliente


class ControladorCliente(ControladorBase):
    """Controlador que maneja la lógica de negocio para clientes."""
    
    def obtener_todos(self):
        """Retorna todos los clientes de la base de datos."""
        query = "SELECT id_cliente, ruc, nombre, telefono, correo FROM clientes"
        resultados = self.ejecutar_query(query)
        return resultados if resultados else []
    
    def crear(self, cliente):
        """Crea un nuevo cliente en la base de datos.
        
        Args:
            cliente: Instancia del modelo Cliente
            
        Returns:
            bool: True si se creó exitosamente, False en caso contrario
        """
        valido, mensaje = cliente.validar()
        if not valido:
            print(f"Validación fallida: {mensaje}")
            return False
        
        query = """
            INSERT INTO clientes (ruc, nombre, telefono, correo) 
            VALUES (%s, %s, %s, %s);
        """
        params = (cliente.ruc, cliente.nombre, cliente.telefono, cliente.correo)
        return self.ejecutar_insert(query, params)
    
    def actualizar(self, id_cliente, cliente):
        """Actualiza un cliente existente.
        
        Args:
            id_cliente: ID del cliente a actualizar
            cliente: Instancia del modelo Cliente con los nuevos datos
            
        Returns:
            bool: True si se actualizó exitosamente, False en caso contrario
        """
        valido, mensaje = cliente.validar()
        if not valido:
            print(f"Validación fallida: {mensaje}")
            return False
        
        query = """
            UPDATE clientes 
            SET ruc = %s, nombre = %s, telefono = %s, correo = %s 
            WHERE id_cliente = %s;
        """
        params = (cliente.ruc, cliente.nombre, cliente.telefono, cliente.correo, id_cliente)
        return self.ejecutar_insert(query, params)
    
    def obtener_por_id(self, id_cliente):
        """Retorna un cliente por su ID."""
        query = "SELECT id_cliente, ruc, nombre, telefono, correo FROM clientes WHERE id_cliente = %s"
        resultados = self.ejecutar_query(query, (id_cliente,))
        return resultados[0] if resultados else None
    
    def obtener_para_combobox(self):
        """Retorna clientes formateados para combobox (ruc - nombre)."""
        query = "SELECT id_cliente, ruc, nombre FROM clientes ORDER BY nombre ASC;"
        resultados = self.ejecutar_query(query)
        return resultados if resultados else []
