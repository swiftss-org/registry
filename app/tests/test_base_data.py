from app.models import User, Center, Drug


def test_base_data(database_session):
    assert len(database_session.query(User).all()) == 3
    assert len(database_session.query(Center).all()) == 6
    assert len(database_session.query(Drug).all()) == 20
