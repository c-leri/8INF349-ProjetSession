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
            OrderProduct,
            OrderShippingInformation,
            OrderCreditCard,
            OrderTransaction,
            Order,
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


class OrderProduct(BaseModel):
    id = AutoField()
    product = ForeignKeyField(Product)
    quantity = IntegerField()

    def dict(self):
        return {"id": self.product.id, "quantity": self.quantity}


class OrderShippingInformation(BaseModel):
    id = AutoField()
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
    id = AutoField()
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
    id = CharField(primary_key=True)
    success = BooleanField()
    amount_charged = FloatField()

    def dict(self):
        return {
            "id": self.id,
            "success": self.success,
            "amount_charged": self.amount_charged,
        }


class Order(BaseModel):
    id = AutoField()
    email = CharField(null=True)
    total_price = FloatField()
    shipping_price = FloatField()
    paid = BooleanField(default=False)
    product = ForeignKeyField(OrderProduct)
    shipping_information = ForeignKeyField(OrderShippingInformation, null=True)
    credit_card = ForeignKeyField(OrderCreditCard, null=True)
    transaction = ForeignKeyField(OrderTransaction, null=True)

    @classmethod
    def create_from_order_product(cls, order_product: OrderProduct):
        total_weight = order_product.product.weight * order_product.quantity
        return cls.create(
            product=order_product,
            total_price=order_product.product.price * order_product.quantity,
            shipping_price=5
            if total_weight < 500
            else 10
            if total_weight < 2000
            else 25,
        )

    def dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "total_price": self.total_price,
            "shipping_price": self.shipping_price,
            "paid": self.paid,
            "product": self.product.dict(),
            "shipping_information": {}
            if not self.shipping_information
            else self.shipping_information.dict(),
            "credit_card": {} if not self.credit_card else self.credit_card.dict(),
            "transaction": {} if not self.transaction else self.transaction.dict(),
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
