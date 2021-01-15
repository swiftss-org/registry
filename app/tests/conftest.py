import pytest

from app import constants, base_data
from app import initialise
from app.tests import test_data
from app.tests.routes.test_login import _login
from application import create_app

TEST_NUM_USERS = 12
TEST_NUM_PATIENTS = 50


@pytest.fixture(scope="function")
def flask_application():
    application = create_app(unit_test=True)

    with application.app_context():
        application.db.create_all()
        base_data.create(application.db.session)
        test_data.create_test_user(application.db.session)

        yield application

        application.db.session.close()
        application.db.drop_all()


@pytest.fixture(scope="function")
def database_session(flask_application):
    with flask_application.app_context():
        yield flask_application.db.session


@pytest.fixture(scope="function")
def flask_client(flask_application):
    with flask_application.app_context():
        with flask_application.test_request_context():
            yield flask_application.test_client()


@pytest.fixture(scope="function")
def flask_client_logged_in(flask_client):
    _login(flask_client, constants.TEST_ACCOUNT_EMAIL, constants.TEST_ACCOUNT_PASSWORD)
    yield flask_client
