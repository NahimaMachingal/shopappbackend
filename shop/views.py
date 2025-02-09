#shop/views.py

from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from customer.models import CustomUser
from .models import Product, Order
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from customer.serializers import CustomUserSerializer
from .serializers import ProductSerializer, OrderSerializer

class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class AdminOrderListView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.prefetch_related("items", "items__product", "customer")
        print(f"Found {queryset.count()} orders") # Debug log
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        print("Serialized data:", serializer.data) # Debug log
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UpdateOrderStatusView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            new_status = request.data.get("status")
            if new_status in dict(Order.STATUS_CHOICES):
                order.status = new_status
                order.save()
                return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)