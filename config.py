import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    FLASK_ENV = os.getenv('FLASK_ENV')
#<<<<<<< HEAD
#<<<<<<< HEAD
    DATABASE_URL = os.getenv('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
#=======
#=======
#>>>>>>> 8b23eae46e2afdda327046014522a4a095078e9a

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#<<<<<<< HEAD
#>>>>>>> 18e99efacace2f67b1fb30cabc3d86d02dbd7574
#=======
#>>>>>>> 8b23eae46e2afdda327046014522a4a095078e9a
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')  
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')