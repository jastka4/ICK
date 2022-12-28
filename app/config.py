import os

basedir = os.path.abspath(os.path.dirname(__file__))
local_base = 'postgresql://admin:admin@localhost:5432/'
database_name = 'face_recognition'


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', local_base + database_name)


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = local_base + database_name + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = (
        'postgresql://{nam}:{pas}@localhost/{dbn}?host=/cloudsql/{con}').format(
        nam=os.getenv('DATABASE_USER'),
        pas=os.getenv('DATABASE_PASSWORD'),
        dbn=os.getenv('DATABASE_NAME'),
        con=os.getenv('DATABASE_CONNECTION'),
    )
