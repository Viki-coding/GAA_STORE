from django.db import models
from django.utils import timezone


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    sort_order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Lower numbers appear first"
    )

    class Meta:
        ordering = ["sort_order", "question"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class ContactMessage(models.Model):
    """
    Capture messages sent by visitors:
      - name, email, subject, body, timestamp
      - “is_read” flag can be managed in admin
    """
    name = models.CharField(max_length=100, help_text="Your full name")
    email = models.EmailField(help_text="Your email address")
    subject = models.CharField(
        max_length=150, blank=True, help_text="Short subject line")
    body = models.TextField(help_text="What would you like to ask us?")
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(
        default=False, help_text="Mark True once message is handled")

    def __str__(self):
        return f"[{self.timestamp.strftime(
            '%Y-%m-%d %H:%M')}] {self.name} – {self.subject or 'No Subject'}"

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Contact Message"
