import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///reimbursement.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    UPLOAD_FOLDER = "static/uploads/"
    MAX_UPLOAD_SIZE = 16 * 1024 * 1024  #16MB

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


admin_password = "adminpass"