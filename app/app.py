import os

from flask import Flask

from .extensions import (
    bcrypt,
    cors,
    db,
    migrate,
)

# blueprints
from .auth import auth

# commands
from .commands import create_db, drop_db

__all__ = ("create_app",)

BLUEPRINTS = (auth,)
COMMANDS = (create_db, drop_db)


def create_app(config=None, app_name="face-recognition-api", blueprints=None):
    app = Flask(
        app_name,
        static_folder=os.path.join(os.path.dirname(__file__), "..", "static"),
        template_folder="templates",
    )

    app_settings = os.getenv(
        'APP_SETTINGS',
        'app.config.DevelopmentConfig'
    )
    app.config.from_object(app_settings)
    app.config.from_pyfile("../local.cfg", silent=True)
    if config:
        app.config.from_pyfile(config)

    if blueprints is None:
        blueprints = BLUEPRINTS

    blueprints_fabrics(app, blueprints)
    extensions_fabrics(app)
    commands_fabrics(app, COMMANDS)

    return app


def blueprints_fabrics(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def extensions_fabrics(app):
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)


def commands_fabrics(app, commands):
    for command in commands:
        app.cli.add_command(command)
