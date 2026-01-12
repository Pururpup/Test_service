from django.db import models


class Customer(models.Model):
    name = models.CharField()
    email = models.EmailField()
    created_at = models.DateTimeField()


class Product(models.Model):
    name = models.CharField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('paid', 'Оплачено'),
        ('shipped', 'Отправлено'),
        ('cancelled', 'Отменено'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


# товар в заказе
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField() # количество этих товаров в заказе
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2) # цена товара в момент заказа
