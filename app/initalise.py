import logging
import os

from app import strtobool, base_data
from app.tests import test_data


def initalise(application):
    logging.info('Initalising application.')

    if strtobool(os.environ.get('ADMIN_RESET_DB', str(False))):
        logging.info('Found ADMIN_RESET_DB -- resetting database...')
        _reset_db(application)

    if strtobool(os.environ.get('ADMIN_GENERATE_DATA', str(False))):
        logging.info('Found ADMIN_GENERATE_DATA -- generating data....')
        _generate(application)

    logging.info('Initalising application complete.')


def _generate(application):
    session = application.db.session
    with session.begin_nested():
        test_data.create_sample_data(session,
                                     num_users=12,
                                     num_patients=50)
    session.commit()
    return "Done"


def _reset_db(application):
    application.db.drop_all()
    application.db.create_all()

    session = application.db.session
    try:
        with session.begin_nested():
            base_data.create(session)

            if application.config.get('DEFAULT_TEST_ACCOUNT_LOGIN'):
                base_data.create_test_user(session)

        session.commit()
        logging.info('Session Committed')
    except Exception as e:
        session.rollback()
        raise e

    return "Done"
