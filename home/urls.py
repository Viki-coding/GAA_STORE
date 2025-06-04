from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home/index.html'), name='home'),
    path('products/', include('products.urls'), name='products'),
    path('how-to-measure/', views.how_to_measure, name='how_to_measure'),
]
