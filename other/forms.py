from django import forms
from .models import Customer, FreelancerProfile, HiredFreelancer, Skills, EmployeementHistory, ContactFreelancer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'address', 'phone')

class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        exclude = ('user','email', 'username',)

class HiredFreelancerForm(forms.ModelForm):
    class Meta:
        model = HiredFreelancer
        fields = ['full_name', 'job_title', 'job_requirement', 'delivery_date', 'project_price']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ('skill',)

class EmployeementHistoryForm(forms.ModelForm):
    class Meta:
        model = EmployeementHistory
        exclude = ('user',)

class ContactFreelancerForm(forms.ModelForm):
    class Meta:
        model = ContactFreelancer
        exclude = ('user',)