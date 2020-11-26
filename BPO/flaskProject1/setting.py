class Config(object):
    DEBUG=False
    TESTING = False
    DATABASE_URL = 'sqlite://:memory:'
class ProductionConfig(Config):
    DATABASE_URL = 'mysql://user@localhost/foo'
class DevelopmentConfig(Config):
    DEBUG = True
class TestingConfig(Config):
    TESTING = True

instance_relative=True
root_path='setting.py'
