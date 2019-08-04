import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'wakerspace'
    SQLALCHEMY_DATABASE_URI = 'mysql://waker:password@localhost/wakerspace'
