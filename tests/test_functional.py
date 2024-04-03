from playhouse.shortcuts import model_to_dict

from api8inf349.models import (
    Order,
    OrderCreditCard,
    OrderProduct,
    OrderShippingInformation,
    OrderTransaction,
    Product,
)
from api8inf349.services import OrderService


class TestProduct(object):
    def test_create(self, app, db_transaction):
        product = Product.create(
            id=1,
            name="Test",
            description="Test Product create()",
            in_stock=True,
            price=23.1,
            weight=200,
            image="test.jpg",
        )

        assert product.id == 1
        assert product.name == "Test"
        assert product.description == "Test Product create()"
        assert product.in_stock is True
        assert product.price == 23.1
        assert product.weight == 200
        assert product.image == "test.jpg"

        got_product = Product.get_by_id(product.id)

        assert got_product.id == 1
        assert got_product.name == "Test"
        assert got_product.description == "Test Product create()"
        assert got_product.in_stock is True
        assert got_product.price == 23.1
        assert got_product.weight == 200
        assert got_product.image == "test.jpg"


class TestOrder(object):
    def test_create(self, app, db_transaction):
        order = Order.create(
            email="test@example.com",
            total_price=1818.9,
            shipping_price=5,
            paid=True,
        )

        assert order.email == "test@example.com"
        assert order.total_price == 1818.9
        assert order.shipping_price == 5
        assert order.paid is True

        got_order = Order.get_by_id(order.id)

        assert got_order.email == "test@example.com"
        assert got_order.total_price == 1818.9
        assert got_order.shipping_price == 5
        assert got_order.paid is True

    def test_dict(self, app, db_transaction):
        order = Order.create(
            email="test@example.com",
            total_price=1818.9,
            shipping_price=5,
            paid=True,
        )

        order_dict = order.dict()

        assert order_dict["email"] == "test@example.com"
        assert order_dict["total_price"] == 1818.9
        assert order_dict["shipping_price"] == 5
        assert order_dict["paid"] is True


class TestOrderProduct(object):
    def test_create(self, app, db_transaction):
        order = Order.create(
            email="test@example.com",
            total_price=1818.9,
            shipping_price=5,
            paid=True,
        )

        product = Product.create(
            id=1,
            name="Test",
            description="Test OrderProduct create()",
            in_stock=True,
            price=23.1,
            weight=200,
            image="test.jpg",
        )

        order_product = OrderProduct.create(
            order_id=order.id, product_id=product.id, quantity=2
        )

        assert order_product.order_id == order.id
        assert order_product.product_id == 1
        assert order_product.quantity == 2

        got_order_product = OrderProduct.get(
            OrderProduct.order_id == order.id, OrderProduct.product_id == product.id
        )

        assert got_order_product.order_id == order.id
        assert got_order_product.product_id == 1
        assert got_order_product.quantity == 2

    def test_dict(self, app, db_transaction):
        order = Order.create(
            email="test@example.com",
            total_price=1818.9,
            shipping_price=5,
            paid=True,
        )

        product = Product.create(
            id=1,
            name="Test",
            description="Test OrderProduct dict()",
            in_stock=True,
            price=23.1,
            weight=200,
            image="test.jpg",
        )

        order_product = OrderProduct.create(
            order_id=order.id, product_id=product.id, quantity=2
        )

        order_product_dict = order_product.dict()

        assert order_product_dict["id"] == 1
        assert order_product_dict["quantity"] == 2


class TestOrderShippingInformation(object):
    def test_create(self, app, db_transaction):
        order = Order.create(
            email="test@example.com",
            total_price=1818.9,
            shipping_price=5,
            paid=True,
        )

        order_shipping_information = OrderShippingInformation.create(
            order_id=order.id,
            country="Canada",
            address="125, rue Imaginaire",
            postal_code="XXX XXX",
            city="Chicoutimi",
            province="QC",
        )

        assert order_shipping_information.order_id == order.id
        assert order_shipping_information.country == "Canada"
        assert order_shipping_information.address == "125, rue Imaginaire"
        assert order_shipping_information.postal_code == "XXX XXX"
        assert order_shipping_information.city == "Chicoutimi"
        assert order_shipping_information.province == "QC"

        got_order_shipping_information = OrderShippingInformation.get_by_id(
            order_shipping_information.order_id
        )

        assert got_order_shipping_information.order_id == order.id
        assert got_order_shipping_information.country == "Canada"
        assert got_order_shipping_information.address == "125, rue Imaginaire"
        assert got_order_shipping_information.postal_code == "XXX XXX"
        assert got_order_shipping_information.city == "Chicoutimi"
        assert got_order_shipping_information.province == "QC"

    def test_dict(self, app, db_transaction):
        order = Order.create(
            email="test@example.com",
            total_price=1818.9,
            shipping_price=5,
            paid=True,
        )

        order_shipping_information = OrderShippingInformation.create(
            order_id=order.id,
            country="Canada",
            address="125, rue Imaginaire",
            postal_code="XXX XXX",
            city="Chicoutimi",
            province="QC",
        )

        order_shipping_information_dict = order_shipping_information.dict()

        assert order_shipping_information_dict["country"] == "Canada"
        assert order_shipping_information_dict["address"] == "125, rue Imaginaire"
        assert order_shipping_information_dict["postal_code"] == "XXX XXX"
        assert order_shipping_information_dict["city"] == "Chicoutimi"
        assert order_shipping_information_dict["province"] == "QC"


class TestOrderCreditCard(object):
    def test_create(self, app, db_transaction):
        order = Order.create(
            email="test@example.com",
            total_price=1818.9,
            shipping_price=5,
            paid=True,
        )

        order_credit_card = OrderCreditCard.create(
            order_id=order.id,
            name="John Doe",
            number="1234 0000 0000 5678",
            cvv="156",
            expiration_year=2025,
            expiration_month=5,
        )

        assert order_credit_card.order_id == order.id
        assert order_credit_card.name == "John Doe"
        assert order_credit_card.number == "1234 0000 0000 5678"
        assert order_credit_card.cvv == "156"
        assert order_credit_card.expiration_year == 2025
        assert order_credit_card.expiration_month == 5

        got_order_credit_card = OrderCreditCard.get_by_id(order_credit_card.order_id)

        assert got_order_credit_card.order_id == order.id
        assert got_order_credit_card.name == "John Doe"
        assert got_order_credit_card.number == "1234 0000 0000 5678"
        assert got_order_credit_card.cvv == "156"
        assert got_order_credit_card.expiration_year == 2025
        assert got_order_credit_card.expiration_month == 5

    def test_dict(self, app, db_transaction):
        order = Order.create(
            email="test@example.com",
            total_price=1818.9,
            shipping_price=5,
            paid=True,
        )

        order_credit_card = OrderCreditCard.create(
            order_id=order.id,
            name="John Doe",
            number="1234 0000 0000 5678",
            cvv="156",
            expiration_year=2025,
            expiration_month=5,
        )

        order_credit_card_dict = order_credit_card.dict()

        assert order_credit_card_dict["name"] == "John Doe"
        assert order_credit_card_dict["first_digits"] == "1234"
        assert order_credit_card_dict["last_digits"] == "5678"
        assert order_credit_card_dict["expiration_year"] == 2025
        assert order_credit_card_dict["expiration_month"] == 5


class TestOrderTransaction(object):
    def test_create(self, app, db_transaction):
        order = Order.create(
            email="test@example.com",
            total_price=1818.9,
            shipping_price=5,
            paid=True,
        )

        order_transaction = OrderTransaction.create(
            order_id=order.id, id="testid", success=True, amount_charged=1048.4
        )

        assert order_transaction.order_id == order.id
        assert order_transaction.id == "testid"
        assert order_transaction.success is True
        assert order_transaction.amount_charged == 1048.4

        got_order_transaction = OrderTransaction.get_by_id(order_transaction.order_id)

        assert got_order_transaction.order_id == order.id
        assert got_order_transaction.id == "testid"
        assert got_order_transaction.success is True
        assert got_order_transaction.amount_charged == 1048.4

    def test_dict(self, app, db_transaction):
        order = Order.create(
            email="test@example.com",
            total_price=1818.9,
            shipping_price=5,
            paid=True,
        )

        order_transaction = OrderTransaction.create(
            order_id=order.id, id="testid", success=True, amount_charged=1048.4
        )

        order_transaction_dict = order_transaction.dict()

        assert order_transaction_dict["id"] == "testid"
        assert order_transaction_dict["success"] is True
        assert order_transaction_dict["amount_charged"] == 1048.4


class TestOrderService(object):
    def test_order_to_dict(self, app, db_transaction):
        product = Product.create(
            id=1,
            name="Test",
            description="Test OrderService order_to_dict()",
            in_stock=True,
            price=23.1,
            weight=200,
            image="test.jpg",
        )

        order = Order.create(
            email="test@example.com",
            total_price=1818.9,
            shipping_price=5,
            paid=True,
        )

        OrderProduct.insert(
            {"order_id": order.id, "product_id": product.id, "quantity": 2},
        ).execute()

        OrderShippingInformation.insert(
            {
                "order_id": order.id,
                "country": "Canada",
                "address": "125, rue Imaginaire",
                "postal_code": "XXX XXX",
                "city": "Chicoutimi",
                "province": "QC",
            },
        ).execute()

        OrderCreditCard.insert(
            {
                "order_id": order.id,
                "name": "John Doe",
                "number": "1234 0000 0000 5678",
                "cvv": "156",
                "expiration_year": 2025,
                "expiration_month": 5,
            },
        ).execute()

        OrderTransaction.insert(
            {
                "order_id": order.id,
                "id": "testid",
                "success": True,
                "amount_charged": 1048.4,
            },
        ).execute()

        order_dict = OrderService.order_to_dict(order)

        assert order_dict["id"] == order.id
        assert order_dict["email"] == "test@example.com"
        assert order_dict["total_price"] == 1818.9
        assert order_dict["shipping_price"] == 5
        assert order_dict["paid"] is True

        order_products_dict = order_dict["products"]

        assert order_products_dict[0]["id"] == 1
        assert order_products_dict[0]["quantity"] == 2

        order_shipping_information_dict = order_dict["shipping_information"]

        assert order_shipping_information_dict["country"] == "Canada"
        assert order_shipping_information_dict["address"] == "125, rue Imaginaire"
        assert order_shipping_information_dict["postal_code"] == "XXX XXX"
        assert order_shipping_information_dict["city"] == "Chicoutimi"
        assert order_shipping_information_dict["province"] == "QC"

        order_credit_card_dict = order_dict["credit_card"]

        assert order_credit_card_dict["name"] == "John Doe"
        assert order_credit_card_dict["first_digits"] == "1234"
        assert order_credit_card_dict["last_digits"] == "5678"
        assert order_credit_card_dict["expiration_year"] == 2025
        assert order_credit_card_dict["expiration_month"] == 5

        order_transaction_dict = order_dict["transaction"]

        assert order_transaction_dict["id"] == "testid"
        assert order_transaction_dict["success"] is True
        assert order_transaction_dict["amount_charged"] == 1048.4


class TestRoutes(object):
    def test_empty_index(self, app, client, db_transaction):
        response = client.get("/")

        assert response.status_code == 200
        assert response.json == {"products": []}

    def test_index(self, app, client, db_transaction):
        product = Product.create(
            id=1,
            name="Test",
            description="Test routes index",
            in_stock=True,
            price=23.1,
            weight=200,
            image="test.jpg",
        )

        response = client.get("/")

        assert response.status_code == 200
        assert response.json == {"products": [model_to_dict(product)]}
