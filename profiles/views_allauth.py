from allauth.account.views import LoginView, SignupView
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm


class CombinedLoginView(LoginView):
    # Tell Allauth’s LoginView to render “profiles/login.html” instead of the default “account/login.html”
    template_name = "profiles/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Allauth’s LoginView normally puts its AuthenticationForm into context as “form.”
        # We also want to supply a fresh signup form, so that our combined template’s “Sign Up” block
        # can render “signup_form.*” fields if someone clicks “Sign Up” on the same page.
        context["signup_form"] = SignupForm(self.request.POST or None)
        return context


class CombinedSignupView(SignupView):
    # Similarly, override Allauth’s SignupView so it also uses the same “profiles/login.html” template
    template_name = "profiles/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Allauth’s SignupView usually puts its SignupForm into context as “form.”
        # We also want to supply a fresh login form, so that our combined template’s “Log In” block
        # can render “form.login” and “form.password” if someone clicks “Log In” on the same page.
        context["login_form"] = AuthenticationForm(self.request)
        return context
