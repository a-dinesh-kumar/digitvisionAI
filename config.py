import os

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'digitvision-ai-deep-learning-secret-key-2026')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB maximum upload size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    # Model configuration
    MODEL_DIR = os.path.join(BASE_DIR, 'model')
    PREFERRED_MODEL_NAMES = [
        # 'mnist_model.h5',
        # 'mnist_model.keras',
        # 'digits_intel.h5',
        # 'digits_intel.keras',
        'latest_model.h5',
        'latest_model.keras'
    ]
    
    # Image preprocessing specs matching MNIST dataset
    IMAGE_SIZE = (28, 28)
    COLOR_MODE = 'L'  # Grayscale
    
    # Logging configuration
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    LOG_FILE = os.path.join(LOG_DIR, 'app.log')
    LOG_LEVEL = 'INFO'

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = False
    TESTING = True
    UPLOAD_FOLDER = os.path.join(Config.BASE_DIR, 'tests', 'test_uploads')

# Mapping environment names to configuration objects
config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'test': TestingConfig,
    'default': DevelopmentConfig
}
