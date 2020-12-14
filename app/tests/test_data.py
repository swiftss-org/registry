import logging
import random
from datetime import timedelta, date
from typing import List

from app import constants
from app.models import User, Patient, Center
from app.tests import names
from app.util import pwd_generator


def test_base_data(database_session):
    create_sample_data(database_session,
                       num_users=12,
                       num_patients=50)

    assert len(database_session.query(User).all()) == 12 + 2
    assert len(database_session.query(Center).all()) == 25


def create_test_user(session):
    test_user = User(name='Test, Account', email=constants.TEST_ACCOUNT_EMAIL)
    test_user.set_password(constants.TEST_ACCOUNT_PASSWORD)
    session.add(test_user)


def create_sample_data(session, num_users: int, num_patients: int):
    logging.info('Running data generator.')

    users = _users(num_users)
    session.add_all(users)

    centers = _centers()
    session.add_all(centers)

    patients = _patients(num_patients, centers, users)
    session.add_all(patients)


def _users(num: int) -> List[User]:
    users = []

    existing_names = set()
    for i in range(0, num - 1):
        gender = random.choice(['M', 'F'])
        name = names.name(gender)

        while name in existing_names:
            name = names.name(gender)

        email = names.email(name)

        u = User(name=name, email=email)
        u.set_password(pwd_generator.password())
        users.append(u)

        existing_names.add(u.name)

    return users


def _patients(num: int, centers, users) -> List[Patient]:
    patients = []
    for i in range(0, num):
        gender = random.choice(['M', 'F'])
        name = names.name(gender)

        patients.append(Patient(
            name=name,
            gender=gender,
            dob=date.today() - timedelta(days=random.randint(365 * 18, 365 * 90)),
            dob_year_only=random.choice([True, False]),
            national_id=_national_id(),
            address=names.address(),
            phone_1=names.phone(),
            phone_1_comments=names.phone_type(),
            center=random.choice(centers),
            created_by=random.choice(users),
            updated_by=random.choice(users)
        ))

    return patients


def _national_id():
    constants.NATIONAL_ID_COUNTER = constants.NATIONAL_ID_COUNTER + random.randint(100, 10000)
    return str(constants.NATIONAL_ID_COUNTER)


def _centers():
    centers = []
    for city in names.cities:
        name = names.center(city)
        address = name + '\n' + city
        centers.append(Center(name=name, address=address))

    return centers


def _date_of_surgery(los: int) -> date:
    return date.today() - timedelta(days=random.randint(los, 5 * 365))


def _date_of_dc(date_of_surgery: date, los: int):
    return date_of_surgery + timedelta(days=los)
