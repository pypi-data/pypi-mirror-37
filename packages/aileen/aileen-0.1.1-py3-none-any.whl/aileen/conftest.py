import pytest

from aileen.app import create as create_app


"""
Useful things for all tests.

One application is made per test session, but cleanup and recreation currently happens per test.
This can be sped up if needed by moving some functions to "module" or even "session" scope,
but then the tests need to share data and and data modifications can lead to tricky debugging.
"""


@pytest.fixture(scope="session")
def app():
    print("APP FIXTURE")
    test_app = create_app(env="testing")

    # Establish an application context before running the tests.
    ctx = test_app.app_context()
    ctx.push()

    yield test_app

    ctx.pop()

    print("DONE WITH APP FIXTURE")


@pytest.fixture(scope="function")
def db(app):
    """
    Provide a db object with the structure freshly created. This assumes a clean database.
    It does clean up after itself when it's done (drops everything).
    """
    print("DB FIXTURE")
    # app is an instance of a flask app, _db a SQLAlchemy DB
    from aileen.data.config import db as _db

    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    print("DB FIXTURE CLEANUP")
    # Explicitly close DB connection
    _db.session.close()

    _db.drop_all()
