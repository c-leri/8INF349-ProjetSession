import click
from flask.cli import with_appcontext
from peewee import (
    AutoField,
    BooleanField,
    CharField,
    CompositeKey,
    FloatField,
    ForeignKeyField,
    IntegerField,
    Model,
)
from rq import Worker

from api8inf349.singleton import DatabaseSingleton, QueueSingleton, CacheSingleton


def init_db():
    DatabaseSingleton.get_db().create_tables(
        [
            Product,
            Order,
            OrderProduct,
            OrderShippingInformation,
            OrderCreditCard,
            OrderTransactionError,
            OrderTransaction,
        ]
    )


class BaseModel(Model):
    class Meta:
        database = DatabaseSingleton.get_db()


class Product(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    description = CharField()
    price = FloatField()
    weight = IntegerField()
    in_stock = BooleanField()
    image = CharField()


class Order(BaseModel):
    id = AutoField()
    email = CharField(null=True)
    total_price = FloatField()
    shipping_price = FloatField()
    paid = BooleanField(default=False)

    def dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "total_price": self.total_price,
            "shipping_price": self.shipping_price,
            "paid": self.paid,
        }


class OrderProduct(BaseModel):
    order_id = ForeignKeyField(Order, on_delete="cascade", lazy_load=False)
    product_id = ForeignKeyField(Product, lazy_load=False)
    quantity = IntegerField()

    def dict(self):
        return {"id": self.product_id, "quantity": self.quantity}

    class Meta:
        primary_key = CompositeKey("order_id", "product_id")


class OrderShippingInformation(BaseModel):
    order_id = ForeignKeyField(
        Order, on_delete="CASCADE", lazy_load=False, primary_key=True
    )
    country = CharField()
    address = CharField()
    postal_code = CharField()
    city = CharField()
    province = CharField()

    def dict(self):
        return {
            "country": self.country,
            "address": self.address,
            "postal_code": self.postal_code,
            "city": self.city,
            "province": self.province,
        }


class OrderCreditCard(BaseModel):
    order_id = ForeignKeyField(
        Order, on_delete="CASCADE", lazy_load=False, primary_key=True
    )
    name = CharField()
    number = CharField()
    cvv = CharField()
    expiration_year = IntegerField()
    expiration_month = IntegerField()

    def dict(self):
        return {
            "name": self.name,
            "first_digits": self.number[0:4],
            "last_digits": self.number[-4:],
            "expiration_year": self.expiration_year,
            "expiration_month": self.expiration_month,
        }


class OrderTransactionError(BaseModel):
    code = CharField()
    name = CharField()

    def dict(self):
        return {"code": self.code, "name": self.name}

    class Meta:
        primarykey = CompositeKey("code", "name")


class OrderTransaction(BaseModel):
    order_id = ForeignKeyField(
        Order, on_delete="CASCADE", lazy_load=False, primary_key=True
    )
    success = BooleanField()
    amount_charged = FloatField()
    id = CharField(null=True)
    error = ForeignKeyField(OrderTransactionError, null=True)

    def dict(self):
        dict = {
            "success": self.success,
            "amount_charged": self.amount_charged,
        }

        if self.id:
            dict["id"] = self.id
        else:
            if self.error:
                dict["error"] = self.error.dict()

        return dict


def close_db(_):
    DatabaseSingleton.close_db()


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


@click.command("worker")
@with_appcontext
def worker_command():
    worker = Worker([QueueSingleton.get_queue()], connection=CacheSingleton.get_cache())
    worker.work()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(worker_command)
