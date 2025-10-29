import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-super-segura-cambiar-en-produccion'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sistema.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True