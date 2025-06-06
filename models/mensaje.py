from DB.conectar_db import Conexion 

class Mensaje:
    def __init__(self, idUsuarioRemitente, idUsuarioDestino, mensaje):
        self.idUsuarioRemitente = idUsuarioRemitente
        self.idUsuarioDestino = idUsuarioDestino
        self.mensaje = mensaje

    @staticmethod
    def conectar():
        return Conexion.conectar()  # 🔹 Devuelve la conexión correcta

    @staticmethod
    def crear_tabla():
        conn = Mensaje.conectar()
        if not conn:
            print("❌ No se pudo conectar a la base de datos.")
            return  # 🔹 Salimos si no hay conexión
        
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS mensajes (
                    id SERIAL PRIMARY KEY,
                    idUsuarioRemitente INT,
                    idUsuarioDestino INT,
                    mensaje TEXT,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (idUsuarioRemitente) REFERENCES usuarios(id),
                    FOREIGN KEY (idUsuarioDestino) REFERENCES usuarios(id)
                )
            """)
            conn.commit()
            print("✅ Tabla 'mensajes' creada o ya existente")
            cur.close()  # 🔹 Cerramos el cursor si todo salió bien

        except Exception as e:
            print(f"❌ Error al crear la tabla: {e}")

        finally:
            Conexion.cerrar(conn)  # 🔹 Aseguramos que la conexión se cierre

    def guardar(self):
        conn = Mensaje.conectar()
        if not conn:
            print("❌ No se pudo conectar a la base de datos.")
            return
        
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO mensajes (idUsuarioRemitente, idUsuarioDestino, mensaje) VALUES (%s, %s, %s)",
                        (self.idUsuarioRemitente, self.idUsuarioDestino, self.mensaje))
            conn.commit()
            print("✅ Mensaje guardado con éxito")
            cur.close()  # 🔹 Cerramos el cursor

        except Exception as e:
            print(f"❌ Error al guardar mensaje: {e}")

        finally:
            Conexion.cerrar(conn)  # 🔹 Aseguramos que la conexión se cierre
