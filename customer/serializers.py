#customer/serializers.py
from rest_framework import serializers
from .models import Address, CartItem, Rating, CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'user_type','password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}

    
    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_user_type(self, value):
        if value not in dict(CustomUser.USER_TYPE_CHOICES).keys():
            raise serializers.ValidationError("Invalid user type.")
        return value


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['product', 'product_name', 'product_price', 'product_image', 'quantity']

    def get_product_image(self, obj):
        return obj.product.image.url if obj.product.image else None


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'