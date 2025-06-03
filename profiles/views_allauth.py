from allauth.account.views import SignupView
from django.contrib.auth.forms import AuthenticationForm

class CombinedSignupView(SignupView):
    """
    When someone hits /accounts/signup/, use Allauths logic to build the signup form (self.get_form()),
    but also create an AuthenticationForm and stick it into the context as 'login_form'.
    """

    def get_context_data(self, **kwargs):
        # Let Allauth build the usual context (which has 'form' = signup_form)
        context = super().get_context_data(**kwargs)

        # Add 'login_form' into the context
        # so that 'profiles/login.html' can do {{ login_form.username }} etc.
        context['login_form'] = AuthenticationForm(self.request)

        return context
