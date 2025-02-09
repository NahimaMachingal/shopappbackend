# shop/serializers.py (Admin Side)
from rest_framework import serializers
from .models import Product, Order, OrderItem, CustomUser


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'created_at', 'items']

    def get_customer(self, obj):
        return {
            'id': obj.customer.id,
            'username': obj.customer.username
        }