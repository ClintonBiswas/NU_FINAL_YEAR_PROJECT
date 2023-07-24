from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import RefBooks, NuQuestion, AddProjects, ProgrammingContest, OurTeam

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class NuQuestionForm(forms.ModelForm):
    class Meta:
        model = NuQuestion
        fields = ['subject_name', 'question_year', 'question_type', 'question_image']

class RefBooksForm(forms.ModelForm):
    class Meta:
        model = RefBooks
        fields = ['book_name', 'bio', 'cover_photo', 'pdf']

class AddProjectsForm(forms.ModelForm):
    class Meta:
        model = AddProjects
        fields = ['title', 'bio', 'image', 'live_demo', 'github_code']

class ProgrammingContestForm(forms.ModelForm):
    class Meta:
        model = ProgrammingContest
        fields = ['contest_name', 'organization_name', 'duration', 'join_link']

class OurTeamForm(forms.ModelForm):
    class Meta:
        model = OurTeam
        fields = ['name', 'bio', 'photo',]