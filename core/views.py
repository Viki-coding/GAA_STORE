from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import FAQ
from .forms import FAQForm


class FaqListView(ListView):
    """
    Anyone can view the FAQ list.
    """
    model = FAQ
    template_name = "core/faq_list.html"
    context_object_name = "faqs"


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name="dispatch")
class FaqCreateView(CreateView):
    """
    Only staff/superuser can create a new FAQ.
    """
    model = FAQ
    form_class = FAQForm
    template_name = "core/faq_form.html"
    success_url = reverse_lazy("faq_list")


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name="dispatch")
class FaqUpdateView(UpdateView):
    """
    Only staff/superuser can edit an existing FAQ.
    """
    model = FAQ
    form_class = FAQForm
    template_name = "core/faq_form.html"
    success_url = reverse_lazy("faq_list")


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name="dispatch")
class FaqDeleteView(DeleteView):
    """
    Only staff/superuser can delete an FAQ.
    """
    model = FAQ
    template_name = "core/faq_confirm_delete.html"
    success_url = reverse_lazy("faq_list")
