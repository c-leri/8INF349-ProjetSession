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
    def order_to_dict(cls, order: Order) -> dict:
        products = (
            OrderProduct.select()
            .where(OrderProduct.order == order)
            .order_by(OrderProduct.product)
        )

        shipping_information = OrderShippingInformation.get_or_none(
            OrderShippingInformation.order == order
        )

        credit_card = OrderCreditCard.get_or_none(OrderCreditCard.order == order)

        transaction = OrderTransaction.get_or_none(OrderTransaction.order == order)

        order_dict = order.dict()

        order_dict["products"] = [product.dict() for product in products]

        order_dict["shipping_information"] = (
            {} if not shipping_information else shipping_information.dict()
        )

        order_dict["credit_card"] = {} if not credit_card else credit_card.dict()

        order_dict["transaction"] = {} if not transaction else transaction.dict()

        return order_dict

    @classmethod
    def create_order_from_post_data(cls, post_data: dict) -> Order:
        if "products" not in post_data:
            if "product" not in post_data or not post_data["product"]:
                raise ProductError.missing_fields()
            products_data = [post_data["product"]]
        else:
            if not post_data["products"] or not post_data["products"][0]:
                raise ProductError.missing_fields()
            products_data = post_data["products"]

        products = []
        for product_data in products_data:
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

            products.append({"product": product, "quantity": quantity})

        products_weight = map(
            lambda product: product["product"].weight * product["quantity"], products
        )
        total_weight = sum(products_weight)

        products_price = map(
            lambda product: product["product"].price * product["quantity"], products
        )
        total_price = sum(products_price)

        order = Order.create(
            total_price=total_price,
            shipping_price=5
            if total_weight < 500
            else 10
            if total_weight < 2000
            else 25,
        )

        OrderProduct.insert_many(
            map(
                lambda product: {
                    "order": order,
                    "product": product["product"],
                    "quantity": product["quantity"],
                },
                products,
            )
        ).execute()

        return order

    @classmethod
    def update_order_from_post_data(cls, order: Order, post_data: dict) -> Order:
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
    def _set_order_client_information(cls, order: Order, order_data: dict) -> Order:
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
        order.save()

        OrderShippingInformation.insert(
            {"order": order, **shipping_information_data}
        ).execute()

        return order

    @classmethod
    def _set_order_credit_card(cls, order: Order, post_data: dict) -> Order:
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
        order.save()

        OrderCreditCard.insert({"order": order, **credit_card_data}).execute()
        OrderTransaction.insert(
            {
                "order": order,
                "id": transaction_data["id"],
                "success": transaction_data["success"] is True
                or transaction_data["success"] == "true",
                "amount_charged": transaction_data["amount_charged"],
            }
        ).execute()

        return order
