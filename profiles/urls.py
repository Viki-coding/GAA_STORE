from django.urls import path
from .views import (
    login_signup_view,
    profile,
    add_address,
    edit_address,
    delete_address,
    order_detail,
)


urlpatterns = [
    path('login/', login_signup_view, name='login'),
    path('', profile, name='profile'),
    path('add_address/', add_address, name='add_address'),
    path(
            'edit_address/<int:address_id>/',
            edit_address,
            name='edit_address'
        ),
    path(
        'delete_address/<int:address_id>/',
        delete_address,
        name='delete_address',
    ),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
]
