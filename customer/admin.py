from django.contrib import admin
from .models import CustomUser, Address, CartItem, Rating
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Address)
admin.site.register(CartItem)
admin.site.register(Rating)
