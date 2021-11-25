import random

pathURI_allow = ['/static','/login']
regexPath = '^(%s)'%'|'.join(pathURI_allow)

class Config(object):
    SECRET_KEY = random.randbytes(random.randint(500,1000)).hex()
    
class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True