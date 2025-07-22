from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactMessageForm, FAQForm
from django.http import HttpResponse

from .models import FAQ


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
    success_url = reverse_lazy("core:faq_list")


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name="dispatch")
class FaqUpdateView(UpdateView):
    """
    Only staff/superuser can edit an existing FAQ.
    """
    model = FAQ
    form_class = FAQForm
    template_name = "core/faq_form.html"
    success_url = reverse_lazy("core:faq_list")


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_member_required, name="dispatch")
class FaqDeleteView(DeleteView):
    """
    Only staff/superuser can delete an FAQ.
    """
    model = FAQ
    template_name = "core/faq_confirm_delete.html"
    success_url = reverse_lazy("core:faq_list")


def contact_us(request):
    """
    Display a “Contact Us” form and save the message when submitted.
    """
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been sent.")
            return redirect("core:contact_us")
    else:
        form = ContactMessageForm()

    return render(request, "core/contact_us.html", {"form": form})


def privacy_policy(request):
    return render(request, "core/privacy_policy.html")


def sitemap_view(request):
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://gaastore-2f38a7e53edc.herokuapp.com/</loc>
    <lastmod>2025-06-11T07:42:53+00:00</lastmod>
    <priority>1.00</priority>
  </url>
</urlset>'''
    return HttpResponse(xml_content, content_type="application/xml")


def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Disallow: /profile/\n"
        "Disallow: /checkout/\n"
        "\n"
        "Sitemap: https://gaastore-2f38a7e53edc.herokuapp.com/sitemap.xml\n"
    )
    return HttpResponse(content, content_type="text/plain")
