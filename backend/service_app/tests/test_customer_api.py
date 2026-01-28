from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from service_app.models import Customer
from service_app.serializers import CustomerSerializer


class CustomerApiTestCase(APITestCase):
    def test_get_customers(self):
        customer_1 = Customer.objects.create(name='Покупатель 1', email='pok_1@gmail.com')
        customer_2 = Customer.objects.create(name='Покупатель 2', email='pok_2@gmail.com')

        url = reverse('customers-list')
        response = self.client.get(url)

        serializer_data = CustomerSerializer([customer_1, customer_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_post_customer(self):
        url = reverse('customers-list')
        data = {
            'name': 'Покупатель 3',
            'email': 'pok_3@gmail.com'
        }
        response = self.client.post(url, data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Customer.objects.filter(
            name='Покупатель 3',
            email='pok_3@gmail.com'
            ).exists()
        )
