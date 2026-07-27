from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config

#Crear instancias
db = SQLAlchemy()
migrate =Migrate()
login_manager= LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    #inicializar base de datos
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    #Configuración de Login Manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Inicia sesión para continuar'
    login_manager.login_message_category ='Warning'
    
    #Modelos
    from app.models import Usuario
    from app.models import Categoria
    from app.models import Pedido
    from app.models import Producto
   
    # User Loader: Flask -login necesita saber como cargar un Usuario por ID
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    #Blueprints#FACTORY
    from app.blueprints.public import public_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.admin import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, utl_prefix='/auth')
    app.register_blueprint(admin_bp, utl_prefix='/admin')

    return app

