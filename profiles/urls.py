from django.urls import path
from . import views


urlpatterns = [
    path("", views.profile, name="profile"),
    path("add_address/", views.add_address, name="add_address"),
    path(
        "edit_address/<int:address_id>/",
        views.edit_address,
        name="edit_address"
    ),
    path(
        "delete_address/<int:address_id>/",
        views.delete_address,
        name="delete_address"
    ),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
]
