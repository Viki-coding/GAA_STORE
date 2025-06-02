from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import ShippingAddress
from .models import Order


class CheckoutForm(forms.ModelForm):
    saved_address = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label="Select a saved address",
        empty_label="Use a new address",
    )
    full_name = forms.CharField(max_length=100, label="Full Name")
    email = forms.EmailField(label="Email Address")
    phone_number = forms.CharField(max_length=15, label="Phone Number")
    street_address1 = forms.CharField(max_length=255, label="Street Address 1")
    street_address2 = forms.CharField(
        max_length=255, required=False, label="Street Address 2 (Optional)")
    town_or_city = forms.CharField(max_length=100, label="Town or City")
    county = forms.CharField(max_length=100, label="County")
    eircode = forms.CharField(max_length=10, label="Eircode")
    store_shipping_address = forms.BooleanField(
        required=False, label="Save this shipping address for future use")
    create_user_profile = forms.BooleanField(
            required=False,
            label="Create a user profile for faster checkout next time"
        )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        label='Create Password'
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        label='Confirm Password'
    )
    
    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone_number', 
            'street_address1', 'street_address2',
            'town_or_city', 'county', 'eircode',
        ]


def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user', None)
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_class = 'form-horizontal'
    self.helper.field_class = 'col-12'
    self.helper.label_class = 'col-form-label'

    # Populate the saved_address field with the user's saved addresses
    if self.user and self.user.is_authenticated:
        self.fields['saved_address'].queryset = ShippingAddress.objects.filter(
            user_profile=self.user.userprofile
        )
    else:
        self.fields['saved_address'].queryset = ShippingAddress.objects.none()


def clean(self):
    cleaned_data = super().clean()
    create_user_profile = cleaned_data.get('create_user_profile')
    password = cleaned_data.get('password')
    password2 = cleaned_data.get('password2')

    # Only validate passwords if user wants to create a profile 
    # and is not logged in
    if create_user_profile and (
        not self.user or not self.user.is_authenticated
    ):
        if not password or not password2:
            raise forms.ValidationError(
                "Please enter and confirm your password."
            )
        if password != password2:
            raise forms.ValidationError("Passwords do not match.")
        if len(password) < 8:
            raise forms.ValidationError(
                "Password must be at least 8 characters long."
            )
    return cleaned_data


class ShippingAddressForm(forms.ModelForm):
    """
    Form for adding and editing shipping addresses.
    """
    class Meta:
        model = ShippingAddress
        fields = [
            'full_name', 'phone_number', 'street_address1', 'street_address2',
            'town_or_city', 'county', 'eircode', 'country', 'is_default'
        ]
        widgets = {
            'is_default': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}),
        }


