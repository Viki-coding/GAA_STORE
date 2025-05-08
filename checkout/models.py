import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from products.models import Product
from profiles.models import UserProfile
from django_countries.fields import CountryField


class ShippingAddress(models.Model):
    """
    Stores shipping addresses for users.
    """
    user_profile = models.ForeignKey(
            UserProfile, 
            on_delete=models.CASCADE,
            related_name='shipping_addresses'
        )
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    street_address1 = models.CharField(max_length=80)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40)
    county = models.CharField(max_length=80, null=True, blank=True)
    eircode = models.CharField(max_length=10)
    country = CountryField(blank_label='Country *', default='IE')

    def __str__(self):
        return f"{self.full_name} - {self.eircode}"


class Order(models.Model):
    """
    Represents an order placed by a user, 
    including saved shipping addresses and gift functionality.
    """
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(
        ShippingAddress, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.EmailField(null=False, blank=False) 
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20, choices=[
            ('cart', 'In Cart'),
            ('Pending', 'Pending'),
            ('Processing', 'Processing'),
            ('Shipped', 'Shipped'),
            ('Delivered', 'Delivered'),],
        default='Pending')
    payment_status = models.CharField(
        max_length=20, choices=[
            ('Pending', 'Pending'),
            ('Paid', 'Paid'),
            ('failed', 'Failed'),
            ('Refunded', 'Refunded')],
        default='Pending')
    delivery_status = models.CharField(max_length=50, null=True, blank=True)
    is_gift = models.BooleanField(
        default=False, help_text="Indicates if the order is a gift.")
    gift_message = models.CharField(
        max_length=255, 
        null=True, blank=True, help_text="Optional gift message.")
    delivery_cost = models.DecimalField(
         max_digits=6, decimal_places=2, default=0)
    grand_total = models.DecimalField(
         max_digits=10, decimal_places=2, default=0)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID.
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Recalculate grand total, including delivery cost.
        """
        self.total_price = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.total_price < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = (
                self.total_price * settings.STANDARD_DELIVERY_PERCENTAGE
                / 100
            )
        else:
            self.delivery_cost = 0
        self.grand_total = self.total_price + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Ensure order number is set before saving.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)


class Meta:
    verbose_name = "Order"
    verbose_name_plural = "Orders"


class OrderItem(models.Model):
    """
    Represents an item in an order, including product details and quantity.
    """
    order = models.ForeignKey(
         Order, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_at_time = models.DecimalField(
         max_digits=10, decimal_places=2, null=True)
    is_gift = models.BooleanField(default=False)
    gift_message = models.CharField(max_length=255, null=True, blank=True)
    lineitem_total = models.DecimalField(
         max_digits=6, decimal_places=2, default=0, editable=False)

    def save(self, *args, **kwargs):
        """Calculate line item total before saving."""
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} in order {self.order.order_number}'
