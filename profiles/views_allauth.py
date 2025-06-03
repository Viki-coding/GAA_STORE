from allauth.account.views import LoginView, SignupView
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm


class CombinedLoginView(LoginView):
    """
    When GET /accounts/login/, show both:
      • login_form (AuthenticationForm),
      • signup_form (fresh SignupForm),
    in the same template.
    When POST /accounts/login/ (user tries to log in), Validation happens as usual;
    if login fails, 'form' (the invalid AuthenticationForm) appears in context,
    so we copy it into 'login_form'. Meanwhile we still supply a fresh 'signup_form'.
    """

    # Tell Allauth to use our single template instead of account/login.html
    template_name = "profiles/login.html"

    def get_context_data(self, **kwargs):
        # 1) Let Allauth build the normal context → context["form"] = AuthenticationForm(POST data or empty)
        context = super().get_context_data(**kwargs)

        # 2) Allauth puts its AuthenticationForm (valid or with login errors) into context["form"].
        #    We want to rename that into `login_form` so our template can refer to login_form.username, etc.
        context["login_form"] = context.pop("form")

        # 3) Always provide a fresh signup_form for the “Sign Up” card.
        #    (On GET, it's brand new; on a failed POST to /accounts/login/, signup_form is still fresh.)
        context["signup_form"] = SignupForm(self.request.POST or None)

        return context


class CombinedSignupView(SignupView):
    """
    When GET /accounts/signup/, show both:
      • signup_form (fresh SignupForm),
      • login_form (fresh AuthenticationForm),
    in the same template.
    When POST /accounts/signup/ (user tries to register), Allauth validates the posted data:
      • If invalid (e.g. password too short), Allauth puts the invalid form into context["form"].
    We then copy that invalid form into 'signup_form' so errors appear under the correct fields.
    We also supply a fresh login_form.
    """

    # Tell Allauth to use our single template instead of account/signup.html
    template_name = "profiles/login.html"

    def get_context_data(self, **kwargs):
        # 1) Let Allauth build its normal context → context["form"] = SignupForm(POST data or empty)
        context = super().get_context_data(**kwargs)

        # 2) Allauth has placed its signup_form (valid or with errors) into context["form"].
        #    Copy that into 'signup_form' so our template can do signup_form.password1.errors, etc.
        context["signup_form"] = context.pop("form")

        # 3) Always provide a fresh login_form for the “Log In” card.
        context["login_form"] = AuthenticationForm(self.request)

        return context
