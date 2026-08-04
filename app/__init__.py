import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from config import config_by_name, Config

def setup_logging(app: Flask):
    """Configures application file and console logging."""
    if not os.path.exists(app.config['LOG_DIR']):
        os.makedirs(app.config['LOG_DIR'], exist_ok=True)
        
    log_format = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s (%(lineno)d): %(message)s'
    )
    
    # File handler for logs/app.log
    file_handler = RotatingFileHandler(
        app.config['LOG_FILE'],
        maxBytes=10 * 1024 * 1024,  # 10 MB limit
        backupCount=5
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_format)
    stream_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)
    
    app.logger.setLevel(logging.INFO)
    if not app.logger.handlers:
        app.logger.addHandler(file_handler)
        app.logger.addHandler(stream_handler)
    app.logger.info("MNIST AI application logging initialized.")

def create_app(config_name: str = 'dev') -> Flask:
    """Application factory for MNIST AI Flask web app."""
    app = Flask(
        __name__,
        template_folder=os.path.join(Config.BASE_DIR, 'templates'),
        static_folder=os.path.join(Config.BASE_DIR, 'static')
    )
    
    # Load configuration
    selected_config = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(selected_config)
    
    # Ensure necessary folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['MODEL_DIR'], exist_ok=True)
    os.makedirs(app.config['LOG_DIR'], exist_ok=True)
    
    # Initialize logging
    setup_logging(app)
    
    # Import and register blueprints/routes
    with app.app_context():
        from app.routes import main_bp
        app.register_blueprint(main_bp)
        
        # Pre-load model on startup to ensure high performance inference
        from app.predictor import get_predictor
        try:
            predictor = get_predictor()
            if predictor.is_loaded():
                app.logger.info(f"Model successfully loaded on startup: {predictor.model_path}")
            else:
                app.logger.warning("Model file not found on startup. Model will be auto-detected when placed in model/.")
        except Exception as e:
            app.logger.error(f"Error loading model during startup: {str(e)}")
            
    return app
