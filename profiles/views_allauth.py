from allauth.account.views import LoginView, SignupView
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse


class CombinedLoginView(LoginView):
    # Tell Allauth to use our single template instead of account/login.html
    template_name = "profiles/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = context.pop("form")
        context["signup_form"] = SignupForm(self.request.POST or None)

        return context
  
    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            # If the logged-in user is staff, send them to /faq/ immediately:
            return reverse("faq_list")
        # Otherwise, default to normal Allauth behavior (i.e. ACCOUNT_LOGIN_REDIRECT_URL)
        return super().get_success_url()


class CombinedSignupView(SignupView):
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
