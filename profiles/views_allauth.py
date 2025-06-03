from allauth.account.views import SignupView
from django.contrib.auth.forms import AuthenticationForm

class CombinedSignupView(SignupView):
    template_name = "account/combined.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = AuthenticationForm(self.request)
        return context
