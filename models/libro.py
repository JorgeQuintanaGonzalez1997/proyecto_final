from DB.conectar_db import Conexion
import psycopg2

class Libro:
    def __init__(self, titulo, autor, tipo,precio,idUsuario,imagen,fecha_limite):
        self.titulo = titulo
        self.autor = autor
        self.tipo = tipo
        self.precio=precio
        self.idUsuario=idUsuario
        self.imagen = imagen
        self.fecha_limite = fecha_limite


    def getTitulo(self):
        return self.titulo
    def getAutor(self):
        return self.autor
    def getTipo(self):
        return self.tipo
    def getPrecio(self):
        return self.precio
    def setTitulo(self, titulo):    
        self.titulo = titulo
    def setAutor(self, autor):
        self.autor = autor
    def setTipo(self, tipo):
        self.tipo = tipo
    def setPrecio(self, precio):
        self.precio = precio
    def setIdUsuario(self, idUsuario):
        self.idUsuario = idUsuario
    def getIdUsuario(self):
        return self.idUsuario
    def setImagen(self, imagen):
        self.imagen = imagen
    def getImagen(self):
        return self.imagen
    def setFechaLimite(self, fecha_limite):
        self.fecha_limite = fecha_limite
    def getFechaLimite(self):
        return self.fecha_limite
    




        
    # @staticmethod
    # def conectar():
    #     return Conexion.conectar()
    # @staticmethod
    # def crear_tabla():
    #     conn = Libro.conectar()
    #     if not conn:
    #         print("❌ No se pudo conectar a la base de datos.")
    #         return  # 🔹 Salimos si no hay conexión
        
    #     try:
    #         cur=conn.cursor()
    #         cur.execute("""
    #             CREATE TABLE IF NOT EXISTS libros (
    #                 id SERIAL PRIMARY KEY,
    #                 titulo VARCHAR(100),
    #                 autor VARCHAR(100),
    #                 tipo VARCHAR(100)
    #             )
    #         """)
    #         conn.commit()
    #         cur.close()  # 🔹 Cerramos el cursor si todo salió bien
    #     except Exception as e:
    #         print(f"❌ Error al crear la tabla: {e}")
    
