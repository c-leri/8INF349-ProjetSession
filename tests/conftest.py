import os
import tempfile

import pytest

from inf349 import create_app
from inf349.models import init_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({"ENV": "TEST", "DATABASE": db_path})
    init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()
