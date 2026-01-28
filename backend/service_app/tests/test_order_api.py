from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from service_app.models import Order, Customer, Product, OrderItem
from service_app.serializers import OrderSerializer


class OrderApiTestCase(APITestCase):
    def test_get_orders(self):
        customer = Customer.objects.create(name='Покупатель 4', email='pok_4@gmail.com')

        order_1 = Order.objects.create(customer=customer, status='new')
        order_2 = Order.objects.create(customer=customer, status='new')

        url = reverse('orders-list')
        response = self.client.get(url)

        serializer_data = OrderSerializer([order_1, order_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_post_order(self):
        url = reverse('orders-list')
        customer = Customer.objects.create(name='Покупатель 5', email='pok_5@gmail.com')
        data = {
            'customer': customer.pk,
            'status': 'new'
        }
        response = self.client.post(url, data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Order.objects.filter(
            customer=customer,
            status='new'
            ).exists()
        )


class OrderStatusApiTestCase(APITestCase):
    def test_patch_order_status(self):
        customer = Customer.objects.create(name='Покупатель 6', email='pok_6@gmail.com')
        order = Order.objects.create(customer=customer, status='new')

        url = reverse('orders-status', args=[order.pk])
        data = {
            'status': 'paid'
        }
        response = self.client.patch(url, data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(Order.objects.filter(
            pk=order.pk,
            status='paid'
            ).exists()
        )


class OrderItemsApiTestCase(APITestCase):
    def test_post_order_item(self):
        customer = Customer.objects.create(name='Покупатель 7', email='pok_7@gmail.com')
        order = Order.objects.create(customer=customer, status='paid')
        product = Product.objects.create(name='Товар 1', price=10.50, stock=100)

        url = reverse('orders-item', args=[order.pk])
        data = {
            'product': product.pk,
            'quantity': 65,
            'price_at_order': 1999.00
        }

        response = self.client.post(url, data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(OrderItem.objects.filter(
            order=order,
            product=product,
            quantity=data['quantity'],
            price_at_order=data['price_at_order']
            ).exists()
        )