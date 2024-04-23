import os

from flask import Flask, Response, abort, json, redirect, request, url_for

from api8inf349.models import init_app
from api8inf349.services import APIError, OrderService, ProductServices


def create_app(initial_config=None):
    app = Flask(__name__)

    app.config["DB_NAME"] = os.getenv("DB_NAME")
    app.config["DB_USER"] = os.getenv("DB_USER")
    app.config["DB_PASSWORD"] = os.getenv("DB_PASSWORD")
    app.config["DB_HOST"] = os.getenv("DB_HOST")
    app.config["DB_PORT"] = os.getenv("DB_PORT")
    app.config["REDIS_URL"] = os.getenv("REDIS_URL")

    if initial_config is not None:
        app.config.update(initial_config)

    init_app(app)

    @app.before_request
    def load_products():
        # Only run on first request
        app.before_request_funcs[None].remove(load_products)

        if not app.config["TESTING"]:
            ProductServices.load_products()

    @app.after_request
    def access_control(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT"
        return response

    # ==== Endpoints ====

    @app.route("/")
    def index():
        return {"products": ProductServices.get_product_dicts()}

    @app.route("/order", methods=["POST"])
    def order_create():
        try:
            order = OrderService.create_order_from_post_data(request.get_json())

            return redirect(url_for("order", order_id=order.id))
        except APIError as e:
            return abort(_api_errpr_response(e))

    @app.route("/order/<int:order_id>")
    def order(order_id):
        try:
            return {"order": OrderService.get_order_dict(order_id)}
        except APIError as e:
            return abort(_api_errpr_response(e))

    @app.route("/order/<int:order_id>", methods=["PUT"])
    def order_update(order_id):
        try:
            order = OrderService.get_order(order_id)

            order = OrderService.update_order_from_post_data(order, request.get_json())

            if order:
                return {"order": OrderService.order_to_dict(order)}
            else:
                return Response(content_type="application/json", status=202)
        except APIError as e:
            return abort(_api_errpr_response(e))

    def _api_errpr_response(error: APIError) -> Response:
        return Response(
            json.dumps(error.content),
            content_type="application/json",
            status=error.code,
        )

    return app
