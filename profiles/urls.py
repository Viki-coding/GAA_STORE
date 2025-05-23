from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from profiles.forms import CustomLoginForm
from . import views

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
    path(
        'login/',
        LoginView.as_view(
            template_name='profiles/login.html',
            authentication_form=CustomLoginForm),
            name='login',
        ),
    ]
