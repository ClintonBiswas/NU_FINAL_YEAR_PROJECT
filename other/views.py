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
from other.models import Category, Product, OrderPlace, Customer, FreelancerProfile, Freelance_category, Skills, EmployeementHistory, HiredFreelancer
from .forms import CustomerForm, FreelancerProfileForm, HiredFreelancerForm, SkillForm, EmployeementHistoryForm, ContactFreelancerForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


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


# expert Section
def ExpertCreateView(request):
    form = FreelancerProfileForm()
    superusers = User.objects.filter(is_superuser=True)
    result = [user.email for user in superusers]
    print(result)
    if request.method == 'POST':
        form = FreelancerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile_pic = form.save(commit=False)
            profile_pic.user = request.user  # Assign the User instance to the user field of FreelancerProfile
            profile_pic.save()
            subject = 'Request for an expert account'
            message = f'Hi Admin,\n You received a request for approval of an expert account.'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = result

            thread = threading.Thread(
                target=send_email_thread,
                args=(subject, message, from_email, to_email),
            )
            thread.start()
            messages.success(request, 'Thank you for applying. Please wait for 24 hours while our agent checks your information. If everything is okay, we will approve your profile, and you can visit it')
            #return redirect('other:expert-profile')  # Redirect to the expert profile page after successful form submission

    context = {'form': form}
    return render(request, 'other/expertcreate.html', context)



def ExpertProfileView(request, pk):
    pk=int(pk)
    profile = get_object_or_404(FreelancerProfile, user__pk=pk)
    user = FreelancerProfile.objects.get(user__pk=pk)
    try:
        skill = Skills.objects.get(user=user)
    except Skills.DoesNotExist:
        skill = None
    
    result = []
    if skill:
        result = skill.skill.split(',')

    try:
        employents = EmployeementHistory.objects.get(user=user)
    except EmployeementHistory.DoesNotExist:
        employents = None 
    
    workhistory = HiredFreelancer.objects.filter(freelancer__user__pk=pk)
    print(len(workhistory))
    context = {'profile': profile, 'skills': result, 'employents': employents, 'workhistory':workhistory}
    return render(request, 'other/expert_profile.html', context)
def ExpertProfileUpdate(request, pk):
    pk = int(pk)
    try:
        profile_info = FreelancerProfile.objects.get(user__pk=pk)
    except FreelancerProfile.DoesNotExist:
        profile_info = None
    if request.method == 'POST':
        form = FreelancerProfileForm(request.POST, request.FILES, instance=profile_info)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('other:freelance-profile',pk=pk)
    else:
        form = FreelancerProfileForm(instance=profile_info)

    context = {
        'form':form
    }
    return render(request, 'other/expertprofile_update.html', context)


def OurExpertView(request):
    user = request.user
    experts = FreelancerProfile.objects.filter(user__is_staff=True)
    categories = Freelance_category.objects.all()
    dict = {'experts':experts, 'categories':categories}
    return render(request, 'other/our_expert.html', context=dict)

def ExpertCategoryView(request, slug):
    category = Freelance_category.objects.get(slug=slug)
    experts = FreelancerProfile.objects.filter(category=category)
    categories = Freelance_category.objects.all()
    print(experts)
    context = {
        'experts':experts,
        'categories':categories,
        'category':category
    }
    return render(request, 'other/expert_category.html', context)

def hire_freelancer_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('user:login')  # Redirect unauthenticated users to the login page or show an error message

    freelancer = get_object_or_404(FreelancerProfile, user__pk=pk)

    if request.method == 'POST':
        form = HiredFreelancerForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.client = request.user
            instance.freelancer = freelancer
            instance.save()

            # Send email to the client
            client_subject = 'Hired Successfully'
            client_message = f'Hi {instance.client.username},\nYou have successfully hired {instance.freelancer.full_name} for the project.\nHere are the details of your hire:\nJob Title: {instance.job_title}\nJob Requirement: {instance.job_requirement}\nDelivery Date: {instance.delivery_date}\nProject Price: {instance.project_price}\n\nThank you for using our platform!\nBest regards,\nYour Company Name'
            client_email = EmailMessage(client_subject, client_message, settings.DEFAULT_FROM_EMAIL, [instance.client.email])

            # Send email to the freelancer
            freelancer_subject = 'New Hire'
            freelancer_message = f'Hi {instance.freelancer.full_name},\nCongratulations! You have been hired by {instance.client.username} for a new project.\nHere are the details of your hire:\nJob Title: {instance.job_title}\nJob Requirement: {instance.job_requirement}\nDelivery Date: {instance.delivery_date}\nProject Price: {instance.project_price}\n\nGood luck with the project!\nBest regards,\nYour Company Name'
            freelancer_email = EmailMessage(freelancer_subject, freelancer_message, settings.DEFAULT_FROM_EMAIL, [instance.freelancer.user.email])

            # Start a thread for sending emails
            client_thread = threading.Thread(target=send_email_thread, args=(client_subject, client_message, settings.DEFAULT_FROM_EMAIL, [instance.client.email]))
            freelancer_thread = threading.Thread(target=send_email_thread, args=(freelancer_subject, freelancer_message, settings.DEFAULT_FROM_EMAIL, [instance.freelancer.user.email]))

            client_thread.start()
            freelancer_thread.start()

            messages.success(request, 'You hired successfully. Please check your email address')

    else:
        form = HiredFreelancerForm()

    context = {
        'form': form,
        'freelancer': freelancer,
    }
    return render(request, 'other/hire_freelancer_form.html', context)

def ContactWithMeView(request, pk):
    pk = int(pk)
    names = FreelancerProfile.objects.get(user__pk=pk)

    if request.method == 'POST':
        form = ContactFreelancerForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = names  # Set the 'user' field with the 'FreelancerProfile' object

            instance.save()
            subject = 'You received a message from a client'
            message = f'Hi {names.full_name},\n Client Info \n Client Name: {instance.name} \n Client Email: {instance.email} \n Client Message: {instance.message}'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [names.user.email]  # Make sure to pass the recipient email as a list or tuple

            # Send the email using the send_mail() function
            send_mail(subject, message, from_email, to_email, fail_silently=False)

            messages.success(request, 'Thanks for contacting with me. I will respond as soon as possible')
    else:
        form = ContactFreelancerForm()
    context = {
        'form': form,
        'names': names,
    }
    return render(request, 'other/freelance_contact.html', context)


def ExpertProfileSkill(request, pk):
    user = FreelancerProfile.objects.get(user__pk=int(pk))
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            return redirect('other:freelance-profile',pk=pk)
    else:
        form = SkillForm()
    context={
        'form':form
    }
    return render(request, 'other/expert_skill.html', context)

def ExpertProfileSkillUpdate(request, pk):
    user = FreelancerProfile.objects.get(user__pk=int(pk))
    print(user.id)
    try:
        skill_instance = Skills.objects.get(user=user)
    except Skills.DoesNotExist:
        skill_instance = None

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill_instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            return redirect('other:freelance-profile', pk=pk)
    else:
        form = SkillForm(instance=skill_instance)

    context = {
        'form': form,
    }
    return render(request, 'other/updateexpert_skill.html', context)

def EmployementHistoryView(request, pk):
    user = FreelancerProfile.objects.get(user__pk=int(pk))
    if request.method == 'POST':
        form = EmployeementHistoryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            return redirect('other:freelance-profile', pk=pk)
    else:
        form = EmployeementHistoryForm()
    context ={'form':form}
    return render(request, 'other/employement_history.html', context)

def EmployementHistoryUpdate(request, pk):
    user = FreelancerProfile.objects.get(user__pk=int(pk))
    try:
        employe_instance = EmployeementHistory.objects.get(user=user)
    except EmployeementHistory.DoesNotExist:
        employe_instance = None

    if request.method == 'POST':
        form = EmployeementHistoryForm(request.POST, instance=employe_instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            return redirect('other:freelance-profile', pk=pk)
    else:
        form = EmployeementHistoryForm(instance=employe_instance)
    context ={
        'form':form
    }
    return render(request, 'other/employementupdate_history.html', context)
