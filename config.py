"""
Configuration module for Autonomous Trucks Fleet Management System
Loads configuration from environment variables with sensible defaults
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class"""

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')

    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))

    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'autonomous_trucks')

    # Google Maps API
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

    # Carla Simulation (Optional)
    CARLA_HOST = os.getenv('CARLA_HOST', 'localhost')
    CARLA_PORT = int(os.getenv('CARLA_PORT', 2000))
    CARLA_TIMEOUT = float(os.getenv('CARLA_TIMEOUT', 10.0))

    # Application Settings
    AVERAGE_FUEL_EFFICIENCY_KM_PER_L = float(
        os.getenv('AVERAGE_FUEL_EFFICIENCY_KM_PER_L', 2.5)
    )

    @staticmethod
    def validate():
        """Validate critical configuration values"""
        warnings = []

        if not Config.GOOGLE_MAPS_API_KEY:
            warnings.append("WARNING: GOOGLE_MAPS_API_KEY not set. Map features will not work.")

        if Config.SECRET_KEY == os.urandom(24).hex():
            warnings.append("WARNING: Using random SECRET_KEY. Set SECRET_KEY in .env for production.")

        return warnings


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    MONGODB_DATABASE = 'autonomous_trucks_test'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration object based on environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
