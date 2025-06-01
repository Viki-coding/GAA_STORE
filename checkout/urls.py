from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path(
        'checkout_success/<order_number>/',
        views.checkout_success,
        name='checkout_success',
    ),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]
