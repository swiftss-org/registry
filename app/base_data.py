import logging
import random

from app import constants
from app.models import User, Center, Drug, DrugType, MeshType


def create(session):
    _create_users(session)
    _create_centers(session)
    _create_drugs(session)
    _create_mesh_types(session)


def create_test_user(session):
    test_user = User(name='Test, Account', email=constants.TEST_ACCOUNT_EMAIL)
    test_user.set_password(constants.TEST_ACCOUNT_PASSWORD)
    test_user.center = random.choice(session.query(Center).all())
    session.add(test_user)


def _create_users(session):
    paul_user = User(name='Paul Smith', email='paul@swiftss.org', active=True)
    # This is clearly terrible but it will have to do for now.
    paul_user.set_password('EWCabre9AWj5T9fU')
    session.add(paul_user)
    logging.info('Create user {}'.format(paul_user.name))

    shim_user = User(name='Dr Mark Szymankiewicz', email='mark@swiftss.org', active=True)
    # This is clearly terrible but it will have to do for now.
    shim_user.set_password('dGm768RvJvA6Fgux')
    session.add(shim_user)
    logging.info('Create user {}'.format(shim_user.name))


def _create_centers(session):
    session.add(Center(name='Muheza, St Augustines', address='Muheza'))
    session.add(Center(name='Korogwe', address='Korogwe'))
    session.add(Center(name='Moshi, KCMC', address='Moshi'))
    session.add(Center(name='Arusha, ALMC', address='Arusha'))
    session.add(Center(name='Dodoma, Benjamin Mkapa National Hospital', address='Dodoma'))
    session.add(Center(name='Test Hospital', address='Test'))


def _create_drugs(session):
    session.add(Drug(name='Amoxicillin', type=DrugType.Antibiotic))
    session.add(Drug(name='Azithromycin', type=DrugType.Antibiotic))
    session.add(Drug(name='Amoxicillin / Clavulanate', type=DrugType.Antibiotic))
    session.add(Drug(name='Clindamycin', type=DrugType.Antibiotic))
    session.add(Drug(name='Cephalexin', type=DrugType.Antibiotic))
    session.add(Drug(name='Ciprofloxacin', type=DrugType.Antibiotic))
    session.add(Drug(name='Sulfamethoxazole / Trimethoprim', type=DrugType.Antibiotic))
    session.add(Drug(name='Metronidazole', type=DrugType.Antibiotic))
    session.add(Drug(name='Levofloxacin', type=DrugType.Antibiotic))
    session.add(Drug(name='Doxycycline', type=DrugType.Antibiotic))

    session.add(Drug(name='Amobarbital / Amytal', type=DrugType.Anesthetic))
    session.add(Drug(name='Methohexital /Brevital', type=DrugType.Anesthetic))
    session.add(Drug(name='Thiamylal / Surital', type=DrugType.Anesthetic))
    session.add(Drug(name='Thiopental / Penthothal / Thiopentone', type=DrugType.Anesthetic))
    session.add(Drug(name='Diazepam', type=DrugType.Anesthetic))
    session.add(Drug(name='Lorazepam', type=DrugType.Anesthetic))
    session.add(Drug(name='Midazolam', type=DrugType.Anesthetic))
    session.add(Drug(name='Etomidate', type=DrugType.Anesthetic))
    session.add(Drug(name='Ketamine', type=DrugType.Anesthetic))
    session.add(Drug(name='Propofol', type=DrugType.Anesthetic))


def _create_mesh_types(session):
    session.add(MeshType(name='TNMHP Mesh'))
    session.add(MeshType(name='KCMC / Northumbria Generic Mesh'))
    session.add(MeshType(name='Commercial Mesh'))
