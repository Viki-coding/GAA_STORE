from django import forms
from crispy_forms.helper import FormHelper
from .models import ShippingAddress, Order
from django_countries.fields import CountryField
from django.core.validators import RegexValidator


class CheckoutForm(forms.ModelForm):
    saved_address = forms.ModelChoiceField(
        queryset=ShippingAddress.objects.none(),
        required=False,
        label="Select a saved address",
        empty_label="Use a new address",
    )
    full_name = forms.CharField(
        max_length=100,
        label="Full Name",
        widget=forms.TextInput(attrs={'autocomplete': 'name'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    phone_number = forms.CharField(
        max_length=15,
        label="Phone Number",
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9\s\-]{7,15}$',
                message="Enter a valid phone number (digits, spaces, dashes, and optional leading +)."
            )
        ],
        widget=forms.TextInput(attrs={'autocomplete': 'tel', 'inputmode': 'tel', 'pattern': r'^\+?[0-9\s\-]{7,15}$'})
    )
    street_address1 = forms.CharField(
        max_length=255,
        label="Street Address 1",
        widget=forms.TextInput(attrs={'autocomplete': 'address-line1'})
    )
    street_address2 = forms.CharField(
        max_length=255,
        required=False,
        label="Street Address 2",
        widget=forms.TextInput(attrs={'autocomplete': 'address-line2'})
    )
    town_or_city = forms.CharField(
        max_length=100,
        label="Town or City",
        widget=forms.TextInput(attrs={'autocomplete': 'address-level2'})
    )
    county = forms.CharField(
        max_length=100,
        label="County",
        widget=forms.TextInput(attrs={'autocomplete': 'address-level1'})
    )
    eircode = forms.CharField(
        max_length=10,
        label="Eircode",
        widget=forms.TextInput(attrs={'autocomplete': 'postal-code'})
    )
    country = CountryField(
        blank_label="Country *",
        default='IE'  # Default to Ireland (ISO code 'IE')
    ).formfield(
        required=True,
        widget=forms.Select(
            attrs={
                'autocomplete': 'country',
                'class': 'form-control'
            }
        )
    )
    store_shipping_address = forms.BooleanField(
        required=False,
        label="Save this shipping address for future use",
        widget=forms.CheckboxInput(attrs={'autocomplete': 'off'})
    )
    create_user_profile = forms.BooleanField(
        required=False,
        label="Create a user profile for faster checkout next time",
        widget=forms.CheckboxInput(attrs={'autocomplete': 'off'})
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
    is_gift = forms.BooleanField(
        required=False,
        label="This is a gift",
        widget=forms.CheckboxInput(attrs={'autocomplete': 'off'})
    )
    gift_message = forms.CharField(
        required=False,
        label="Gift Message (optional)",
        max_length=255,
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Write a short message…'}
        )
    )

    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'county', 'eircode',
            'is_gift', 'gift_message',
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
            self.fields['saved_address'].queryset = ShippingAddress.objects.\
                filter(
                user_profile=self.user.userprofile
            )
        else:
            self.fields['saved_address'].queryset = ShippingAddress.objects.\
                none()

    def clean(self):
        cleaned_data = super().clean()
        saved = cleaned_data.get('saved_address')

        # If user chose an existing address, skip "new address" validation
        if saved:
            # remove any errors on the new‐address fields
            for field in [
                'full_name', 'street_address1', 'town_or_city',
                'county', 'eircode', 'country'
            ]:
                if field in self._errors:
                    del self._errors[field]
            return cleaned_data

        # Otherwise, ensure all required address fields are present
        missing = []
        for field in [
            'full_name',
            'street_address1',
            'town_or_city',
            'county',
            'eircode',
            'country'
        ]:
            if not cleaned_data.get(field):
                missing.append(field)
        if missing:
            raise forms.ValidationError(
                (
                    "Please fill in all shipping address fields or "
                    "choose a saved address."
                )
            )

        # Password logic (only if creating a profile)
        create_profile = cleaned_data.get('create_user_profile')
        pwd1 = cleaned_data.get('password')
        pwd2 = cleaned_data.get('password2')
        if create_profile and (
            not self.user or not self.user.is_authenticated
        ):
            if not pwd1 or not pwd2:
                raise forms.ValidationError(
                    "Please enter and confirm your password.")
            if pwd1 != pwd2:
                raise forms.ValidationError("Passwords do not match.")
            if len(pwd1) < 8:
                raise forms.ValidationError(
                    "Password must be at least 8 characters long.")

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
            'full_name': forms.TextInput(attrs={'autocomplete': 'name'}),
            'phone_number': forms.TextInput(attrs={'autocomplete': 'tel'}),
            'street_address1': forms.TextInput(
                attrs={'autocomplete': 'address-line1'}
            ),
            'street_address2': forms.TextInput(
                attrs={'autocomplete': 'address-line2'}
            ),
            'town_or_city': forms.TextInput(
                attrs={'autocomplete': 'address-level2'}
            ),
            'county': forms.TextInput(
                attrs={'autocomplete': 'address-level1'}
            ),
            'eircode': forms.TextInput(attrs={'autocomplete': 'postal-code'}),
            'country': forms.Select(attrs={'autocomplete': 'country'}),
            'is_default': forms.CheckboxInput(attrs={'autocomplete': 'off'}),
        }
