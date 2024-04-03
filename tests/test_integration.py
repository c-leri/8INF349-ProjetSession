from time import sleep
from random import randint

from api8inf349.models import Order, Product
from api8inf349.singleton import QueueSingleton


class TestOrder(object):
    def test_create_order(self, app, client):
        product_id = randint(1000, 100000)
        Product.create(
            id=product_id,
            name="Test",
            description="Test routes index",
            in_stock=True,
            price=23.1,
            weight=200,
            image="test.jpg",
        )

        response = client.post(
            "/order",
            json={"product": {"id": product_id, "quantity": 2}},
        )
        assert response.status_code == 302

        order_id = int(response.location[7:])

        response = client.get(f"/order/{order_id}")
        assert response.status_code == 200
        assert response.json == {
            "order": {
                "id": order_id,
                "email": None,
                "total_price": 46.2,
                "shipping_price": 5,
                "paid": False,
                "products": [{"id": product_id, "quantity": 2}],
                "shipping_information": {},
                "credit_card": {},
                "transaction": {},
            }
        }

        response = client.put(
            f"/order/{order_id}",
            json={
                "order": {
                    "email": "test@example.com",
                    "shipping_information": {
                        "country": "Canada",
                        "address": "125, rue Imaginaire",
                        "postal_code": "XXX XXX",
                        "city": "Chicoutimi",
                        "province": "QC",
                    },
                }
            },
        )
        assert response.status_code == 200
        assert response.json == {
            "order": {
                "id": order_id,
                "email": "test@example.com",
                "total_price": 46.2,
                "shipping_price": 5,
                "paid": False,
                "products": [{"id": product_id, "quantity": 2}],
                "shipping_information": {
                    "country": "Canada",
                    "address": "125, rue Imaginaire",
                    "postal_code": "XXX XXX",
                    "city": "Chicoutimi",
                    "province": "QC",
                },
                "credit_card": {},
                "transaction": {},
            }
        }

        response = client.put(
            f"/order/{order_id}",
            json={
                "credit_card": {
                    "name": "John Doe",
                    "number": "4242 4242 4242 4242",
                    "cvv": "156",
                    "expiration_year": 2025,
                    "expiration_month": 5,
                }
            },
        )
        assert response.status_code == 202

        response = client.get(f"/order/{order_id}")
        assert response.status_code == 200
        assert response.json["order"]["paid"] is False

        # Wait for transaction to be handled
        sleep(2)

        response = client.get(f"/order/{order_id}")
        print(response.json)
        assert response.status_code == 200
        assert response.json["order"]["paid"] is True
        assert response.json["order"]["transaction"]["success"] is True
        assert response.json["order"]["transaction"]["amount_charged"] == 51.2

        # Clean up
        Order.delete().where(Order.id == order_id).execute()
        Product.delete().where(Product.id == product_id).execute()
