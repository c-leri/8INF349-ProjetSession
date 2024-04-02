import html
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from flask import json

from api8inf349.models import (
    Product,
    Order,
    OrderProduct,
    OrderShippingInformation,
    OrderCreditCard,
    OrderTransaction,
)


class APIError(Exception):
    code: int
    content: dict


class ProductError(APIError):
    content = {"errors": {"product": {"code": "", "name": ""}}}

    def missing_fields():
        error = ProductError()

        error.code = 422
        error.content["errors"]["product"]["code"] = "missing-fields"
        error.content["errors"]["product"][
            "name"
        ] = "La création d'une commande nécessite un produit"

        return error

    def out_of_inventory():
        error = ProductError()

        error.code = 422
        error.content["errors"]["product"]["code"] = "out-of-inventory"
        error.content["errors"]["product"][
            "name"
        ] = "Le produit demandé n'est pas en inventaire"

        return error

    def not_found(id):
        error = ProductError()

        error.code = 404
        error.content["errors"]["product"]["code"] = "not-found"
        error.content["errors"]["product"][
            "name"
        ] = f"Aucun produit trouvé pour l'id {id}"

        return error


class OrderError(APIError):
    content = {"errors": {"order": {"code": "", "name": ""}}}

    def missing_fields(
        message="Il manque un ou plusieurs champs qui sont obligatoires",
    ):
        error = OrderError()

        error.code = 422
        error.content["errors"]["order"]["code"] = "missing-fields"
        error.content["errors"]["order"]["name"] = message

        return error

    def already_paid():
        error = OrderError()

        error.code = 422
        error.content["errors"]["order"]["code"] = "already-paid"
        error.content["errors"]["order"]["code"] = "La commande a déjà été payée"

        return error


def send_request(route, method="GET", data=None):
    request = Request(f"http://dimprojetu.uqac.ca/~jgnault/shops{route}")
    request.method = method
    request.add_header("content-type", "application/json")

    if data:
        request.data = json.dumps(data).encode("utf-8")

    try:
        with urlopen(request) as response:
            if response.headers["content-type"] == "application/json":
                return json.loads(response.read().decode("utf-8", errors="replace"))
            else:
                return None
    except HTTPError as e:
        error = APIError()
        error.code = e.code
        if e.headers["content-type"] == "application/json":
            error.content = json.loads(
                html.unescape(e.read().decode("utf-8", errors="replace"))
            )

        raise error


class ProductServices(object):
    @classmethod
    def load_products(cls):
        products = [
            {
                k: v.replace("\x00", "\uFFFD") if isinstance(v, str) else v
                for k, v in p.items()
            }
            for p in send_request("/products/")["products"]
        ]

        Product.insert_many(
            products,
            fields=[
                Product.id,
                Product.name,
                Product.description,
                Product.price,
                Product.weight,
                Product.in_stock,
                Product.image,
            ],
        ).on_conflict(
            conflict_target=[Product.id],
            preserve=[
                Product.name,
                Product.description,
                Product.price,
                Product.weight,
                Product.in_stock,
                Product.image,
            ],
        ).execute()
        print("Loaded products.")


class OrderService(object):
    @classmethod
    def create_order_from_post_data(cls, post_data):
        if "product" not in post_data or not post_data["product"]:
            raise ProductError.missing_fields()

        product_data = post_data["product"]

        if (
            "id" not in product_data
            or not product_data["id"]
            or "quantity" not in product_data
            or not product_data["quantity"]
        ):
            raise ProductError.missing_fields()

        id = product_data["id"]
        quantity = product_data["quantity"]

        product = Product.get_or_none(Product.id == id)

        if not product:
            raise ProductError.not_found(id)

        if not product.in_stock:
            raise ProductError.out_of_inventory()

        return Order.create_from_order_product(
            OrderProduct.create(product=product, quantity=quantity)
        )

    @classmethod
    def update_order_from_post_data(cls, order, post_data):
        if order.paid:
            raise OrderError.already_paid()

        if not order.email:
            if "credit_card" in post_data:
                raise OrderError.missing_fields(
                    "Les informations du client sont nécessaure avant d'appliquer une carte de crédit"
                )

            if "order" not in post_data or not post_data["order"]:
                raise OrderError.missing_fields()

            return cls._set_order_client_information(order, post_data["order"])

        return cls._set_order_credit_card(order, post_data)

    @classmethod
    def _set_order_client_information(cls, order, order_data):
        if (
            "email" not in order_data
            or not order_data["email"]
            or "shipping_information" not in order_data
            or not order_data["shipping_information"]
        ):
            raise OrderError.missing_fields()

        shipping_information_data = order_data["shipping_information"]

        if (
            "country" not in shipping_information_data
            or not shipping_information_data["country"]
            or "address" not in shipping_information_data
            or not shipping_information_data["address"]
            or "postal_code" not in shipping_information_data
            or not shipping_information_data["postal_code"]
            or "city" not in shipping_information_data
            or not shipping_information_data["city"]
            or "province" not in shipping_information_data
            or not shipping_information_data["province"]
        ):
            raise OrderError.missing_fields()

        order.email = order_data["email"]
        order.shipping_information = OrderShippingInformation.create(
            country=shipping_information_data["country"],
            address=shipping_information_data["address"],
            postal_code=shipping_information_data["postal_code"],
            city=shipping_information_data["city"],
            province=shipping_information_data["province"],
        )
        order.save()

        return order

    @classmethod
    def _set_order_credit_card(cls, order, post_data):
        if "credit_card" not in post_data or not post_data["credit_card"]:
            raise OrderError.missing_fields()

        credit_card_data = post_data["credit_card"]

        if (
            "name" not in credit_card_data
            or not credit_card_data["name"]
            or "number" not in credit_card_data
            or not credit_card_data["number"]
            or "cvv" not in credit_card_data
            or not credit_card_data["cvv"]
            or "expiration_month" not in credit_card_data
            or not credit_card_data["expiration_month"]
            or "expiration_year" not in credit_card_data
            or not credit_card_data["expiration_year"]
        ):
            raise OrderError.missing_fields()

        amount_charged = order.total_price + order.shipping_price
        transaction_data = send_request(
            "/pay/",
            "POST",
            {"credit_card": credit_card_data, "amount_charged": amount_charged},
        )["transaction"]

        order.paid = True
        order.credit_card = OrderCreditCard.create(**credit_card_data)
        order.transaction = OrderTransaction.create(
            id=transaction_data["id"],
            success=transaction_data["success"] is True
            or transaction_data["success"] == "true",
            amount_charged=transaction_data["amount_charged"],
        )
        order.save()

        return order
