# -*- coding: utf-8 -*-
# @Time : 2018/4/9 19:03
# @Author : csk
# @FileName: manage.py
# @log:
import os
from app import create_app, db, mongo
from app.models import User, Role, Movie, Wish
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Movie= Movie,
                mongo=mongo, Wish=Wish)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()