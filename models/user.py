from DB.conectar_db import Conexion 

class Usuario:
    def __init__(self, nombre, email, password):
        self.nombre = nombre
        self.email = email
        self.password = password

    @staticmethod
    def conectar():
        return Conexion.conectar()  
    @staticmethod
    def crear_tabla():
        conn = Usuario.conectar()
        if not conn:
            print("❌ No se pudo conectar a la base de datos.")
            return  # 🔹 Salimos si no hay conexión
        
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100),
                    email VARCHAR(100) UNIQUE,
                    password VARCHAR(100)
                )
            """)
            conn.commit()
            print("✅ Tabla 'usuarios' creada o ya existente")
            cur.close()  # 🔹 Cerramos el cursor si todo salió bien

        except Exception as e:
            print(f"❌ Error al crear la tabla: {e}")

        finally:
            Conexion.cerrar(conn)  # 🔹 Aseguramos que la conexión se cierre

    def guardar(self):
        conn = Usuario.conectar()
        if not conn:
            print("❌ No se pudo conectar a la base de datos.")
            return
        
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                        (self.nombre, self.email,self.password ))
            conn.commit()
            print("✅ Usuario guardado con éxito")
            cur.close()  # 🔹 Cerramos el cursor

        except Exception as e:
            print(f"❌ Error al guardar usuario: {e}")

        finally:
            Conexion.cerrar(conn)  # 🔹 Aseguramos que la conexión se cierre