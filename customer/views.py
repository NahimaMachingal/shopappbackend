from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import generics
from .models import CustomUser, CartItem, Address, Rating
from .serializers import CustomUserSerializer, CartItemSerializer, AddressSerializer, RatingSerializer
from rest_framework.generics import ListAPIView
from shop.models import Product, Order, OrderItem
from rest_framework.permissions import IsAuthenticated
from shop.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListCreateAPIView, ListAPIView
# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response({'error': 'Incorrect email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        serializer = CustomUserSerializer(user)  # Serialize user details

        return Response({
            'user': serializer.data,  # Use serializer to return structured user data
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)



class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class CartItemListView(ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(customer=self.request.user)

class CartItemCreateView(ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(customer=self.request.user)  # Filter for the authenticated user

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class CartItemUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        try:
            product_id = request.data.get("product")
            new_quantity = request.data.get("quantity")

            cart_item = CartItem.objects.get(customer=request.user, product_id=product_id)
            cart_item.quantity = new_quantity
            cart_item.save()

            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

class CartItemRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        try:
            cart_item = CartItem.objects.get(customer=request.user, product_id=product_id)
            cart_item.delete()
            return Response({"message": "Item removed"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)


class SubmitAddressView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        customer = request.user  # Get the logged-in user
        address_data = request.data.get("address") 
        cart_items = request.data.get("cart_items", [])  # Expect cart items in the request

        if not address_data:
            return Response({"error": "Address data is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Order for the customer
        order = Order.objects.create(customer=customer)

        order_items = []
        for item in cart_items:
            try:
                product = Product.objects.get(id=item["product_id"])
                quantity = item["quantity"]
                order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity)
                order_items.append(order_item)
            except Product.DoesNotExist:
                return Response({"error": f"Product with ID {item['product_id']} not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the order with its items
        order_serializer = OrderSerializer(order)

        return Response({
            "message": "Order placed successfully!",
            "order": order_serializer.data
        }, status=status.HTTP_201_CREATED)

class SubmitOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Received request data:", request.data)
        customer = request.user
        address_data = request.data  # Since we're sending address data directly
        cart_items = request.data.get("cart_items", [])

        if not address_data:
            return Response({"error": "Address data is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Save Address
            address = Address.objects.create(
                customer=customer,
                street=address_data.get("street"),
                city=address_data.get("city"),
                state=address_data.get("state"),
                zip_code=address_data.get("zip_code")
            )

            # Create Order
            order = Order.objects.create(
                customer=customer,
                shipping_address=address  # Add this field to Order model if not present
            )

            # Create OrderItems
            for item in cart_items:
                if 'product_id' not in item:
                    raise ValidationError("product_id is required for each cart item")
                if 'quantity' not in item:
                    raise ValidationError("quantity is required for each cart item")

                try:
                    product = Product.objects.get(id=item['product_id'])
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity']
                    )
                except Product.DoesNotExist:
                    # Cleanup if product doesn't exist
                    order.delete()
                    address.delete()
                    return Response(
                        {"error": f"Product with id {item['product_id']} not found"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

            order_serializer = OrderSerializer(order)
            return Response({
                "message": "Order placed successfully!",
                "order": order_serializer.data,
                "address_id": address.id
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error processing order: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(customer=self.request.user).prefetch_related('items', 'items__product')
        print("Orders queryset:", queryset.values())  # Debug log
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        print("Response data:", response.data)  # Debug log
        return response

class SubmitRatingView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RatingSerializer

    def create(self, request, *args, **kwargs):
        # Extract data from request
        user = request.user
        product_id = request.data.get("product")
        rating_value = request.data.get("rating")

        if not product_id or not rating_value:
            return Response({"error": "Product ID and rating are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has already rated this product (Optional: To prevent duplicate ratings)
        existing_rating = Rating.objects.filter(customer=user, product_id=product_id).first()
        if existing_rating:
            existing_rating.rating = rating_value
            existing_rating.save()
            return Response(RatingSerializer(existing_rating).data, status=status.HTTP_200_OK)

        # Create new rating
        rating = Rating.objects.create(customer=user, product_id=product_id, rating=rating_value)
        return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED)