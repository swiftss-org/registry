from flask import url_for

from app.models import Patient
from app.util.filter import like_all


def test_patient(flask_client_logged_in):
    flask_client = flask_client_logged_in
    test_patient_dict = dict(name='Test Patient',
                             gender='F',
                             center_id='1'
                             )

    # Create a Patient and assert the form return ok.
    response = flask_client.post(url_for('patient_create'), data=test_patient_dict, follow_redirects=True)
    assert response.status == '200 OK'
    assert 'New patient details for {} have been registered.'.format(test_patient_dict['name']) in str(response.data)

    # Assert that the patient we create is actually in the database
    from app import db
    f = like_all({Patient.name: test_patient_dict['name']})
    patients = db.session.query(Patient).filter(f).order_by(Patient.name).all()
    assert len(patients) == 1
    assert patients[0].name == test_patient_dict['name']

    # Assert that patient_search can find the patient
    response = flask_client.post(url_for('patient_search'),
                                 data=test_patient_dict, follow_redirects=True)
    assert response.status == '200 OK'
