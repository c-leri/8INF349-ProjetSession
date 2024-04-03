import os

from peewee import PostgresqlDatabase
from redis import Redis
from rq import Queue


class DatabaseSingleton(object):
    _instance: PostgresqlDatabase = None

    @classmethod
    def get_db(cls) -> PostgresqlDatabase:
        if not cls._instance:
            cls._instance = PostgresqlDatabase(
                os.environ["DB_NAME"],
                host=os.environ["DB_HOST"],
                port=os.environ["DB_PORT"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
            )
            cls._instance.connect()
        return cls._instance

    @classmethod
    def close_db(cls):
        cls.get_db().close()


class CacheSingleton(object):
    _instance: Redis = None

    @classmethod
    def get_cache(cls) -> Redis:
        if not cls._instance:
            cls._instance = Redis.from_url(url=os.environ["REDIS_URL"])
        return cls._instance


class QueueSingleton(object):
    _instance: Queue = None

    @classmethod
    def get_queue(cls) -> Queue:
        if not cls._instance:
            cls._instance = Queue("api8inf349", connection=CacheSingleton.get_cache())
        return cls._instance
