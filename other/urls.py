from django.urls import path
from .views import Home, RefBooksView, NuQuestionView, ProgrammingContestView, ProductView, SearchView, projectDetails, ProductDetailsView, CategoryProductView, YourOrder, OrderPlaceView, UpdateProfileView, ProfileView, ExpertCreateView, OurExpertView, ExpertProfileView, hire_freelancer_view, ExpertProfileSkill, ExpertProfileSkillUpdate, EmployementHistoryView, EmployementHistoryUpdate, ExpertProfileUpdate, ExpertCategoryView, ContactWithMeView

app_name = 'other'
urlpatterns = [
    path('', Home, name='home'),
    path('search/', SearchView, name='search'),
    path('ref-books/', RefBooksView, name='ref-books'),
    path('project-details/<slug:slug>/',projectDetails, name='project_details'),
    path('nu-questions/', NuQuestionView, name='nu-questions'),
    path('programming-contest/', ProgrammingContestView, name='programming-contest'),
    path('product/', ProductView, name='product'),
    path('product/<slug:slug>/', ProductDetailsView, name='product-detail'),
    path('category-product/<int:pk>/',CategoryProductView, name='category-product'),
    path('order-item/<slug:slug>/', YourOrder, name='order-item'),
    path('profile/', ProfileView, name='profile'),
    #path('confirm-order/<slug:slug>/', ConfirmOrder, name='confirm-order'),
    path('order-place/<slug:slug>/', OrderPlaceView, name='order-place'),
    path('update_profile/', UpdateProfileView, name='update_profile'),
    # expert section url
    path('create-expert-profile/', ExpertCreateView, name='create-expert-profile'),
    path('expert-profile/', OurExpertView, name='expert-profile'),
    path('freelance-profile/<int:pk>/', ExpertProfileView, name='freelance-profile'),
    path('freelance-update-profile/<int:pk>/', ExpertProfileUpdate, name='freelance-update-profile'),
    path('expert-category/<slug:slug>/', ExpertCategoryView, name='expert-category'),
    path('hire-freelancer/<int:pk>/', hire_freelancer_view, name='hire_freelancer'),
    path('contact-freelancer/<int:pk>/', ContactWithMeView, name='contact-freelancer'),
    path('add-skill/<int:pk>/', ExpertProfileSkill, name='add-skill'),
    path('update-skill/<int:pk>/', ExpertProfileSkillUpdate, name='update-skill'),
    path('add-employement/<int:pk>/', EmployementHistoryView, name='add-employement'),
    path('update-employement/<int:pk>/', EmployementHistoryUpdate, name='update-employement'),
]