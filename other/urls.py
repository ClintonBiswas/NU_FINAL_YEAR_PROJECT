from django.urls import path
from .views import Home, RefBooksView, NuQuestionView, ProgrammingContestView, ProductView, SearchView, projectDetails, ProductDetailsView, CategoryProductView, YourOrder, OrderPlaceView, UpdateProfileView, ProfileView

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
]