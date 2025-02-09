#customer/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import apps

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    )

    username=models.CharField(max_length= 250,unique=True)
    email=models.EmailField(max_length=250,unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')  # New Field
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return self.email

class Address(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.zip_code}"

class CartItem(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Rating(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.customer.username} rated {self.product.name} {self.rating}/5"