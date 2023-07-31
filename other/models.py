from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='customer_profile_pic', blank=True, null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=13)

    def __str__(self) -> str:
        return self.name

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)

class OrderPlace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, default='Pending', max_length=100)

    class Meta:
        ordering = ('order_date',)

    def __str__(self):
        return str(self.product)

    def save(self, *args, **kwargs):
        # Check if the instance is being newly created (no primary key)
        if not self.pk:
            self.status = 'Accepted'
        super().save(*args, **kwargs)
    @property
    def Total_Cost(self):
        return self.quantity * self.product.price

# experts section

class Freelance_category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Freelance_category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

STATUS_CHOICES_PROFILE = (
    ('Available Now', 'Available Now'),
    ('I am going on vacation', 'I am going on vacation'),
)

class FreelancerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, help_text="Enter your full name")
    location = models.CharField(max_length=255, help_text='E.g. city,coutry Dhaka, Bangladesh', blank=True, null=True)
    set_available = models.CharField(choices=STATUS_CHOICES_PROFILE, default='Available Now', max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, help_text='E.g. Django developer, javascript developer')
    category = models.ForeignKey(Freelance_category, on_delete=models.CASCADE)
    hourly_rate = models.CharField(max_length=10,help_text='E.g. $15')
    description = models.TextField(max_length=2000, help_text='E.g. within 2000 characters')
    other_experience = models.CharField(max_length=1000, help_text='E.g. within 1000 characters',blank=True, null=True)
    profile_pic = models.ImageField(upload_to='freelance_profile_pricture')


    def __str__(self):
        return self.user.username

class PortfolioModel(models.Model):
    user = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    portfolio = models.ImageField(upload_to='ferrlancer_portfolio')
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title
class Skills(models.Model):
    user = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    skill = models.TextField(max_length=2000, help_text='E.g. python, django, react')

    def __str__(self) -> str:
        return self.user.full_name

class EmployeementHistory(models.Model):
    user = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255)
    role = models.CharField(max_length=500)
    join_date = models.CharField(max_length=255, help_text='E.g. March, 2023')
    short_bio = models.CharField(max_length=500, blank=True, null=True, help_text='E.g. about company')

    def __str__(self) -> str:
        return self.user.full_name
    
STATUS_CHOICES_HIRED = (
    ('Accepted', 'Accepted'),
    ('Completed', 'Completed'),
)
class HiredFreelancer(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=500, help_text='E.g. within 500 characters')
    job_requirement = models.TextField()
    delivery_date = models.DateField(null=True, blank=True, help_text='E.g. YYYY-MM-DD format')
    project_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='E.g. 100.00')
    status = models.CharField(choices=STATUS_CHOICES_HIRED, default='Accepted', blank=True, null=True, max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.job_title}"

class ContactFreelancer(models.Model):
    user = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, help_text='E.g. Full Name')
    email = models.EmailField(max_length=255, help_text='E.g. Enter Your Email')
    message = models.TextField()

    def __str__(self) -> str:
        return self.user.full_name
    


