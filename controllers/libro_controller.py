from models import libro
from DB.conectar_db import Conexion
from flask import Blueprint, request, jsonify, render_template_string
import base64

libro_bp = Blueprint('libro_bp', __name__)

@libro_bp.route('/registrar', methods=['POST'])
def registrar_libro():
    try:

         
        if 'imagen' not in request.files or request.files['imagen'].filename == '':
            return jsonify({"error": "Es obligatorio seleccionar una imagen"}), 400

        file = request.files['imagen']
        imagen_binaria = file.read()


        titulo = request.form.get('titulo')  
        autor = request.form.get('autor')    
        tipo = request.form.get('tipo')      
        precio = request.form.get('precio') 
        idUsuario = request.form.get('idUsuario')
        fecha_limite = request.form.get('fecha_limite')  

        print(titulo,autor,tipo,precio,idUsuario, fecha_limite)


        
        


        libro_obj = libro.Libro(titulo, autor, tipo, precio,idUsuario,imagen_binaria,fecha_limite)

       
        guardar(libro_obj)

        return jsonify({"mensaje": "Libro registrado con éxito"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@libro_bp.route('/eliminar/<int:idLibro>', methods=['DELETE'])
def eliminar_libro(idLibro):
    conn = Conexion.conectar()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM pujas WHERE idLibro = %s", (idLibro,))
    
    cur.execute("DELETE FROM libros WHERE id = %s", (idLibro,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Libro y pujas asociadas eliminados"})
    

@libro_bp.route('/lista_libros', methods=['GET'])
def obtener_libros():
    try:
        
        query = "SELECT id, titulo, autor, precio,idUsuario, imagen, fecha_limite FROM libros"
        conn = Conexion.conectar()
        cur = conn.cursor()
        cur.execute(query)
        libros = cur.fetchall()
        cur.close()
        conn.close()

        #Lista de diccionarios para convertir la información de los libros en JSON
        libros_lista = [
            
            {   "id":libro[0],
                "titulo": libro[1], 
                "autor": libro[2], 
                "precio": libro[3],
                "idUsuario":libro[4],
                #Convierte la imagen a texto para poder enviarla por JSON
                "imagen": base64.b64encode(libro[5]).decode('utf-8') if libro[5] else None,
                #Convierte la fecha a string, en formato ISO, que es compatible con JSON
                "fecha_limite": libro[6].isoformat()  if libro[6] else None
            }
            #El for es un "list comprehesion" sirve para recorrer los libros que hay en la base de datos 
            # y los convierte en un diccionario
            for libro in libros]

        return jsonify(libros_lista), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@libro_bp.route('/lista_libros_por_usuario/<int:idUsuario>', methods=['GET'])
def obtener_libros_por_usuario(idUsuario):
    try:
        
        query = "SELECT id, titulo, autor, precio, id, imagen,fecha_limite FROM libros where idUsuario = %s"
        conn = Conexion.conectar()

        cur = conn.cursor()

        cur.execute(query, (idUsuario,))
        libros = cur.fetchall()
        cur.close()
        conn.close()

        libros_lista = [
            {   "titulo": libro[1], 
                "autor": libro[2], 
                "precio": libro[3],
                "id": libro[0],
                "idUsuario":libro[4],
                "imagen": base64.b64encode(libro[5]).decode('utf-8') if libro[5] else None,
                "fecha_limite": libro[6].isoformat()  if libro[6] else None
            }
            
            for libro in libros]

        return jsonify(libros_lista), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def guardar(libro):
        conn = Conexion.conectar()
        if not conn:
            print("No se pudo conectar a la base de datos.")
            return
        
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO libros (titulo, autor, tipo, precio,idUsuario, imagen,fecha_limite) VALUES (%s, %s, %s, %s, %s,%s,%s)",
                        (libro.getTitulo(), libro.getAutor(), libro.getTipo(), libro.getPrecio(),libro.getIdUsuario(),libro.getImagen(),libro.getFechaLimite()))
            conn.commit()
            print("Libro guardado con éxito")
            cur.close() 

        except Exception as e:
            print(f"Error al guardar usuario: {e}")

        finally:
            Conexion.cerrar(conn) 



def crear_tabla():
        conn = Conexion.conectar()
        if not conn:
            print("No se pudo conectar a la base de datos.")
            return  
        
        try:
            cur=conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS libros (
                    id SERIAL PRIMARY KEY,
                    titulo VARCHAR(100),
                    autor VARCHAR(100),
                    tipo VARCHAR(100),
                    precio NUMERIC(10, 2) DEFAULT 0.00,
                    idUsuario INTEGER REFERENCES usuarios(id),
                    imagen BYTEA,
                    fecha_limite TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    
                )
            """)
            conn.commit()
            cur.close()  
        except Exception as e:
            print(f"Error al crear la tabla: {e}")