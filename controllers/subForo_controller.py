from flask import Blueprint, request, jsonify, render_template_string
from models.subForo import SubForo
from DB.conectar_db import Conexion

subForo_bp = Blueprint('subForo_bp', __name__)


contenido_predefinido=""
@subForo_bp.route('/crear', methods=['POST'])
def crear_subForo():
    try:
        data = request.json
        titulo = data["titulo"]
        contenido = contenido_predefinido

        subForo = SubForo(titulo, contenido)
        guardar(subForo)
        
        return jsonify({"mensaje": "SubForo creado"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@subForo_bp.route('/listar', methods=['GET'])
def listar_subForos():
    try:
        conn =Conexion.conectar()
        cur = conn.cursor()
        cur.execute("SELECT titulo FROM sub_foros")
        subForos = cur.fetchall()
        cur.close()
        conn.close()

        subForos_list = [{"titulo": subForo[0]} for subForo in subForos]
        return jsonify({"subForos": subForos_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@subForo_bp.route('/<titulo>', methods=['GET'])
def obtener_subForo(titulo):
    try:
        conn = Conexion.conectar()
        cur = conn.cursor()
        cur.execute("SELECT titulo, contenido FROM sub_foros WHERE titulo = %s", (titulo,))
        subForo = cur.fetchone()
        cur.close()
        conn.close()

        if subForo:
            return jsonify({"titulo": subForo[0], "contenido": subForo[1]}), 200
            
        else:
            return jsonify({"error": "SubForo no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
@subForo_bp.route('/guardarContenido', methods=['POST'])
def guardar_contenido():
    try:
        data = request.json
        titulo = data["titulo"]
        contenido = data["contenido"]

        idUsuario = request.cookies.get("cookieSesion").split('-')[1]
   
        conn = Conexion.conectar()
        cur = conn.cursor()
        cur.execute("SELECT nombre FROM usuarios WHERE id = %s", (idUsuario,))
        resultado = cur.fetchone()
        if not resultado:
            return jsonify({"error": "Usuario no encontrado"}), 404
        nombreUsuario = resultado[0]

        contenido = f"{nombreUsuario}: {contenido}"

        conn = Conexion.conectar()
        cur = conn.cursor()
    
        cur.execute("UPDATE sub_foros SET contenido = contenido || '\n' || %s WHERE titulo = %s", (contenido, titulo))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"mensaje": "Contenido guardado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
def crear_tabla():
        conn = Conexion.conectar()
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
            print("Tabla 'sub_foros' creada o ya existente")
            cur.close()

        except Exception as e:
            print(f"Error al crear la tabla: {e}")

        finally:
            conn.close()
    
def guardar(self):
    conn = Conexion.conectar()
    if not conn:
        print("No se pudo conectar a la base de datos.")
        return
        
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO sub_foros (titulo, contenido) VALUES (%s, %s)",(self.titulo, self.contenido))
        conn.commit()
        print("SubForo guardado con éxito")
        cur.close()

    except Exception as e:
        print(f"Error al guardar el subforo: {e}")

    finally:
        conn.close()