import logging

from app.tests import data_generator


def execute(application, command):
    if command.lower().strip() == 'reset_db':
        return _reset_db(application)
    elif command.lower().strip() == 'generate':
        return _generate(application)
    else:
        return "No such command."


