from models.puja import Puja
from flask import Blueprint, request, jsonify
from DB.conectar_db import Conexion
from datetime import datetime

puja_bp = Blueprint('puja_bp', __name__)


@puja_bp.route('/pujarPrecio', methods=['POST'])
def pujar():
    data = request.json
    idLibro = data['Libro']
    idUsuario = data['Usuario']
    monto = data['monto']

    try:
        monto = float(data['monto'])
    except (ValueError, TypeError):
        return jsonify({"error": "El monto debe ser un número válido"}), 400

    
    
    

    conn = Conexion.conectar()
    cur = conn.cursor()

    try:
        monto = float(monto)
    except (Exception):
        cur.close()
        conn.close()
        return jsonify({"error": "El monto debe ser un número "}), 400
    


    

    
    cur.execute("SELECT MAX(monto) FROM pujas WHERE idLibro = %s", (idLibro,))
    puja_mayor = cur.fetchone()[0]

    if puja_mayor is None:
        # Primera puja: debe ser igual o mayor al precio del libro
        cur.execute("SELECT precio FROM libros WHERE id = %s", (idLibro,))
        precio_libro = cur.fetchone()
        if precio_libro is None:
            cur.close()
            conn.close()
            return jsonify({"error": "Libro no encontrado"}), 404
        precio_libro = float(precio_libro[0])
        if monto < precio_libro:
            cur.close()
            conn.close()
            return jsonify({"error": "La primera puja debe ser igual o mayor al precio del libro"}), 400
    else:
        # Hay pujas previas: debe ser mayor a la puja actual
        if monto <= float(puja_mayor):
            cur.close()
            conn.close()
            return jsonify({"error": "La puja debe ser mayor a la actual"}), 400
        

    cur.execute("SELECT fecha_limite FROM libros WHERE id = %s", (idLibro,))
    fecha_limite = cur.fetchone()[0]
    if fecha_limite and datetime.now() > fecha_limite:
        cur.close()
        conn.close()
        return jsonify({"error": "La subasta ha finalizado. No se pueden realizar más pujas."}), 400    

    
    cur.execute(
        "INSERT INTO pujas (idLibro, idUsuario, monto) VALUES (%s, %s, %s)",
        (idLibro, idUsuario, monto)
    )

    conn.commit()
    cur.close()

    conn.close()
    return jsonify({"mensaje": "Puja realizada"}), 201

@puja_bp.route('/mayor/<int:idLibro>', methods=['GET'])
def mayor_puja(idLibro):
    conn = Conexion.conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.monto, p.idUsuario, u.nombre
        FROM pujas p
        JOIN usuarios u ON p.idUsuario = u.id
        WHERE p.idLibro = %s
        ORDER BY p.monto DESC, p.fecha_puja ASC
        LIMIT 1
    """, (idLibro,))
    puja = cur.fetchone()
    cur.close()
    conn.close()
    if puja:
        return jsonify({
            "monto": puja[0],
            "idUsuario": puja[1],
            "nombreUsuario": puja[2]
        })
    else:
        return jsonify({"monto": None, "idUsuario": None, "nombreUsuario": None})


def crear_tabla():
        conn = Conexion.conectar()
        if not conn:
            print("No se pudo conectar a la base de datos.")
            return  
        
        try:
            cur=conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS pujas (
                    id SERIAL PRIMARY KEY,
                    idLibro INTEGER REFERENCES libros(id),
                    idUsuario INTEGER REFERENCES usuarios(id),
                    monto NUMERIC NOT NULL,
                    fecha_puja TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            cur.close()  
        except Exception as e:
            print(f"Error al crear la tabla: {e}")

