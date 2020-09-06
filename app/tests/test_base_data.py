from app import base_data
from app.models import User, Center, Drug


def test_base_data(database_session):
    base_data.create(database_session)

    assert len(database_session.query(User).all()) == 2
    assert len(database_session.query(Center).all()) == 6
    assert len(database_session.query(Drug).all()) == 10