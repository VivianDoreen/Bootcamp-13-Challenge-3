# config file
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class MainConfiguration(object):
    """ Main configuration class"""
    DEBUG = False
    CSRF_ENABLED = True


class DevelopmentEnvironment(MainConfiguration):
    """ Configurations for development"""
    ENV = 'development'
    DATABASE = 'ManagerStore'
    DEBUG = True

class TestingEnvironment(MainConfiguration):
    """ Configurations for Testing environment"""
    ENV = 'testing'
    DATABASE = 'testdatabase'
    DEBUG = True
    TESTING = True

class ProductionEnvironment(MainConfiguration):
    """ Configurations for production environment"""
    ENV = 'production'
    DEBUG = False
    TESTING = False
    HOST = 'ec2-23-23-101-25.compute-1.amazonaws.com'
    # DATABASE = 'dec9gdnj02hff8'
    # USER = 'xtyhcyxhshwipn'
    # PASSWORD = '40750512ca9a1bb9de7b8793fc4d2494caca32c156efc895cf529aa69111b39e'


application_config = {
    'MainConfig': MainConfiguration,
    'TestingEnv': TestingEnvironment,
    'DevelopmentEnv': DevelopmentEnvironment,
    'ProductionEnv': ProductionEnvironment
}