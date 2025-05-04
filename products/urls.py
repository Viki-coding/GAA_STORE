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
    path(
        'grip/<int:grip_id>/',
        views.grip_detail,
        name='grip_detail',
    ),
    path(
        'sliotar/<int:sliotar_id>/',
        views.sliotar_detail,
        name='sliotar_detail',
    ),
    path(
        'helmet/<int:helmet_id>/',
        views.helmet_detail,
        name='helmet_detail',
    ),
]
