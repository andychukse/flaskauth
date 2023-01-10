"""Flask configuration."""
import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    APP_NAME=os.environ.get("APP_NAME")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG") or False
    TESTING = os.environ.get("FLASK_TESTING") or False
    APPLICATION_ROOT = os.environ.get("APPLICATION_ROOT") or os.getcwd()
    # SERVER_NAME=
    SECRET_KEY = os.environ.get('SECRET_KEY') or '7vgtdjh_fgWQgdhLbas9df9409sf6a6ds4f3435fa64ˆGggfXV6Miy'
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    # SQLALCHEMY_ECHO=
    # SQLALCHEMY_ENGINE_OPTIONS=
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    MAIL_USE_SSL = 'True' == os.environ.get("MAIL_USE_SSL")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    MAIL_DEBUG = 'True' == os.environ.get("MAIL_DEBUG")
    MAIL_SUPPRESS_SEND = False

    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    AWS_KEY_ID = os.environ.get('AWS_KEY_ID')
    AWS_BUCKET = os.environ.get('AWS_BUCKET')
    CELERY_CONFIG = {
    'broker_url': 'redis://localhost:6379',
    'result_backend': 'redis://localhost:6379',
    }
    JWT_DURATION=os.environ.get("JWT_DURATION") or 10080
    REFRESH_TOKEN_DURATION=os.environ.get("REFRESH_TOKEN_DURATION") or 525600
class ProductionConfig(Config):
    FLASK_ENV = 'production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class DevelopmentConfig(Config):
    FLASK_ENV = "development"
    DEVELOPMENT = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True