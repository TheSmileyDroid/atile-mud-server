import os
import string
import random

random_str = string.ascii_letters + string.digits + string.ascii_uppercase
key = 'senha'
DEBUG = True
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///atile.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = key
