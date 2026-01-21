from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Customer, Product, Order, OrderItem


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrderDetailSerializer(OrderSerializer):
    list_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_list_items(self, obj):
        items = OrderItem.objects.filter(order_id=obj.pk)
        list_items = OrderItemSerializer(items, many=True).data
        return list_items

    def get_total_price(self, obj):
        items = OrderItem.objects.filter(order_id=obj.pk)
        total_price = sum(item.quantity * item.price_at_order for item in items)
        return total_price


class OrderStatusSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['status',]


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price_at_order']

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']

        if product.stock < quantity:
            raise serializers.ValidationError('На складе недостаточно товара')

        return data
