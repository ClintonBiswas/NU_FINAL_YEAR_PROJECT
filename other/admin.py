from django.contrib import admin
from .models import Product, Category, Customer, OrderPlace
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(OrderPlace)