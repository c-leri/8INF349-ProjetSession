from playhouse.shortcuts import model_to_dict

from api8inf349.models import (
    Product,
    OrderProduct,
    OrderShippingInformation,
    OrderCreditCard,
    OrderTransaction,
    Order,
)


class TestProduct(object):
    def test_create(self, app):
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


class TestOrderProduct(object):
    def test_create(self, app):
        product = Product.create(
            id=1,
            name="Test",
            description="Test OrderProduct create()",
            in_stock=True,
            price=23.1,
            weight=200,
            image="test.jpg",
        )

        order_product = OrderProduct.create(product=product, quantity=2)

        assert order_product.product.id == 1
        assert order_product.quantity == 2

        got_order_product = OrderProduct.get_by_id(order_product.id)

        assert got_order_product.product.id == 1
        assert got_order_product.quantity == 2

    def test_dict(self, app):
        product = Product.create(
            id=1,
            name="Test",
            description="Test OrderProduct dict()",
            in_stock=True,
            price=23.1,
            weight=200,
            image="test.jpg",
        )

        order_product = OrderProduct.create(product=product, quantity=2)

        order_product_dict = order_product.dict()

        assert order_product_dict["id"] == 1
        assert order_product_dict["quantity"] == 2


class TestOrderShippingInformation(object):
    def test_create(self, app):
        order_shipping_information = OrderShippingInformation.create(
            country="Canada",
            address="125, rue Imaginaire",
            postal_code="XXX XXX",
            city="Chicoutimi",
            province="QC",
        )

        assert order_shipping_information.country == "Canada"
        assert order_shipping_information.address == "125, rue Imaginaire"
        assert order_shipping_information.postal_code == "XXX XXX"
        assert order_shipping_information.city == "Chicoutimi"
        assert order_shipping_information.province == "QC"

        got_order_shipping_information = OrderShippingInformation.get_by_id(
            order_shipping_information.id
        )

        assert got_order_shipping_information.country == "Canada"
        assert got_order_shipping_information.address == "125, rue Imaginaire"
        assert got_order_shipping_information.postal_code == "XXX XXX"
        assert got_order_shipping_information.city == "Chicoutimi"
        assert got_order_shipping_information.province == "QC"

    def test_dict(self, app):
        order_shipping_information = OrderShippingInformation.create(
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
    def test_create(self, app):
        order_credit_card = OrderCreditCard.create(
            name="John Doe",
            number="1234 0000 0000 5678",
            cvv="156",
            expiration_year=2025,
            expiration_month=5,
        )

        assert order_credit_card.name == "John Doe"
        assert order_credit_card.number == "1234 0000 0000 5678"
        assert order_credit_card.cvv == "156"
        assert order_credit_card.expiration_year == 2025
        assert order_credit_card.expiration_month == 5

        got_order_credit_card = OrderCreditCard.get_by_id(order_credit_card.id)

        assert got_order_credit_card.name == "John Doe"
        assert got_order_credit_card.number == "1234 0000 0000 5678"
        assert got_order_credit_card.cvv == "156"
        assert got_order_credit_card.expiration_year == 2025
        assert got_order_credit_card.expiration_month == 5

    def test_dict(self, app):
        order_credit_card = OrderCreditCard.create(
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
    def test_create(self, app):
        order_transaction = OrderTransaction.create(
            id="testid", success=True, amount_charged=1048.4
        )

        assert order_transaction.id == "testid"
        assert order_transaction.success is True
        assert order_transaction.amount_charged == 1048.4

        got_order_transaction = OrderTransaction.get_by_id(order_transaction.id)

        assert got_order_transaction.id == "testid"
        assert got_order_transaction.success is True
        assert got_order_transaction.amount_charged == 1048.4

    def test_dict(self, app):
        order_transaction = OrderTransaction.create(
            id="testid", success=True, amount_charged=1048.4
        )

        order_transaction_dict = order_transaction.dict()

        assert order_transaction_dict["id"] == "testid"
        assert order_transaction_dict["success"] is True
        assert order_transaction_dict["amount_charged"] == 1048.4


class TestOrder(object):
    def test_create(self, app):
        product = Product.create(
            id=1,
            name="Test",
            description="Test Order create()",
            in_stock=True,
            price=23.1,
            weight=200,
            image="test.jpg",
        )

        order_product = OrderProduct.create(product=product, quantity=2)

        order_shipping_information = OrderShippingInformation.create(
            country="Canada",
            address="125, rue Imaginaire",
            postal_code="XXX XXX",
            city="Chicoutimi",
            province="QC",
        )

        order_credit_card = OrderCreditCard.create(
            name="John Doe",
            number="1234 0000 0000 5678",
            cvv="156",
            expiration_year=2025,
            expiration_month=5,
        )

        order_transaction = OrderTransaction.create(
            id="testid", success=True, amount_charged=1048.4
        )

        order = Order.create(
            email="test@example.com",
            total_price=1818.9,
            shipping_price=5,
            paid=True,
            product=order_product,
            shipping_information=order_shipping_information,
            credit_card=order_credit_card,
            transaction=order_transaction,
        )

        assert order.email == "test@example.com"
        assert order.total_price == 1818.9
        assert order.shipping_price == 5
        assert order.paid is True
        assert order.product.id == order_product.id
        assert order.shipping_information.id == order_shipping_information.id
        assert order.credit_card.id == order_credit_card.id
        assert order.transaction.id == order_transaction.id

        got_order = Order.get_by_id(order.id)

        assert got_order.email == "test@example.com"
        assert got_order.total_price == 1818.9
        assert got_order.shipping_price == 5
        assert got_order.paid is True
        assert got_order.product.id == order_product.id
        assert got_order.shipping_information.id == order_shipping_information.id
        assert got_order.credit_card.id == order_credit_card.id
        assert got_order.transaction.id == order_transaction.id

    def test_create_from_order_product(self, app):
        product = Product.create(
            id=1,
            name="Test",
            description="Test Order create_from_order_product()",
            in_stock=True,
            price=23.1,
            weight=200,
            image="test.jpg",
        )

        order_product = OrderProduct.create(product=product, quantity=2)

        order = Order.create_from_order_product(order_product)

        total_price = order_product.product.price * order_product.quantity
        total_weight = order_product.product.weight * order_product.quantity
        shipping_price = 5 if total_weight < 500 else 10 if total_weight < 2000 else 25

        assert order.email is None
        assert order.total_price == total_price
        assert order.shipping_price == shipping_price
        assert order.paid is False
        assert order.product.id == order_product.id
        assert order.shipping_information is None
        assert order.credit_card is None
        assert order.transaction is None

        got_order = Order.get_by_id(order.id)

        assert got_order.email is None
        assert got_order.total_price == total_price
        assert got_order.shipping_price == shipping_price
        assert got_order.paid is False
        assert got_order.product.id == order_product.id
        assert got_order.shipping_information is None
        assert got_order.credit_card is None
        assert got_order.transaction is None

    def test_dict(self, app):
        product = Product.create(
            id=1,
            name="Test",
            description="Test Order dict()",
            in_stock=True,
            price=23.1,
            weight=200,
            image="test.jpg",
        )

        order_product = OrderProduct.create(product=product, quantity=2)

        order_shipping_information = OrderShippingInformation.create(
            country="Canada",
            address="125, rue Imaginaire",
            postal_code="XXX XXX",
            city="Chicoutimi",
            province="QC",
        )

        order_credit_card = OrderCreditCard.create(
            name="John Doe",
            number="1234 0000 0000 5678",
            cvv="156",
            expiration_year=2025,
            expiration_month=5,
        )

        order_transaction = OrderTransaction.create(
            id="testid", success=True, amount_charged=1048.4
        )

        order = Order.create(
            email="test@example.com",
            total_price=1818.9,
            shipping_price=5,
            paid=True,
            product=order_product,
            shipping_information=order_shipping_information,
            credit_card=order_credit_card,
            transaction=order_transaction,
        )

        order_dict = order.dict()

        assert order_dict["id"] == order.id
        assert order_dict["email"] == "test@example.com"
        assert order_dict["total_price"] == 1818.9
        assert order_dict["shipping_price"] == 5
        assert order_dict["paid"] is True

        order_product_dict = order_dict["product"]

        assert order_product_dict["id"] == 1
        assert order_product_dict["quantity"] == 2

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
    def test_empty_index(self, app, client):
        response = client.get("/")

        assert response.status_code == 200
        assert response.json == {"products": []}

    def test_index(self, app, client):
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
