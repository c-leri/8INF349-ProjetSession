import os
import tempfile

import pytest

from api8inf349 import create_app
from api8inf349.models import init_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({"TESTING": True, "DATABASE": db_path})
    init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()
