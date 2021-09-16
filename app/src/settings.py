import os

APP_NAME = os.getenv('APP_NAME')
DATABASE_URL = os.getenv('DATABASE_URL')
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = os.getenv('ALGORITHM')
INTERVAL = int(os.getenv('INTERVAL', 10))

ORM = {
    'connections': {
        'default': DATABASE_URL
    },
    'apps': {
        'models': {
            'models': ['src.models', 'aerich.models'],
            'default_connection': 'default',
        },
    },
}