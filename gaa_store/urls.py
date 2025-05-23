"""gaa_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views
from django.contrib.auth.views import LoginView
from profiles.forms import CustomLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('profiles/', include('profiles.urls')),
    path('hurleys/', views.hurleys_shop, name='hurleys_shop'),
    path('products/', include('products.urls')),
    path('bag/', include('bag.urls')),
    path('accessories/', views.accessories_shop, name='accessories_shop'),
    path('checkout/', include('checkout.urls')),
    path(
        'login/',
        LoginView.as_view(
            template_name='profiles/login.html',
            authentication_form=CustomLoginForm
        ),
        name='login',
    ),
]

HANDLER_404 = 'gaa_store.views.handle_404'
HANDLER_500 = 'gaa_store.views.handle_500'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
