import os
from glob import glob

APP_NAME = os.getenv('APP_NAME')
DATABASE_URL = os.getenv('DATABASE_URL')
JWT_SECRET = os.getenv('JWT_SECRET')
SECRET_KEY = os.getenv('SECRET')
ALGORITHM = os.getenv('ALGORITHM')
INTERVAL = int(os.getenv('INTERVAL', 10))


def auto_models():
    return [model[:-3].replace('/', '.') for model in glob('app/src/*/models.py')]


APPS_MODELS = [
    'app.src.auth.models',
    'app.src.user.models',
    'app.src.link.models',
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
