import os
from glob import glob

APP_NAME = 'd4rkvv0r1.de'

DEBUG = os.getenv('DEBUG', False)
MODE = os.getenv('MODE', False)

DATABASE_URL = os.getenv('DATABASE_URL')
JWT_SECRET = os.getenv('JWT_SECRET')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
INTERVAL = int(os.getenv('INTERVAL', 10))

CORS_ALLOW_ORIGINS = [
    'https://d4rkvv0r1.de',
    'http://localhost',
    'http://localhost:8000',
    'http://127.0.0.1',
    'http://127.0.0.1:8000',
    'http://0.0.0.0',
    'http://0.0.0.0:8000'
]

APP_PARAMS = {
    'redoc_url': None,
    'docs_url': '/docs' if DEBUG else None,
}


def auto_load_models():
    return [model[:-3].replace('/', '.') for model in glob('app/src/*/models.py')]


APPS_MODELS = [
    'app.src.auth.models',
    'app.src.user.models',
    'app.src.link.models',
    'app.src.grab.models',
    'aerich.models'
]

ORM = {
    'connections': {
        'default': DATABASE_URL
    },
    'apps': {
        'models': {
            'models': APPS_MODELS,
            'default_connection': 'default',
        },
    },
}
