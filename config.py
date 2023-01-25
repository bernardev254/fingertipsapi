class Config:
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    #import pymysql
    #pymysql.install_as_MySQLdb()
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://bernard:b1yeHU9laEALTCbdGj9L1y6bPqqWat9Z@dpg-cf8cnrqrrk0e2at8bco0-a.oregon-postgres.render.com/fingertips"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "SECRET_KEY"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    JWT_ACCESS_TOKEN_EXPIRES = False
    SQLALCHEMY_ECHO= "True"

class TestingConfig(Config):
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgres://bernard:b1yeHU9laEALTCbdGj9L1y6bPqqWat9Z@dpg-cf8cnrqrrk0e2at8bco0-a.oregon-postgres.render.com/fingertips"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "SECRET_KEY"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    JWT_ACCESS_TOKEN_EXPIRES = False
    SQLALCHEMY_ECHO= "True"

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
    )
