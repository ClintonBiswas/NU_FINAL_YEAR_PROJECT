from django.urls import path
from .views import RegisterView, UserLoginView, LogoutView,AddBookView,NuQuestionAdd,AddProjectView,AddProgrammingContest,AddOurTeam

app_name = 'user'
urlpatterns = [
    path('register/', RegisterView, name='register'),
    path('login/', UserLoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('add-book/', AddBookView, name='add-book'),
    path('nu-question/', NuQuestionAdd, name='nu-question'),
    path('add-project/', AddProjectView, name='add-project'),
    path('add-contest/', AddProgrammingContest, name='add-contest'),
    path('add-team-member/', AddOurTeam, name='add-team'),
]
