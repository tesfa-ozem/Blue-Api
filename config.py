import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMINS = ['your-email@example.com']
    PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
    UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)