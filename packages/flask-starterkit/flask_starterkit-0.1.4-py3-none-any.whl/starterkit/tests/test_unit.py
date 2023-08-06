# -*- coding: utf-8 -*-

from starterkit.unit import application


def _start_response(*args, **kwargs):
    pass


def test_application():
    assert application(
        {"SERVER_NAME": "localhost", "SERVER_PORT": "42", "REQUEST_METHOD": "GET"}, _start_response
    )
