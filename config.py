import os
DEBUG = False
TESTING = False
CSRF_ENABLED = True
SECRET_KEY = 'qwertyuiop'
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql:///atile_dev')