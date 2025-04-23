
class Config:
    # SQLAlchemy configuration
    SQLALCHEMY_ECHO = True # echoes SQL for debug
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'EmmanuelAPISecretKey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///clients.db' #path to Db


