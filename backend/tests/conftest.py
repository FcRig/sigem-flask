import os
import sys
import pathlib
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import config
from app import create_app
from app.extensions import db

@pytest.fixture
def app():
    config.Config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    config.Config.JWT_SECRET_KEY = "test-secret-key"
    app = create_app()
    app.config.update(
        TESTING=True,
    )
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
