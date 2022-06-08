class Config:
    SECRET = "secret"
    ALGORITHM = "HS256"
    TESTING = False
    MONGO_URI = "mongodb://localhost:27017/aimmo_ojt"


class LocalConfig(Config):
    MONGO_URI = "mongodb://localhost:27017/aimmo_ojt"
    TESTING = True
    DEBUG = True


class TestConfig(Config):
    MONGO_URI = "mongomock://127.0.0.1:27017/aimmo_ojt?connect=false"
    TESTING = True


config_by_name = dict(dev=LocalConfig, test=TestConfig)
