from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail',
    ),
    path('hurleys/', views.hurleys_shop, name='hurleys_shop'),
]