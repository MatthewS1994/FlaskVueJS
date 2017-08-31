import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from management.commands import *
from app import app, db

from server.models import UsersProfileData


app.config.from_object(os.environ.get('APP_SETTINGS', 'config.DevelopmentConfig'))

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
