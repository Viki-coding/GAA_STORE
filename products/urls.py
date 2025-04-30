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
    path('accessories/', views.accessories_shop, name='accessories_shop'),
    path(
        'hurley/<int:hurley_id>/',
        views.hurley_detail,
        name='hurley_detail',
    ),
    path('add/<int:product_id>/', views.add_to_bag, name='add_to_bag'),
]
