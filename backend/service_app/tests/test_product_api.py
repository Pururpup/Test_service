from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from service_app.models import Product
from service_app.serializers import ProductSerializer


class ProductApiTestCase(APITestCase):
    def test_get_products(self):
        product_1 = Product.objects.create(name='Товар 1', price=10.50, stock=100)
        product_2 = Product.objects.create(name="Товар 2", price=20.00, stock=50)

        url = reverse('products-list') # получаем url
        response = self.client.get(url) # отправляем запрос

        serializer_data = ProductSerializer([product_1, product_2], many=True).data
        # сериализуем товары вручную
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])
        # сравниваем их с ответом, который вернул API

    def test_post_product(self):
        url = reverse('products-list')
        data = {
            'name': 'Товар 3',
            'price': 15.99,
            'stock': 30
        }
        response = self.client.post(url, data) # отправляем запрос

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Product.objects.filter(
            name='Товар 3',
            price=data['price'],
            stock=data['stock']
            ).exists()
        ) # проверяем, что товар существует в бд

