from django.db import models


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
