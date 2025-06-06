from DB.conectar_db import Conexion
import psycopg2

class SubForo:
    def __init__(self, titulo, contenido):
        self.titulo = titulo
        self.contenido = contenido

    @staticmethod
    def conectar():
        try:
            return Conexion.conectar()
        except psycopg2.DatabaseError as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    @staticmethod
    def crear_tabla():
        conn = SubForo.conectar()
        if not conn:
            print("❌ No se pudo conectar a la base de datos.")
            return
        
        try:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS sub_foros (
                    id SERIAL PRIMARY KEY,
                    titulo VARCHAR(255) NOT NULL UNIQUE,
                    contenido TEXT NOT NULL
                )
            ''')
            conn.commit()
            print("✅ Tabla 'sub_foros' creada o ya existente")
            cur.close()

        except Exception as e:
            print(f"❌ Error al crear la tabla: {e}")

        finally:
            conn.close()
    
    def guardar(self):
        conn = SubForo.conectar()
        if not conn:
            print("No se pudo conectar a la base de datos.")
            return
        
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO sub_foros (titulo, contenido) VALUES (%s, %s)",
                        (self.titulo, self.contenido))
            conn.commit()
            print("SubForo guardado con éxito")
            cur.close()

        except Exception as e:
            print(f"Error al guardar el subforo: {e}")

        finally:
            conn.close()
