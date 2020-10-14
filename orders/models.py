from django.db import models


class Order(models.Model):
    order_number = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return "Order {}".format(self.order_number)
