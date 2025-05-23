from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class CustomLoginForm(AuthenticationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}),
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}),
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                # Map email to username
                self.cleaned_data['username'] = user.username
            except User.DoesNotExist:
                raise forms.ValidationError("No user with this email exists.")
        return cleaned_data
