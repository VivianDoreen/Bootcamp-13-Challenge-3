# config file


class MainConfiguration(object):
    """ Main configuration class"""
    DEBUG = False
    CSRF_ENABLED = True


class DevelopmentEnvironment(MainConfiguration):
    """ Configurations for development"""
    DEBUG = True



class TestingEnvironment(MainConfiguration):
    """ Configurations for Testing environment"""
    DEBUG = True
    TESTING = True


class StagingEnvironment(MainConfiguration):
    """ Configurations for staging environment"""
    DEBUG = True


class ProductionEnvironment(MainConfiguration):
    """ Configurations for production environment"""
    DEBUG = False
    TESTING = False


application_config = {
    'MainConfig': MainConfiguration,
    'TestingEnv': TestingEnvironment,
    'DevelopmentEnv': DevelopmentEnvironment,
    'ProductionEnv': ProductionEnvironment
}