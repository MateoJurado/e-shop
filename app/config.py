import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    
    # Configuración de la BD con valores por defecto para entorno local
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')       # En XAMPP suele estar vacía ''
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'ecommerce_db')  
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ==========================================
    # CONFIGURACIÓN PARA SUBIDA DE IMÁGENES
    # ==========================================
    # Ruta absoluta hacia la carpeta app/static/img
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'img')
    
    # Tamaño máximo permitido (Ejemplo: 2 MB)
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    
    # Extensiones permitidas (Requerimiento del checklist)
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'webp','png'}