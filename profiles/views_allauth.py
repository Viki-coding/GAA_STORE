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

        # Debugging: Print the request method and POST data
        print(f"Request method: {self.request.method}")
        print(f"POST data: {self.request.POST}")

        return context

    def get_success_url(self):
        user = self.request.user

        # Debugging: Print the user authentication status
        print(f"User authenticated: {user.is_authenticated}")
        print(f"User is staff: {user.is_staff}")

        # Always redirect staff to FAQ, regardless of 'next'
        if user.is_authenticated and user.is_staff:
            print("Redirecting staff to FAQ...")
            return reverse("faq")

        # Debugging: Print the next parameter from POST or GET
        next_url = self.request.POST.get("next") or self.request.GET.get("next")
        print(f"Next URL parameter: {next_url}")

        if next_url:
            print(f"Redirecting to next URL: {next_url}")
            return next_url

        print("Redirecting to profile...")
        return reverse("profile")
    
    
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
