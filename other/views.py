from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from user.models import RefBooks, NuQuestion, AddProjects, ProgrammingContest,Contact, OurTeam
from other.models import Category, Product, OrderPlace, Customer
from .forms import CustomerForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Create your views here.
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

# Email threading to send faster
def send_email_thread(subject, message, from_email, to_email):
    send_mail(subject, message, from_email, to_email, fail_silently=True)


def Home(request):
    project = AddProjects.objects.all()
    team = OurTeam.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        print(email)
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, description=message)
        # email_message = EmailMessage(
        # f'Hi {name}, Thanks for Contacting With me',
        # 'Our customer agent will contact you soon.',
        # settings.EMAIL_HOST_USER,
        # [email],
        # )
        # EmailThread(email_message).start()
        messages.success(request,"Thanks for submission. Please check your email")
    
    dict = {'projects':project,'teams': team}
    return render(request, 'other/home.html', context=dict)

def SearchView(request):
    query = request.GET.get('query')
    results = []
    results1 = []
    if query:
        results = RefBooks.objects.filter(book_name__icontains=query)
        try:
            query_int = int(query)  # Convert the input value to an integer
            results1 = NuQuestion.objects.filter(
                Q(subject_name__icontains=query) |
                Q(question_type__icontains=query) |
                Q(question_year=query_int)
            )
        except ValueError:
            results1 = NuQuestion.objects.filter(
                Q(subject_name__icontains=query) |
                Q(question_type__icontains=query)
            )

    dict = {'results': results, 'results1': results1, 'query': query}
    return render(request, 'other/search.html', context=dict)

def projectDetails(request, slug):
    project = AddProjects.objects.get(slug=slug)
    dict = {'project':project}
    return render(request, 'other/project_d.html', context=dict)


def RefBooksView(request):
    book = RefBooks.objects.all()
    dict={'books': book}
    return render(request, 'other/ref_bookV.html', context=dict)

def NuQuestionView(request):
    question = NuQuestion.objects.all()
    dict={'questions': question}
    return render(request, 'other/question.html', context=dict)

def ProgrammingContestView(request):
    contest = ProgrammingContest.objects.all()
    dict = {'contests':contest}
    return render(request, 'other/pcontest.html', context=dict)

def ProductView(request):
    category_list = Category.objects.all()
    product_list = Product.objects.all()
    dict = {'categorys':category_list, 'products': product_list}
    return render(request, 'other/product.html', context=dict)

def ProductDetailsView(request, slug):
    products = Product.objects.get(slug=slug)
    dict = {'products':products}
    return render(request, 'other/product_detail.html', context=dict)

def CategoryProductView(request, pk):
    category_p = Category.objects.get(pk=pk)
    product_list = Product.objects.filter(category=category_p)
    category_list = Category.objects.all()
    dict = {'products': product_list, 'categorys':category_list, 'category': category_p}
    return render(request, 'other/category_product.html', context=dict)

# def ConfirmOrder(request, slug):
#     order_product = Product.objects.get(slug=slug)
#     dict = {}
#     return render(request, 'other/confirm_order.html', context=dict)

@login_required
def OrderPlaceView(request, slug):
    total_amount = 0.00
    user = request.user
    customer_info = Customer.objects.filter(user=user)
    products = Product.objects.get(slug=slug)

    if customer_info:
        shipping_amount = Decimal('60.00')
        total_amount = products.price + shipping_amount
        dict = {'customers': customer_info, 'product': products, 'product_price': total_amount}
        return render(request, 'other/confirm_order.html', context=dict)
    else:
        messages.warning(request, 'Please add a product shipping address information')
        form = CustomerForm()
        if request.method == 'POST':
            form = CustomerForm(request.POST)
            if form.is_valid():
                customer = form.save(commit=False)
                customer.user = request.user
                customer.save()
                return redirect('other:order-place', slug=slug)

        dict = {'form': form}
        return render(request, 'other/confirm_order.html', context=dict)

    # print(products)
    # if names:
    #     name = names[0]
    #     products = Product.objects.get(slug=slug)
    #     customer_name = Customer.objects.get(name=name, user=request.user)
    #     OrderPlace.objects.create(user=request.user, customer=customer_name, product=products)
    #     shipping_amount = Decimal('60.00')
    #     total_amount = products.price + shipping_amount
         # send email when a user suceesfull order placed
         # subject = 'Order Placed'
         # message = f'Hi {name},\n We received your order. Your Order is accepted.\n We will deliver the product within the next 3 days. \n Product Name: {products.title}. \n Price: {total_amount}'
         # from_email = settings.DEFAULT_FROM_EMAIL
         # to_email = [request.user.email]

         # thread = threading.Thread(
         #     target=send_email_thread,
         #     args=(subject, message, from_email, to_email),
         # )
         # thread.start()

    # else:
    #     messages.warning(request, 'Please add a product shipping address information')
    #     form = CustomerForm()
    #     if request.method == 'POST':
    #         form = CustomerForm(request.POST)
    #         if form.is_valid():
    #             customer = form.save(commit=False)
    #             customer.user = request.user
    #             customer.save()
                 # name = form.cleaned_data['name']
                 # address = form.cleaned_data['address']
                 # phone = form.cleaned_data['phone']
    #             OrderPlace.objects.create(user=request.user, customer=customer, product=products)

     # Move this line outside the POST request handling
    # form = CustomerForm()

    # dict = {'customers': customer_info, 'product': products, 'product_price': total_amount, 'form': form}
    # return render(request, 'other/confirm_order.html', context=dict)

@login_required
def YourOrder(request, slug):
    total_amount = 0.00
    product = Product.objects.get(slug=slug)
    customer = Customer.objects.get(user=request.user)
    shipping_amount = Decimal('60.00')
    total_amount = product.price + shipping_amount
    if request.method == 'POST':
        OrderPlace.objects.create(user=request.user, customer=customer, product=product)
        messages.success(request, 'Thank you for placing your order with us. We are pleased to inform you that your order has been successfully placed and is being processed')
        subject = 'Order Placed'
        message = f'Hi {customer.name},\n We received your order. Your Order is accepted.\n We will deliver the product within the next 3 days. \n Product Name: {product.title}. \n Price: {total_amount}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [request.user.email]

        thread = threading.Thread(
             target=send_email_thread,
             args=(subject, message, from_email, to_email),
         )
        thread.start()
        return redirect('other:order-item', slug=slug)
    
    order_infos = OrderPlace.objects.filter(user=request.user, status='Accepted')
    previous_order = OrderPlace.objects.filter(user=request.user, status='Delivered')
    dict = {'order_infos': order_infos, 'previous_order': previous_order, 'total_amount':total_amount,}
    return render(request, 'other/your_order.html', context=dict)



@login_required
def ProfileView(request):
    user_info = User.objects.get(username=request.user)
    customers = Customer.objects.filter(user=request.user).first()
    dict = {'user_infos': user_info, 'customers': customers}
    return render(request, 'other/profile.html', context=dict)


@login_required
def UpdateProfileView(request):
    user = request.user
    customer_data, created = Customer.objects.get_or_create(user=user)

    if request.method == 'POST':
        customer_data.name = request.POST.get('name')
        customer_data.address = request.POST.get('address')
        customer_data.phone = request.POST.get('phone')

        if 'profile_pic' in request.FILES:
            customer_data.profile_pic = request.FILES['profile_pic']
        customer_data.save()

        return redirect('other:profile')

    dict = {'customer_data': customer_data}
    return render(request, 'other/update_profile.html', context=dict)

