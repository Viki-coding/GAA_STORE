from django.contrib import admin
from django.urls import path, include
from products import views as product_views

from django.conf import settings
from django.conf.urls.static import static
from profiles.views_allauth import CombinedLoginView, CombinedSignupView


urlpatterns = [
    path("admin/", admin.site.urls),

    # allauth
    path("accounts/login/",  CombinedLoginView.as_view(),  name="account_login"),
    path("accounts/signup/", CombinedSignupView.as_view(), name="account_signup"),
    path("accounts/", include("allauth.urls")),

    # home, products, profiles, bag, checkout, etc.
    path("", include("home.urls")),
    path("", include("products.urls", namespace="products")),
    path("profile/", include("profiles.urls")),
    path("bag/",     include("bag.urls")),
    path("checkout/", include("checkout.urls")),
    path("privacy-policy/", include("core.urls")),
    path("faq/", include("core.urls")),
]


handler_404 = 'gaa_store.views.handle_404'
handler_500 = 'gaa_store.views.handle_500'

if settings.DEBUG:
    # serve uploaded media files in debug
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
