import argparse

from app import create_app
from app.admin import admin_command
from app.tests import data_generator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tanzania Mesh Hernia Repository')
    parser.add_argument('--reset-db', help='drop and create the database', action='store_true')
    parser.add_argument('--generate', help='generate dummy test data', action='store_true')
    parser.add_argument('--no-flask', help='do not run Flask', dest='flask', action='store_false')
    parser.add_argument('--flask', help='run Flask (default)', dest='flask', action='store_true', default=True)
    args = parser.parse_args()

    application = create_app()
    with application.app_context():

        if args.reset_db:
            admin_command.execute(application, 'reset_db')

        if args.generate:
            admin_command.execute(application, 'generate')

    if args.flask:
        application.run(debug=True)
