from flask import Blueprint, request, jsonify, make_response
from models.user import Usuario
from DB.conectar_db import Conexion
import bcrypt

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

usuario_bp = Blueprint('usuario_bp', __name__)



@usuario_bp.route('/registrar', methods=['POST'])
def registrar_usuario():
    try:
        data = request.json
        nombre = data["nombre"]
        email = data["email"]
        password = data["password"]

        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        #enviar_correo(email, nombre, password)  
        usuario = Usuario(nombre, email, hashed_password)

        
        guardar(usuario)

        return jsonify({"mensaje": "Usuario registrado con éxito"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    



@usuario_bp.route('/login', methods=['POST'])
def login():

    try:
        
        data = request.json

        username = data.get('username')

        password = data.get('password')

        
        if not username or not password:
            return jsonify({"error": "Nombre de usuario y contraseña son obligatorios"}), 400

        
        query = "SELECT id, password FROM usuarios WHERE nombre = %s"
        conn = Conexion.conectar()

        cur = conn.cursor()
        cur.execute(query, (username,))
        result = cur.fetchone()
        cur.close()

        conn.close()

        
        if result is None:
            print("Usuario no encontrado")
            return jsonify({"error": "Credenciales inválidas"}), 401
        print("Usuario encontrado")
        user_id, hashed_password = result

        
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            
            cookie = f"cookie-{user_id}"

            
            response = make_response(jsonify({"mensaje": "Inicio de sesión exitoso"}))
            response.set_cookie("cookieSesion", cookie, httponly=False, max_age=604800)  # Tiempo de vida de 7 días

            return response, 200
        else:
            return jsonify({"error": "Credenciales inválidas"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@usuario_bp.route('/obtener_usuario', methods=['GET'])
def obtener_usuario():
    
    cookie = request.cookies.get('cookieSesion')
    print("cookie recibido:", cookie)

    if not cookie:


        return jsonify({"error": "No autorizado"}), 401

    
    try:
        user_id = cookie.split('-')[1] 
    except IndexError:
        return jsonify({"error": "cookie inválido"}), 400

   
    query = "SELECT nombre FROM usuarios WHERE id = %s"
    conn = Conexion.conectar()

    cur = conn.cursor()

    cur.execute(query, (user_id,))

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result is None:
        return jsonify({"error": "Usuario no encontrado"}), 404

    nombre = result[0]

    return jsonify({"nombre": nombre}), 200

# @usuario_bp.route("/getDinero",methods=["GET"])
# def getDinero():
    
#     cookie = request.cookies.get('cookieSesion')


#     print("cookie recibido en getDinero:", cookie)

#     if not cookie:


#         return jsonify({"error": "No autorizado"}), 401

    
#     try:
#         user_id = cookie.split('-')[1]  
        
#         print("ID de usuario extraído:", user_id)
#     except IndexError:
#         return jsonify({"error": "cookie inválido"}), 400

    
#     query = "SELECT dinero FROM usuarios WHERE id = %s"
#     conn = Conexion.conectar()


#     cur = conn.cursor()
#     cur.execute(query, (user_id,))

#     result = cur.fetchone()
#     print("Resultado de la consulta:", result)

#     cur.close()

#     conn.close()

#     if result is None:
#         return jsonify({"error": "Usuario no encontrado"}), 404

#     dinero = float(result[0])  
#     print("Dinero del usuario:", dinero)

#     return jsonify({"dinero": dinero}), 200



@usuario_bp.route('/perfil', methods=['GET'])
def perfil():
    
    cookie = request.cookies.get('cookieSesion')

    if not cookie:
        return jsonify({"error": "No autorizado"}), 401

    
    user_id = cookie.split('-')[1]  
    return jsonify({"mensaje": f"Bienvenido, usuario {user_id}"}), 200


@usuario_bp.route('/logout', methods=['POST'])
def logout():

    response = make_response(jsonify({"mensaje": "Sesión cerrada"}))

    response.delete_cookie("cookieSesion")
    
    return response, 200


def crear_tabla():
        conn = Conexion.conectar()  # 🔹 Conectamos a la base de datos
        if not conn:
            print("No se pudo conectar a la base de datos.")
            return  
        
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100),
                    email VARCHAR(100) UNIQUE,
                    password VARCHAR(100),
                    dinero FLOAT DEFAULT 0.0
                )
            """)
            conn.commit()
            print("Tabla 'usuarios' creada o ya existente")
            cur.close()  

        except Exception as e:
            print(f"Error al crear la tabla: {e}")

        finally:
            Conexion.cerrar(conn)  # 🔹 Aseguramos que la conexión se cierre

def guardar(self):
        conn = Conexion.conectar()  
        if not conn:
            print("No se pudo conectar a la base de datos.")
            return
        
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                        (self.nombre, self.email,self.password ))
            conn.commit()
            print("Usuario guardado con éxito")
            cur.close() 

        except Exception as e:
            print(f"Error al guardar usuario: {e}")

        finally:
            Conexion.cerrar(conn)
# def enviar_correo(destinatario, nombre_usuario, password):
#     remitente = "vocesdepapel2@gmail.com"
#     clave = "vocesdepapel123"  # Usa una contraseña de aplicación, no la normal
#     asunto = "Registro exitoso en Voces de Papel"
#     cuerpo = f"""
#     Hola {nombre_usuario},

#     ¡Bienvenido a Voces de Papel!
#     Tus datos de acceso son:
#     Usuario: {nombre_usuario}
#     Contraseña: {password}

#     ¡Gracias por registrarte!
#     """

#     msg = MIMEMultipart()
#     msg['From'] = remitente
#     msg['To'] = destinatario
#     msg['Subject'] = asunto
#     msg.attach(MIMEText(cuerpo, 'plain'))

#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(remitente, clave)
#         server.sendmail(remitente, destinatario, msg.as_string())
#         server.quit()
#     except Exception as e:
#         print("Error enviando correo:", e)




