from DB.conectar_db import Conexion 

class Usuario:
    def __init__(self, nombre,password):
        self.nombre = nombre
        
        self.password = password

    @staticmethod
    def conectar():
        return Conexion.conectar()  
    