from api8inf349.models import Product


class TestOrder(object):
    def test_create_order(self, app, client):
        Product.create(
            id=1,
            name="Test",
            description="Test routes index",
            in_stock=True,
            price=23.1,
            weight=200,
            image="test.jpg",
        )

        response = client.post(
            "/order",
            json={"product": {"id": 1, "quantity": 2}},
        )
        assert response.status_code == 302
        assert response.location == "/order/1"

        response = client.get("/order/1")
        assert response.status_code == 200
        assert response.json == {
            "order": {
                "id": 1,
                "email": None,
                "total_price": 46.2,
                "shipping_price": 5,
                "paid": False,
                "products": [{"id": 1, "quantity": 2}],
                "shipping_information": {},
                "credit_card": {},
                "transaction": {},
            }
        }

        response = client.put(
            "/order/1",
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
                "id": 1,
                "email": "test@example.com",
                "total_price": 46.2,
                "shipping_price": 5,
                "paid": False,
                "products": [{"id": 1, "quantity": 2}],
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
            "/order/1",
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
        assert response.status_code == 200
        assert response.json["order"]["paid"] is True
        assert response.json["order"]["credit_card"] == {
            "name": "John Doe",
            "first_digits": "4242",
            "last_digits": "4242",
            "expiration_year": 2025,
            "expiration_month": 5,
        }
        assert response.json["order"]["transaction"]["success"] is True
        assert response.json["order"]["transaction"]["amount_charged"] == 51.2
