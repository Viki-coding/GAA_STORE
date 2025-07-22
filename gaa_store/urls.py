from django.contrib import admin
from django.urls import path, include
from products import views as product_views

from django.conf import settings
from django.conf.urls.static import static
from profiles.views_allauth import CombinedLoginView, CombinedSignupView
from core import views as core_views


urlpatterns = [
    path("admin/", admin.site.urls),

    # allauth
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

    path("hurleys/", product_views.hurleys_shop, name="hurleys_root_shop"),
    path(
        "accessories/",
        product_views.accessories_shop,
        name="accessories_root_shop",
    ),


    # home, products, profiles, bag, checkout, etc.
    path("products/", include("products.urls", namespace="products")),
    path("profile/", include("profiles.urls")),
    path("bag/",     include("bag.urls")),
    path("checkout/", include("checkout.urls")),
    path("privacy-policy/", core_views.privacy_policy, name="privacy_policy"),
    path("faq/", include(("core.urls", "core"), namespace="core")),
    path("", include("home.urls")),
    path("sitemap.xml", core_views.sitemap_view, name="sitemap"),
    path("robots.txt", core_views.robots_txt, name="robots_txt"),
]


handler_404 = 'gaa_store.views.handle_404'
handler_500 = 'gaa_store.views.handle_500'

if settings.DEBUG:
    # serve uploaded media files in debug
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
