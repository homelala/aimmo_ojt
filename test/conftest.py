import pytest


@pytest.fixture(scope="session")
def app():
    from app import create_app

    app = create_app()
    return app


@pytest.fixture(scope="function")
def db(app):
    import mongoengine

    mongoengine.connect(host="mongodb://localhost:27017/aimmo_ojt_test")
    yield
    mongoengine.disconnect()
