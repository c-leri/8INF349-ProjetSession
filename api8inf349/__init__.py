import os

from flask import Flask, Response, request, redirect, url_for, abort, json

from api8inf349.models import init_app, Product, Order
from api8inf349.services import ProductServices, OrderService, APIError


def create_app(initial_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if initial_config is not None:
        app.config.update(initial_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_app(app)

    @app.before_request
    def load_products():
        # Only run on first request
        app.before_request_funcs[None].remove(load_products)

        if not app.config["TESTING"]:
            ProductServices.load_products()

    @app.route("/")
    def index():
        return {"products": [product for product in Product.select().dicts()]}

    @app.route("/order", methods=["POST"])
    def order_create():
        try:
            order = OrderService.create_order_from_post_data(request.get_json())

            return redirect(url_for("order", order_id=order.id))
        except APIError as e:
            return abort(
                Response(
                    json.dumps(e.content),
                    content_type="application/json",
                    status=e.code,
                )
            )

    @app.route("/order/<int:order_id>")
    def order(order_id):
        order = Order.get_or_none(Order.id == order_id)

        if not order:
            return abort(404)

        return {"order": order.dict()}

    @app.route("/order/<int:order_id>", methods=["PUT"])
    def order_update(order_id):
        order = Order.get_or_none(Order.id == order_id)

        if not order:
            return abort(404)

        try:
            order = OrderService.update_order_from_post_data(order, request.get_json())
            return {"order": order.dict()}
        except APIError as e:
            return abort(
                Response(
                    json.dumps(e.content),
                    content_type="application/json",
                    status=e.code,
                )
            )

    return app
