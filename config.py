import os
class Config:
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    #import pymysql
    #pymysql.install_as_MySQLdb()
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.getenv("MY_SECRET")
    JWT_SECRET_KEY = os.getenv("MY_JWT_SECRET")
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    JWT_ACCESS_TOKEN_EXPIRES = False
    SQLALCHEMY_ECHO= True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.getenv("MY_SECRET")
    JWT_SECRET_KEY = os.getenv("MY_JWT_SECRET")
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    JWT_ACCESS_TOKEN_EXPIRES = False
    SQLALCHEMY_ECHO= True

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
    )
