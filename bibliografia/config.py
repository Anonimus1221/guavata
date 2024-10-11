import os
import secrets

class Config:
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'guavata.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    DEBUG = os.environ.get('FLASK_DEBUG') or False
    SECRET_KEY = secrets.token_urlsafe(32)
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    


