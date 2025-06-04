from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import our two “combined” Allauth views
from profiles.views_allauth import CombinedLoginView, CombinedSignupView
from products import views as product_views 

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/login/",
        CombinedLoginView.as_view(),
        name="account_login",
    ),
    path(
        "accounts/signup/",
        CombinedSignupView.as_view(),
        name="account_signup",
    ),
    path("accounts/", include("allauth.urls")),


    path("", include("home.urls")),              
    path("profile/", include("profiles.urls")),
    path("hurleys/", include("products.urls")),
    path(
        "accessories/",
        product_views.accessories_shop,
        name="accessories_shop",
    ),
    path("bag/", include("bag.urls")),
    path("checkout/", include("checkout.urls")),
]


handler_404 = 'gaa_store.views.handle_404'
handler_500 = 'gaa_store.views.handle_500'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
