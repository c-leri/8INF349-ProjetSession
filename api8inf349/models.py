import os
import click
from flask import current_app
from flask.cli import with_appcontext
from peewee import (
    Model,
    SqliteDatabase,
    PostgresqlDatabase,
    Proxy,
    CharField,
    IntegerField,
    FloatField,
    BooleanField,
    AutoField,
    ForeignKeyField,
    CompositeKey,
)

db_proxy = Proxy()


def connect_db():
    if current_app.config["TESTING"]:
        db_proxy.initialize(
            SqliteDatabase(current_app.config["DATABASE"], pragmas={"foreign_keys": 1})
        )
    else:
        db_proxy.initialize(
            PostgresqlDatabase(
                os.environ["DB_NAME"],
                host=os.environ["DB_HOST"],
                port=os.environ["DB_PORT"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
            )
        )
        db_proxy.connect()


def init_db():
    db_proxy.create_tables(
        [
            Product,
            Order,
            OrderProduct,
            OrderShippingInformation,
            OrderCreditCard,
            OrderTransaction,
        ]
    )


def close_db_proxy(_):
    db_proxy.close()


class BaseModel(Model):
    class Meta:
        database = db_proxy


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
    order = ForeignKeyField(Order, on_delete="cascade")
    product = ForeignKeyField(Product)
    quantity = IntegerField()

    def dict(self):
        return {"id": self.product.id, "quantity": self.quantity}

    class Meta:
        primary_key = CompositeKey("order", "product")


class OrderShippingInformation(BaseModel):
    order = ForeignKeyField(Order, on_delete="CASCADE", primary_key=True)
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
    order = ForeignKeyField(Order, on_delete="CASCADE", primary_key=True)
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


class OrderTransaction(BaseModel):
    order = ForeignKeyField(Order, on_delete="CASCADE", primary_key=True)
    id = CharField()
    success = BooleanField()
    amount_charged = FloatField()

    def dict(self):
        return {
            "id": self.id,
            "success": self.success,
            "amount_charged": self.amount_charged,
        }


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    with app.app_context():
        connect_db()
    app.teardown_appcontext(close_db_proxy)
    app.cli.add_command(init_db_command)
