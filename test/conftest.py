import pytest

from flask import current_app, g
from unittest import mock

from pprint import pprint


@pytest.fixture(scope="session")
def app():
    from app import create_app

    app = create_app()
    return app


@pytest.fixture(scope="session", autouse=True)
def app_context(app):
    ctx = app.app_context()
    ctx.push()
    yield
    ctx.pop()


def create_mock_session():
    return mock.Mock()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="function", autouse=True)
def db(app):
    import mongoengine

    mongoengine.connect(host=current_app.config["MONGO_URI"])
    yield
    mongoengine.disconnect()


#
# @pytest.fixture(scope="function")
# def session(db):
#     session = db["session"]()
#     g.db = session
#     yield session
#     session.rollback()
#     session.close()
