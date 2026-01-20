from django.contrib.admin.templatetags.admin_list import pagination
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer, Product, Order, OrderItem
from .serializers import CustomerSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, \
    OrderDetailSerializer, OrderStatusSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


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

        # pagination
        page_size = int(request.query_params.get('page_size', 3)) # размер страницы
        page_number = int(request.query_params.get('page_number', 1)) # номер страницы
        paginator = Paginator(orders, page_size)

        serializer = OrderSerializer(paginator.get_page(page_number), many=True)

        return Response(serializer.data)


    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class OrderDetailAPIView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        serializer = OrderDetailSerializer(order)

        return Response(serializer.data)


class OrderStatusAPIView(APIView):
    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        serializer = OrderStatusSerializer(order, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class OrderItemsAPIView(APIView):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        serializer = OrderItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_item = serializer.save(order=order)

        order.save() # чтобы обновилось поле updated_at

        if order.status == 'paid':
            product = order_item.product
            product.stock -= order_item.quantity
            product.save()

        return Response(OrderItemSerializer(order_item).data)