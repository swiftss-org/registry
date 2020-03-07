import argparse

from app import create_app

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tanzania Mesh Hernia Repository')
    parser.add_argument('--no-flask', help='do not run Flask', dest='flask', action='store_false')
    parser.add_argument('--flask', help='run Flask (default)', dest='flask', action='store_true', default=True)
    args = parser.parse_args()

    application = create_app()

    if args.flask:
        application.run(debug=True)
