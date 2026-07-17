# controladores/base_controlador.py
"""Controlador base con lógica de base de datos compartida."""
from database import ConexionBD


class ControladorBase:
    """Clase base para todos los controladores.
    Maneja la conexión y operaciones comunes de base de datos."""
    
    def __init__(self):
        self.db = ConexionBD()
        self.conn = None
    
    def conectar(self):
        """Establece conexión a la base de datos."""
        self.conn = self.db.conectar()
        return self.conn is not None
    
    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        if self.db:
            self.db.desconectar()
            self.conn = None
    
    def ejecutar_query(self, query, params=None):
        """Ejecuta una query SELECT y retorna los resultados."""
        if not self.conectar():
            return None
        
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            return resultados
        except Exception as e:
            print(f"Error ejecutando query: {e}")
            return None
        finally:
            self.desconectar()
    
    def ejecutar_insert(self, query, params):
        """Ejecuta una query INSERT/UPDATE/DELETE y retorna True si tiene éxito."""
        if not self.conectar():
            return False
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error ejecutando insert/update/delete: {e}")
            return False
        finally:
            self.desconectar()
