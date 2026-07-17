# modelos.py
"""Clases modelo para las entidades del sistema.
Proporcionan estructura POO sin modificar la lógica existente."""


class ModeloBase:
    """Clase base para todos los modelos del sistema."""
    
    def __init__(self, **kwargs):
        """Inicializa el modelo con los atributos proporcionados."""
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self):
        """Convierte el modelo a un diccionario."""
        return self.__dict__
    
    def __repr__(self):
        """Representación en string del modelo."""
        attrs = ', '.join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


class Cliente(ModeloBase):
    """Modelo para la entidad Cliente."""
    
    def __init__(self, id_cliente=None, ruc=None, nombre=None, telefono=None, correo=None):
        super().__init__(
            id_cliente=id_cliente,
            ruc=ruc,
            nombre=nombre,
            telefono=telefono,
            correo=correo
        )
    
    def validar(self):
        """Valida que los campos obligatorios estén presentes."""
        if not self.ruc or not self.nombre or not self.telefono:
            return False, "RUC, Nombre y Teléfono son obligatorios"
        return True, ""


class Vehiculo(ModeloBase):
    """Modelo para la entidad Vehículo."""
    
    def __init__(self, id_vehiculo=None, id_cliente=None, placa=None, 
                 marca=None, modelo=None, anio=None, kilometraje=None):
        super().__init__(
            id_vehiculo=id_vehiculo,
            id_cliente=id_cliente,
            placa=placa,
            marca=marca,
            modelo=modelo,
            anio=anio,
            kilometraje=kilometraje
        )
    
    def validar(self):
        """Valida que los campos obligatorios estén presentes."""
        if not self.placa or not self.marca or not self.modelo or not self.anio:
            return False, "Placa, Marca, Modelo y Año son obligatorios"
        return True, ""


class ServicioCatalogo(ModeloBase):
    """Modelo para la entidad Servicio del catálogo."""
    
    def __init__(self, id_servicio_cat=None, nombre_servicio=None, 
                 precio_mano_obra=None, rubro=None):
        super().__init__(
            id_servicio_cat=id_servicio_cat,
            nombre_servicio=nombre_servicio,
            precio_mano_obra=precio_mano_obra,
            rubro=rubro
        )
    
    def validar(self):
        """Valida que los campos obligatorios estén presentes."""
        if not self.nombre_servicio or self.precio_mano_obra is None:
            return False, "Nombre del servicio y precio son obligatorios"
        return True, ""


class Repuesto(ModeloBase):
    """Modelo para la entidad Repuesto."""
    
    def __init__(self, id_repuesto=None, nombre_repuesto=None, 
                 codigo_parte=None, precio_venta=None, stock_actual=None):
        super().__init__(
            id_repuesto=id_repuesto,
            nombre_repuesto=nombre_repuesto,
            codigo_parte=codigo_parte,
            precio_venta=precio_venta,
            stock_actual=stock_actual
        )
    
    def validar(self):
        """Valida que los campos obligatorios estén presentes."""
        if not self.nombre_repuesto or not self.codigo_parte:
            return False, "Nombre del repuesto y código son obligatorios"
        return True, ""


class OrdenTrabajo(ModeloBase):
    """Modelo para la entidad Orden de Trabajo."""
    
    def __init__(self, id_orden=None, id_vehiculo=None, id_usuario=None,
                 fecha_ingreso=None, estado=None, diagnostico_inicial=None,
                 total_pagar=None):
        super().__init__(
            id_orden=id_orden,
            id_vehiculo=id_vehiculo,
            id_usuario=id_usuario,
            fecha_ingreso=fecha_ingreso,
            estado=estado,
            diagnostico_inicial=diagnostico_inicial,
            total_pagar=total_pagar
        )
    
    def validar(self):
        """Valida que los campos obligatorios estén presentes."""
        if not self.id_vehiculo or not self.diagnostico_inicial:
            return False, "Vehículo y diagnóstico son obligatorios"
        return True, ""
