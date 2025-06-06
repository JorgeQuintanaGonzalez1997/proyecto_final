import psycopg2

class Conexion:
    
    @staticmethod
    def conectar():
        try:
            conn = psycopg2.connect(
                dbname="DB",
                user="postgres",
                password="pluton",
                host="localhost",
                port="5432"
            )
            print("✅ Conexión exitosa")
            return conn  
        except psycopg2.Error as e:
            print(f"❌ Error de conexión: {e}")
            return None  

    @staticmethod
    def cerrar(conn):
        if conn:
            conn.close()
            print("🔌 Conexión cerrada")