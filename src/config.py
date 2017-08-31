import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY")

    CACHE_TYPE = 'simple'

    USE_TZ = True

    API_PREFIX = '/api/v1'
    API_RESULT_PER_PAGE = 4

    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_BACKEND = CELERY_BROKER_URL
    DEFAULT_CELERY_RETRY_DELAY = int(os.environ.get('DEFAULT_CELERY_RETRY_DELAY', 60))  # 1 minute
    DEFAULT_CELERY_MAX_RETRIES = int(os.environ.get('DEFAULT_CELERY_MAX_RETRIES', 5))
    CELERY_IMPORTS = [
        'service.tasks'
    ]
    INSTALLED_APPS = [
        'server',
        'service',
    ]

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FOLDER_DIR = basedir


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'