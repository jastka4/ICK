import click
from flask.cli import with_appcontext

from .extensions import db


@click.command('create')
@with_appcontext
def create_db():
    """Creates the db tables."""
    db.create_all()


@click.command('drop')
@with_appcontext
def drop_db():
    """Drops the db tables."""
    db.drop_all()
