from django.urls import path
from . import views
from checkout import views as checkout_views


urlpatterns = [
    path('', views.checkout, name='checkout'),
    path(
        'checkout_success/<order_number>/',
        views.checkout_success,
        name='checkout_success',
    ),
    path('checkout/wh/', checkout_views.stripe_webhook, name='stripe_webhook'),
]
