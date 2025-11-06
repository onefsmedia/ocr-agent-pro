from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import config
import os
from sqlalchemy.exc import OperationalError

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    """Application factory pattern"""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Set the template and static folders relative to the project root
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    
    # Try the default config first
    app.config.from_object(config[config_name])
    
    # Test database connection and fallback to SQLite if needed
    try:
        from sqlalchemy import create_engine
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], 
                             connect_args={'connect_timeout': 2})
        with engine.connect():
            print(f"Connected to database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    except (OperationalError, Exception) as e:
        print(f"PostgreSQL connection failed: {e}")
        print("Falling back to SQLite database...")
        app.config.from_object(config['sqlite'])
        print(f"Using SQLite: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Create upload directory
    upload_dir = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    from app.routes.auth import auth_bp
    from app.api.deepseek_routes import deepseek_bp
    from app.api.lesson_routes import lesson_bp
    from app.api.storage_routes import storage_bp
    from app.api.prompt_routes import prompt_api
    from app.routes.onlyoffice_routes import onlyoffice_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(deepseek_bp)
    app.register_blueprint(lesson_bp)
    app.register_blueprint(storage_bp)
    app.register_blueprint(prompt_api)  # Has its own url_prefix='/api/prompts'
    app.register_blueprint(onlyoffice_bp)
    
    return app