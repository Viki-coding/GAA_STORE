from django.urls import path
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm
from . import views
from django.contrib import admin
from django.urls import path, include
from .views import login_signup_view


urlpatterns = [
    path('', views.profile, name='profile'),
    path('manage_addresses/', views.manage_addresses, name='manage_addresses'),
    path('add_address/', views.add_address, name='add_address'),
    path(
            'edit_address/<int:address_id>/',
            views.edit_address,
            name='edit_address'
        ),
    path(
        'delete_address/<int:address_id>/',
        views.delete_address,
        name='delete_address',
    ),
    path('login/', login_signup_view, name='login'),

    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]
