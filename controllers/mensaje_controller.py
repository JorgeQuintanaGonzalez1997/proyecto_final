from models import mensaje
from flask import Blueprint, request, jsonify
from DB.conectar_db import Conexion

mensaje_bp = Blueprint('mensaje_bp', __name__)

@mensaje_bp.route('/enviar', methods=['POST'])
def enviar_mensaje():
    try:
        data = request.json
        idUsuarioDestino = data["idUsuarioDestino"]
        mensaje = data["mensaje"]

        
        idUsuarioRemitente = request.cookies.get("cookieSesion").split('-')[1]

        query = "INSERT INTO mensajes (idUsuarioRemitente, idUsuarioDestino, mensaje) VALUES (%s, %s, %s)"
        conn = Conexion.conectar()
        cur = conn.cursor()
        cur.execute(query, (idUsuarioRemitente, idUsuarioDestino, mensaje))

        conn.commit()
        cur.close()

        conn.close()

        return jsonify({"mensaje": "Mensaje enviado con éxito"}), 201
    
    except Exception as e:

        return jsonify({"error": str(e)}), 500
    

@mensaje_bp.route('/mensajes/<int:idUsuario>', methods=['GET'])
def obtener_mensajes(idUsuario):
    try:
        query = """
            SELECT m.id, m.mensaje, m.fecha, u_remitente.id AS id_remitente, u_remitente.nombre AS remitente,
                   u_destino.id AS id_destinatario, u_destino.nombre AS destinatario
            FROM mensajes m
            JOIN usuarios u_remitente ON m.idUsuarioRemitente = u_remitente.id
            JOIN usuarios u_destino ON m.idUsuarioDestino = u_destino.id
            WHERE m.idUsuarioRemitente = %s OR m.idUsuarioDestino = %s
            ORDER BY m.fecha DESC
        """
        conn = Conexion.conectar()
        cur = conn.cursor()
        cur.execute(query, (idUsuario, idUsuario))
        mensajes = cur.fetchall()
        cur.close()
        conn.close()

        mensajes_formateados = [
            {
                "id": mensaje[0],
                "mensaje": mensaje[1],
                "fecha": mensaje[2],
                "id_remitente": mensaje[3],
                "remitente": mensaje[4],
                "id_destinatario": mensaje[5],
                "destinatario": mensaje[6]
            }
            for mensaje in mensajes
        ]

        return jsonify(mensajes_formateados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@mensaje_bp.route('/no_leidos/<int:idUsuario>', methods=['GET'])
def obtener_mensajes_no_leidos(idUsuario):
    try:
        query = """
            SELECT COUNT(*) 
            FROM mensajes 
            WHERE idUsuarioDestino = %s AND leido = FALSE
        """
        conn = Conexion.conectar()

        cur = conn.cursor()
        cur.execute(query, (idUsuario,))

        mensajes_no_leidos = cur.fetchone()[0]

        cur.close()
        
        conn.close()
        

        return jsonify({"mensajes_no_leidos": mensajes_no_leidos}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@mensaje_bp.route('/marcar_leidos/<int:idUsuario>', methods=['POST'])
def marcar_mensajes_leidos(idUsuario):
    try:
        query = """
            UPDATE mensajes 
            SET leido = TRUE 
            WHERE idUsuarioDestino = %s AND leido = FALSE
        """
        conn = Conexion.conectar()
        cur = conn.cursor()

        cur.execute(query, (idUsuario,))

        conn.commit()
        
        cur.close()
        conn.close()

        return jsonify({"mensaje": "Mensajes marcados como leídos"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
def crear_tabla():
        conn = Conexion.conectar() 
        if not conn:
            print("❌ No se pudo conectar a la base de datos.")
            return 
        
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS mensajes (
                    id SERIAL PRIMARY KEY,
                    idUsuarioRemitente INT,
                    idUsuarioDestino INT,
                    mensaje TEXT,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    leido BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (idUsuarioRemitente) REFERENCES usuarios(id),
                    FOREIGN KEY (idUsuarioDestino) REFERENCES usuarios(id)
                )
            """)
            conn.commit()
            print("Tabla 'mensajes' creada o ya existente")
            cur.close()  # 🔹 Cerramos el cursor si todo salió bien

        except Exception as e:
            print(f"Error al crear la tabla: {e}")

        finally:
            Conexion.cerrar(conn)  # 🔹 Aseguramos que la conexión se cierre

def guardar(self):
    conn = Conexion.conectar()
    if not conn:
        print("❌ No se pudo conectar a la base de datos.")
        return
        
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO mensajes (idUsuarioRemitente, idUsuarioDestino, mensaje) VALUES (%s, %s, %s)",(self.idUsuarioRemitente, self.idUsuarioDestino, self.mensaje))
        conn.commit()
        print("Mensaje guardado con éxito")
        cur.close()  

    except Exception as e:
        print(f"Error al guardar mensaje: {e}")

    finally:
        Conexion.cerrar(conn)  