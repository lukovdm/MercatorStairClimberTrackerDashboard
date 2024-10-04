import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'BJT9wzy@bcx1dge4twa'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.environ.get("DATABASE", os.path.join(basedir, 'database.db'))
    UPLOAD_FOLDER = os.environ.get("UPLOAD", os.path.join(basedir, 'photos'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False