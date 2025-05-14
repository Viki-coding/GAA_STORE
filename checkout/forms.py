from django import forms


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, label="Full Name")
    email = forms.EmailField(label="Email Address")
    phone_number = forms.CharField(max_length=15, label="Phone Number")
    street_address1 = forms.CharField(max_length=255, label="Street Address 1")
    street_address2 = forms.CharField(max_length=255, required=False, label="Street Address 2 (Optional)")
    town_or_city = forms.CharField(max_length=100, label="Town or City")
    county = forms.CharField(max_length=100, label="County")
    eircode = forms.CharField(max_length=10, label="Eircode")
    store_shipping_address = forms.BooleanField(required=False, label="Save this shipping address for future use")
    create_user_profile = forms.BooleanField(required=False, label="Create a user profile for faster checkout next time")