from django.contrib import admin
from .models import FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "sort_order")
    list_editable = ("sort_order",)
    search_fields = ("question", "answer")
    list_per_page = 20