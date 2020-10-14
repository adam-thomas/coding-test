from django.test import TestCase

from orders.models import Customer, LineItem, Order, Product
from orders.parse_orders import parse_orders


class TestParseOrders(TestCase):
    """
    Stop right there! Didn't you read the sign? Don't look in here!

    If you are taking a peek, I assume that means one of three things:
      1) You're cheating. Stop it.
      2) You've finished the test already and you're curious. Carry on.
      3) You're a bit stuck and have given in to the temptation for a hint.

    If #3 is what you want, perhaps I can help out without having to completely peel back the curtain. Remember that:
      * The documentation, while not necessarily inaccurate, doesn't give you the full picture. Sometimes the data
        format is a bit different. Have you looked at what api_data actually contains in each case?
      * The feedback from your stakeholders is very vague and functional. You could try to isolate what the
        actual discrepancy in data could be, and work from there. Examine the objects you've actually produced,
        and compare them to what you think the stakeholders expect.
      * If you haven't made every test pass - don't worry about it. I'm more interested in your approach, the
        decisions you made along the way, and your coding style. Your time is important to me and I don't want you
        to sink hours of your life into this if you've got other things to do. Perhaps jot down what you've
        discovered or struggled with, and we can talk about it in the interview :)
      * And of course if something is just plain confusing, or you're stuck, shoot me an email. I would be an
        idiot to assume that this test is completely clear or robust - I may just have made something too hard
        or too obscure.

    Still reading? I really can't persuade you to turn away? Pfft, some people.
    """
    def setUp(self):
        self.customer = Customer.objects.create(email="leeroy.jenkins@example.com", name="Leeroy Jenkins")

        self.product_one = Product.objects.create(product_code="SMALL-HAT", price=10.0)
        self.product_two = Product.objects.create(product_code="REALLY-BIG-HAT", price=250.0)


    def test_one(self):
        api_data = {
            "orders": [
                {
                    "number": "001234",
                    "customer_email": "leeroy.jenkins@example.com",
                    "line_items": [
                        {"sku": "SMALL-HAT", "quantity": 1}
                    ]
                }
            ]
        }

        parse_orders(api_data)

        self.assertEqual(Order.objects.count(), 1, msg="Order 001234 isn't in the system!")
        order = Order.objects.first()

        self.assertEqual(order.order_number, "001234", msg="Order 001234 isn't in the system!")
        self.assertEqual(
            order.customer.pk, self.customer.pk,
            msg="We had an email from Leeroy Jenkins telling us their order hasn't arrived"
        )
        self.assertEqual(order.line_items.count(), 1, msg="Order 001234 has the wrong products on it")

        item = order.line_items.first()
        self.assertEqual(item.product.pk, self.product_one.pk, msg="Order 001234 has the wrong products on it")
        self.assertEqual(item.quantity, 1, msg="Order 001234 has the wrong product quantity on it")
        self.assertEqual(
            item.price, self.product_one.price,
            msg="The customer has been charged the wrong amount for order 001234!"
        )


    def test_two(self):
        api_data = {
            "orders": [
                {
                    "number": "002345-1",
                    "customer_email": "leeroy.jenkins@example.com",
                    "line_items": [
                        {"sku": "SMALL-HAT", "quantity": 1},
                    ]
                },
                {
                    "number": "002345-2",
                    "customer_email": "leeroy.jenkins@example.com",
                    "line_items": [
                        {"sku": "SMALL-HAT", "quantity": 3},
                        {"sku": "REALLY-BIG-HAT", "quantity": 2, "discount_price": 150.0},
                    ]
                }
            ]
        }

        parse_orders(api_data)

        self.assertEqual(Order.objects.count(), 2, msg="Not all our orders have come through!")
        self.assertTrue(
            Order.objects.filter(order_number="002345-1").exists(),
            msg="Order 002345-1 isn't in the system!"
        )
        self.assertTrue(
            Order.objects.filter(order_number="002345-2").exists(),
            msg="Order 002345-2 isn't in the system!"
        )

        order = Order.objects.get(order_number="002345-2")

        self.assertEqual(
            order.customer.pk, self.customer.pk,
            msg="We had an email from Leeroy Jenkins telling us their order is missing"
        )

        self.assertEqual(order.line_items.count(), 2, msg="Order 002345-2 has the wrong products on it")
        self.assertEqual(
            order.get_total_price(), 330.0,
            msg="The customer has been charged the wrong amount for order 002345-2!"
        )

        item = order.line_items.get(product=self.product_one)
        self.assertEqual(item.quantity, 3, msg="Order 002345-2 has the wrong product quantity on it")

        item = order.line_items.get(product=self.product_two)
        self.assertEqual(item.quantity, 2, msg="Order 002345-2 has the wrong product quantity on it")


    def test_three(self):
        api_data = {
            "orders": [
                {
                    "number": "003456",
                    "customer_email": "leeroy.jenkins@example.com",
                    "line_items": [
                        {"sku": "SMALL-HAT", "quantity": 1}
                    ]
                }
            ]
        }

        parse_orders(api_data)

        api_data_edited = {
            "orders": [
                {
                    "number": "003456",
                    "customer_email": "leeroy.jenkins@example.com",
                    "line_items": [
                        {"sku": "REALLY-BIG-HAT", "quantity": 1},
                    ]
                }
            ]
        }

        parse_orders(api_data_edited)

        self.assertEqual(Order.objects.count(), 1, msg="Order 003456 isn't in the system!")
        order = Order.objects.first()

        self.assertEqual(order.order_number, "003456", msg="Order 003456 isn't in the system!")
        self.assertEqual(
            order.customer.pk, self.customer.pk,
            msg="We had an email from Leeroy Jenkins telling us their order is missing"
        )

        self.assertEqual(
            order.line_items.count(), 1,
            msg=("Order 003456 has an unwanted product - the customer emailed to say they don't want a small hat, "
                 "just the really big one")
        )

        item = order.line_items.first()
        self.assertEqual(
            item.product.pk, self.product_two.pk,
            msg=("Order 003456 has the wrong product on it - the customer emailed to say they don't want a small hat, "
                 "they want the really big one instead")
        )


    def test_four(self):
        parse_orders({})


    def test_five(self):
        parse_orders({"orders": []})


    def test_six(self):
        api_data = {
            "orders": [
                {
                    "number": "004567",
                    "customer_email": "darth.vader@example.com",
                    "line_items": [
                        {"sku": "SMALL-HAT", "quantity": 1}
                    ]
                }
            ]
        }

        parse_orders(api_data)

        self.assertEqual(Order.objects.count(), 1, msg="Order 004567 isn't in the system!")
        order = Order.objects.first()

        self.assertEqual(order.order_number, "004567", msg="Order 004567 isn't in the system!")

        self.assertEqual(
            Customer.objects.count(), 2,
            msg="We had an email from Darth Vader telling us their order hasn't arrived"
        )
        self.assertEqual(
            order.customer.email, "darth.vader@example.com",
            msg="We had an email from Darth Vader telling us their order hasn't arrived"
        )
