from django.core.serializers import serialize
from django.db.models import Sum
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from models import Customer, Product, Order, OrderItem
from serializers import CustomerListSerializer, CustomerSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer


class CustomerAPIView(APIView):
    def get(self, request):
        print("CUSTOMER LIST VIEW CALLED")
        customers = Customer.objects.all()
        serializer = CustomerListSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CustomerDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


class ProductAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request):
        product_id = request.data.get('id')

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request):
        product_id = request.data.get('id')

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        product_id = request.data.get('id')

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all()

        filter_status = request.query_params.get('status')
        if filter_status:
            orders = orders.filter(status=filter_status)

        filter_customer_id = request.query_params.get('customer_id')
        if filter_customer_id:
            orders = orders.filter(customer_id=filter_customer_id)

        filter_created_at = request.query_params.get('created_at')
        if filter_created_at:
            orders = orders.filter(created_at=filter_created_at)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OrderDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        items = OrderItem.objects.filter(order_id=pk)
        total_price = sum(item.quantity * item.price_at_order for item in items)

        order_details = OrderSerializer(order).data
        order_details['total_price'] = total_price # добавили поле total_price
        return Response(order_details)


class OrderStatusAPIView(APIView):
    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data)


class OrderItemsAPIView(APIView):
    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrderItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        if product.stock < quantity:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        order_item = serializer.save(order=order)

        if order.status == 'paid':
            product.stock -= quantity
            product.save()

        return Response(OrderItemSerializer(order_item).data)













