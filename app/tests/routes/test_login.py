from flask import url_for

from app import constants


def test_login(flask_client):
    _logout(flask_client)

    response = _login(flask_client, 'bad_email', 'bad_password')
    assert response.status == '200 OK'
    assert 'Please Sign In' in str(response.data)

    response = _login(flask_client, constants.TEST_ACCOUNT_EMAIL, constants.TEST_ACCOUNT_PASSWORD)
    assert response.status == '200 OK'
    assert 'Please Sign In' not in str(response.data)

    response = _logout(flask_client)
    assert response.status == '200 OK'


def _login(flask_client, username, password):
    return flask_client.post(url_for('login'), data=dict(
        username=username,
        password=password,
    ), follow_redirects=True)


def _logout(flask_client):
    return flask_client.get(url_for('logout'), follow_redirects=True)
