from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = 'dummy-secret-key'

INSTALLED_APPS = [
]

DATABASES={
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

ROOT_URLCONF='test.urls'

USE_TZ = True  # Avoid deprecation warning

RATED_REDIS = {
    'host': 'localhost',
    'port': 16379,
}
