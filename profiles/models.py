from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True)
    default_country = CountryField(
        blank_label='Country *',
        null=True,
        blank=True,
        default='IE'  # ISO 3166-1 alpha-2 code for Ireland)
    )
    default_eircode = models.CharField(max_length=10, null=True, blank=True)
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True)
    default_street_address1 = models.CharField(
        max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(
        max_length=80, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.user.email}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ['-joined_date']


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            instance.userprofile.save()
        except Exception as e:
            # Log the exception or handle it appropriately
            print(f"Error creating/updating user profile: {e}")


class ShippingAddress(models.Model):
    """
    Model to store multiple shipping addresses for a user.
    """
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="shipping_addresses",
    )
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    street_address1 = models.CharField(max_length=80)
    street_address2 = models.CharField(max_length=80, blank=True)
    town_or_city = models.CharField(max_length=40)
    county = models.CharField(max_length=80)
    eircode = models.CharField(max_length=10, blank=True)
    country = CountryField(
        blank_label="Country *", default="IE")  # Default to Ireland
    is_default = models.BooleanField(default=False)  # Mark as default address
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.street_address1}, {
            self.town_or_city}, {self.country}"

    class Meta:
        ordering = ["-is_default", "-date_added"]  # Default add 1st
