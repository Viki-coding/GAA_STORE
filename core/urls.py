from django.urls import path
from .views import (
    FaqListView, 
    FaqCreateView, 
    FaqUpdateView, 
    FaqDeleteView
)


urlpatterns = [
    path("", FaqListView.as_view(), name="faq_list"),
    path("add/", FaqCreateView.as_view(), name="faq_add"),
    path("edit/<int:pk>/", FaqUpdateView.as_view(), name="faq_edit"),
    path("delete/<int:pk>/", FaqDeleteView.as_view(), name="faq_delete"),
]
