from flask import Flask
import os

import yaml

import pandamonium.commands as commands
import pandamonium.db as db
import pandamonium.auth as auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    with app.open_resource('db_credentials.yml') as db_credentials_file:
        db_credentials = yaml.safe_load(db_credentials_file)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_CREDENTIALS=db_credentials,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    commands.register_commands(app)
    app.teardown_appcontext(db.close_db)
    app.register_blueprint(auth.blueprint)

    return app
