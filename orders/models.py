from django.core.validators import MinValueValidator
from django.db import models


class Customer(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return "{} ({})".format(self.name, self.email)


class Product(models.Model):
    product_code = models.CharField(max_length=255, unique=True)
    price = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.product_code


class Order(models.Model):
    order_number = models.CharField(max_length=255, unique=True)
    customer = models.ForeignKey(Customer, related_name="orders", on_delete=models.CASCADE)

    def __str__(self):
        return "Order {}".format(self.order_number)

    def get_total_price(self):
        price = 0
        for item in self.line_items.all():
            price += (item.price * item.quantity)

        return price


class LineItem(models.Model):
    order = models.ForeignKey(Order, related_name="line_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_line_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return "Line item of {}x {} on {}".format(self.quantity, self.product, self.order)
