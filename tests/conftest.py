import pytest

from api8inf349 import create_app
from api8inf349.models import Order, Product, init_db
from api8inf349.singleton import DatabaseSingleton


@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    init_db()

    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture()
def db_transaction():
    with DatabaseSingleton.get_db().atomic() as transaction:
        Order.delete().execute()
        Product.delete().execute()
        yield
        transaction.rollback()
