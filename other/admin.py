from django.contrib import admin
from .models import Product, Category, Customer, OrderPlace, FreelancerProfile, PortfolioModel, Skills, Freelance_category, EmployeementHistory, HiredFreelancer, ContactFreelancer
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(OrderPlace)
admin.site.register(FreelancerProfile)
admin.site.register(PortfolioModel)
admin.site.register(Skills)
admin.site.register(Freelance_category)
admin.site.register(EmployeementHistory)
admin.site.register(HiredFreelancer)
admin.site.register(ContactFreelancer)