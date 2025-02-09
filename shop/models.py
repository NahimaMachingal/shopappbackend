#shop/models.py

from django.db import models
from cloudinary.models import CloudinaryField
from customer.models import CustomUser, Address


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = CloudinaryField('image', null=True, blank=True)  # Replaced ImageField with CloudinaryField
    average_rating = models.FloatField(default=0.0)

    def update_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            self.average_rating = sum(r.rating for r in ratings) / ratings.count()
            self.save()

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    shipping_address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"