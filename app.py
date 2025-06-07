# Importamos Flask para crear la aplicación web
from flask import Flask  

# Importamos CORS para permitir peticiones desde otros dominios (como un frontend separado)
from flask_cors import CORS  

# Importamos los blueprints de los controladores para mapear rutas en el servidor

from controllers.user_controller import usuario_bp  
from controllers.subForo_controller import subForo_bp
from controllers.libro_controller import libro_bp
from controllers.mensaje_controller import mensaje_bp
from controllers.puja_controller import puja_bp

from controllers import user_controller
from controllers import subForo_controller
from controllers import libro_controller
from controllers import mensaje_controller
from controllers import puja_controller


from models.user import Usuario
from models.subForo import SubForo
from models.libro import Libro
from models.mensaje import Mensaje
from models.puja import Puja




app = Flask(__name__)  




CORS(app, supports_credentials=True)

# Registramos el blueprint (usuario_bp) en la aplicación para definir las rutas del controlador de usuarios

app.register_blueprint(subForo_bp, url_prefix='/subForo')
app.register_blueprint(usuario_bp, url_prefix='/usuario')
app.register_blueprint(libro_bp, url_prefix='/libro')
app.register_blueprint(mensaje_bp, url_prefix='/mensaje')
app.register_blueprint(puja_bp, url_prefix='/puja')

user_controller.crear_tabla()
subForo_controller.crear_tabla()
libro_controller.crear_tabla()
mensaje_controller.crear_tabla()
puja_controller.crear_tabla()


if __name__ == '__main__':  
    app.run(debug=True)  
    
    
    
    # El servidor Flask es http://127.0.0.1:5000/