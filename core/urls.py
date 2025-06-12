from django.urls import path
from .views import (
    FaqListView,
    FaqCreateView,
    FaqUpdateView,
    FaqDeleteView
)
from .views import contact_us
from .views import privacy_policy

app_name = "core"

urlpatterns = [
    path("", FaqListView.as_view(), name="faq_list"),
    path("add/", FaqCreateView.as_view(), name="faq_add"),
    path("edit/<int:pk>/", FaqUpdateView.as_view(), name="faq_edit"),
    path("delete/<int:pk>/", FaqDeleteView.as_view(), name="faq_delete"),
    path("contact/", contact_us, name="contact_us"),
    path("privacy-policy/", privacy_policy, name="privacy_policy"),
]
