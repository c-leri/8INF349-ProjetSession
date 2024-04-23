from multiprocessing import Process

import pytest
from rq import Worker
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from api8inf349 import create_app
from api8inf349.models import Order, Product, get_cache, get_db, get_queue, init_db

postgres_container = PostgresContainer("postgres:12")
redis_container = RedisContainer("redis:5")


@pytest.fixture(scope="module")
def app(request):
    # Start the postgres container
    postgres_container.start()

    # Remove the postgres container after the end of the test file
    request.addfinalizer(postgres_container.stop)

    # Create the app with the postgres connection informations
    app = create_app(
        {
            "TESTING": True,
            "DB_NAME": postgres_container.env["POSTGRES_DB"],
            "DB_HOST": postgres_container.get_container_host_ip(),
            "DB_PORT": postgres_container.get_exposed_port(5432),
            "DB_USER": postgres_container.env["POSTGRES_USER"],
            "DB_PASSWORD": postgres_container.env["POSTGRES_PASSWORD"],
        }
    )

    # Wait for postgres to be ready then init the db
    wait_for_logs(postgres_container, "database system is ready to accept connections")
    with app.app_context():
        init_db()

    return app


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


@pytest.fixture
def with_db_transaction(request, app):
    with get_db().atomic() as transaction:
        Order.delete().execute()
        Product.delete().execute()
        request.addfinalizer(transaction.rollback)


@pytest.fixture(scope="module")
def with_cache(request, app):
    # Start the redis container
    redis_container.start()

    # Remove the redis container at the end of the test file
    request.addfinalizer(redis_container.stop)

    # Add the connection informations for redis to the app
    app.config["REDIS_URL"] = "redis://{}:{}".format(
        redis_container.get_container_host_ip(),
        redis_container.get_exposed_port(6379),
    )

    # Wait for redis to be ready
    wait_for_logs(redis_container, "Ready to accept connections")


@pytest.fixture
def with_worker(with_cache):
    # Start the worker in the background
    worker = Worker([get_queue()], connection=get_cache())
    Process(target=worker.work, daemon=True).start()
