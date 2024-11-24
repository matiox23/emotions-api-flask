from flask import Flask
from werkzeug.exceptions import HTTPException
from flask_cors import CORS  # Importar CORS
from src.specification import spec
from src.db.database import create_db_and_tables
from src.controller.emotion_controller import emotions_router
from src.controller.user_controller import user_router
from src.controller.auth_controller import auth_router
from src.exception.handler import handle_exception
from src.controller.examen_controller import examen_router
from src.controller.resultado_controller import resultado_router


app = Flask(__name__)
CORS(app)
  # Inicializar CORS

app.register_error_handler(HTTPException, handle_exception)
app.register_blueprint(emotions_router, url_prefix='/api')
app.register_blueprint(user_router, url_prefix='/api')
app.register_blueprint(auth_router, url_prefix='/api')
app.register_blueprint(examen_router, url_prefix='/api')

app.register_blueprint(resultado_router, url_prefix='/api')

spec.register(app)

if __name__ == '__main__':
    create_db_and_tables()
    app.run(debug=True)
