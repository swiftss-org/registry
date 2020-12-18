import logging
import os
import tempfile

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from app import formatters
from app.util import pwd_generator, strtobool
from app.util.strtobool import strtobool

db = SQLAlchemy()
login = LoginManager()

LOG_FORMAT = '%(asctime)-15s [%(levelname)s] %(message)s'
LOG_DATE_FMT = '%Y-%m-%d %H:%M:%S'


from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')  # Path to .env file
load_dotenv(dotenv_path)


def create_app(unit_test=False):
    """Initialize the core app."""

    init_logging()

    app = Flask(__name__, instance_relative_config=False)

    if unit_test:
        database_url = 'sqlite://'
    elif 'RDS_URL' in os.environ or 'DATABASE_URL' in os.environ:
        database_url = os.environ.get('RDS_URL') or os.environ.get('DATABASE_URL')
    elif 'RDS_HOSTNAME' in os.environ:
        DATABASE = {
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }

        database_url = 'mysql+mysqlconnector://%(USER)s:%(PASSWORD)s@%(HOST)s:%(PORT)s/%(NAME)s' % DATABASE
    else:
        database_url = 'sqlite:///' + os.path.join(tempfile.gettempdir(), 'registry.db')

    logging.info('Initalising SQLAlchemy with database URL {}'.format(database_url))

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or pwd_generator.password(),
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_POOL_RECYCLE=280,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=not unit_test,
        DEFAULT_TEST_ACCOUNT_LOGIN=bool(strtobool(os.environ.get('DEFAULT_TEST_ACCOUNT_LOGIN', 'False'))),
        MINIMUM_PASSWORD_STRENGTH=0.3
    )

    # Initialize Plugins
    db.init_app(app)
    app.db = db

    # Setup the login manager
    login.init_app(app)
    login.login_view = 'login'

    # Register custom formattters
    app.jinja_env.filters['datetime'] = formatters.format_datetime

    # Set custom JSON Encode
    # app.json_encoder = CustomJSONEncoder()

    with app.app_context():
        from app import routes

    return app


def init_logging():
    log_level_name = os.environ.get('LOG_LEVEL', 'INFO')
    log_level = logging.getLevelName(log_level_name.upper())
    if not log_level:
        log_level = logging.INFO

    logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FMT, level=log_level)


if __name__ == '__main__':
    print('Please start the registry application from Flask:')
    print('\t`export FLASK_APP="application.py"`')
    print('\t`flask run`\n')
elif os.environ.get("HEROKU"):
    app = create_app()
