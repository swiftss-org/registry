from app.tests import data_generator


def execute(application, command):
    if command.lower().strip() == 'reset_db':
        return _reset_db(application)
    elif command.lower().strip() == 'generate':
        return _generate(application)
    else:
        return "No such command."


def _generate(application):
    session = application.db.session
    with session.begin_nested():
        data_generator.create_sample_data(session,
                                          num_users=12,
                                          num_patients=50)
    session.commit()
    return "Done"


def _reset_db(application):
    application.db.drop_all()
    application.db.create_all()

    session = application.db.session
    with session.begin_nested():
        data_generator.create_default_data(session)
    session.commit()

    return "Done"
