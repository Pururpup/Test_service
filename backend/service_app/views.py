from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer, Product, Order
from .serializers import CustomerSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, \
    OrderDetailSerializer, OrderStatusSerializer


# paginator
class CustomPagination(PageNumberPagination):
    page_size = 3 # размер страницы по умолчанию
    page_size_query_param = 'page_size'
    max_page_size = 50


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('pk')
    serializer_class = CustomerSerializer
    pagination_class = CustomPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('pk')
    serializer_class = ProductSerializer
    pagination_class = CustomPagination


class OrderAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all().order_by('pk')

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
        paginator = CustomPagination()
        page = paginator.paginate_queryset(orders, request, view=self)
        # page возвращает список объектов для текущей страницы

        # orders - список, для которого пагинация применяется
        # request - чтение параметров page и page_size (page=1 по умолчанию, а page_size берется из CustomPagination)
        # view=self - ссылка на текущее APIView для формирования ссылки next/previous

        serializer = OrderSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)


    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

        return Response(OrderItemSerializer(order_item).data, status=status.HTTP_201_CREATED)