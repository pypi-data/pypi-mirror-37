# -*- coding: utf-8 -*-

import os

from functools import wraps

from starterkit.app import create_app
from starterkit.commands import create_db, delete_db
from starterkit.db import db


def check_is_equal(n1, n2):
    assert n1 == n2, "{} (received) is not equal to {} (expected)".format(n1, n2)


def _create_app():
    check_is_equal(os.environ["STARTERKIT_ENVIRONMENT"], "testing")
    app = create_app()
    delete_db(db, app)
    create_db(db, app)
    return app


def with_tst_request_context(fn):
    @wraps(fn)
    def test_with_tst_request_context_wrapper(*args, **kwargs):
        test_app = _create_app()
        with test_app.test_request_context():
            kwargs["test_app"] = test_app
            rc = fn(*args, **kwargs)
        return rc

    return test_with_tst_request_context_wrapper


def _post(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        headers = kwargs.setdefault("headers", {})
        headers["X-Real-IP"] = "127.0.0.1"
        return fn(*args, **kwargs)

    return wrapper


def with_tst_client(fn):
    @wraps(fn)
    def test_with_test_client_wrapper(*args, test_app=None, **kwargs):
        with test_app.test_client() as test_client:
            test_client.post = _post(test_client.post)
            kwargs["test_client"] = test_client
            rc = fn(*args, **kwargs)
        return rc

    return test_with_test_client_wrapper
