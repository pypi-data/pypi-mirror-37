# -*- coding: utf-8 -*-

from starterkit.app import create_app
from starterkit.commands import create_db, delete_db
from starterkit.db import db


def test_create_db():
    app = create_app()
    create_db(db, app)
    create_db(db, app)


def test_delete_db():
    app = create_app()
    delete_db(db, app)
    delete_db(db, app)
