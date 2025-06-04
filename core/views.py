from django.shortcuts import render
from .models import FAQ


def faq_list(request):
    # Fetch all FAQs 
    faqs = FAQ.objects.all()
    return render(request, "core/faq_list.html", {"faqs": faqs})