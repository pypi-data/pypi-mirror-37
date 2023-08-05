import os

import mbq.metrics

import dj_database_url


SECRET_KEY = 'fake-key'
DEBUG = True
RANCH = {
    'env': 'Test',
    'service': 'test-service',
}

database_url = os.environ.get('DATABASE_URL', 'mysql://root:@mysql:3306/ranchdb')
DATABASES = {
    'default': dj_database_url.parse(database_url),
}

INSTALLED_APPS = [
    'mbq.ranch',
]

USE_TZ = True

mbq.metrics.init()
