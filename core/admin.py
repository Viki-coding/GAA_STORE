from django.contrib import admin
from .models import FAQ
from .models import ContactMessage


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "sort_order")
    list_editable = ("sort_order",)
    search_fields = ("question", "answer")
    list_per_page = 20


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "timestamp", "is_read")
    list_filter = ("is_read", "timestamp")
    search_fields = ("name", "email", "subject", "body")
    readonly_fields = ("timestamp",)
    ordering = ("-timestamp",)
