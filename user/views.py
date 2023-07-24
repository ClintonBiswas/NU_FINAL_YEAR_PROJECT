from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm, RefBooksForm, NuQuestionForm, AddProjectsForm, ProgrammingContestForm, OurTeamForm
# Create your views here.

def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('other:home')
        else:
            # Add error messages to the messages framework
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, f"{field}: {error}")
    else:
        form = RegisterForm()
    
    dict = {'form': form}
    return render(request, 'user/register.html', context=dict)

def UserLoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}.")
                return redirect('other:home')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")

    form = AuthenticationForm()
    dict = {'form': form}
    return render(request, 'user/login.html', context=dict)

def LogoutView(request):
    logout(request)
    # messages.info(request, "You have successfully logged out.") 
    return redirect('other:home')

def AddBookView(request):
    if request.method == 'POST':
        form = RefBooksForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.user = request.user
            pdf.save()
            messages.success(request,"Ref Book Added Successfully")
    form = RefBooksForm()
    dict = {'form':form}
    return render(request, 'user/add_book.html', context=dict)

def NuQuestionAdd(request):
    if request.method == 'POST':
        form = NuQuestionForm(request.POST, request.FILES)
        if form.is_valid():
            nu = form.save(commit=False)
            nu.user = request.user
            nu.save()
            messages.success(request,"Question Added Successfully")
    form = NuQuestionForm()
    dict={'form':form}
    return render(request, 'user/nu_question_add.html', context=dict)

def AddProjectView(request):
    if request.method == 'POST':
        form = AddProjectsForm(request.POST, request.FILES)
        if form.is_valid():
            pro = form.save(commit=False)
            pro.user = request.user
            pro.save()
            messages.success(request,"Project Added Successfully")
    form = AddProjectsForm()
    dict={'form':form}
    return render(request, 'user/add_project.html', context=dict)

def AddProgrammingContest(request):
    if request.method == 'POST':
        form = ProgrammingContestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Contest Added Successfully")
    form = ProgrammingContestForm()
    dict={'form':form}
    return render(request, 'user/add_pro_contest.html', context=dict)

def AddOurTeam(request):
    if request.method == 'POST':
        form = OurTeamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Team Member Added Successfully")
    form = OurTeamForm()
    dict={'form':form}
    return render(request, 'user/add_team.html', context=dict)
