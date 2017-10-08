"""
configuration
"""
import os

DEFAULT_PATH = os.path.join(os.path.expanduser('~'), '.iDict')


class Config(object):
    URL = ''
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    URL = 'dev-dict.db'
    DATABASE_URL = 'sqlite:///' + os.path.join(DEFAULT_PATH, URL)


class TestingConfig(Config):
    TESTING = True
    URL = 'test-dict.db'
    DATABASE_URL = 'sqlite:///' + os.path.join(DEFAULT_PATH, URL)


class ProductionConfig(Config):
    URL = 'prod-dict.db'
    DATABASE_URL = 'sqlite:///' + os.path.join(DEFAULT_PATH, URL)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
