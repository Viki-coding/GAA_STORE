# from django.contrib import admin
# from django.urls import path, include
# from products import views as product_views
# from profiles.views_allauth import CombinedLoginView, CombinedSignupView
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path(
#         "accounts/login/",
#         CombinedLoginView.as_view(),
#         name="account_login",
#     ),
#     path(
#         "accounts/signup/",
#         CombinedSignupView.as_view(),
#         name="account_signup",
#     ),
#     path("accounts/", include("allauth.urls")),
#     path("", include("home.urls")),
#     path("profile/", include("profiles.urls")),
#     path("hurleys/", include("products.urls")),
#     path(
#         "accessories/",
#         product_views.accessories_shop,
#         name="accessories_shop",
#     ),
#     path("bag/", include("bag.urls")),
#     path("checkout/", include("checkout.urls")),
#     path("privacy-policy/", include("core.urls")),
#     path("faq/", include("core.urls")),

# ]


# handler_404 = 'gaa_store.views.handle_404'
# # handler_500 = 'gaa_store.views.handle_500'

# if settings.DEBUG:
#     urlpatterns += static(
#         settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

from django.contrib import admin
from django.urls import path, include
from products import views as product_views
from profiles.views_allauth import CombinedLoginView, CombinedSignupView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # -- allauth --
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

    # -- home & profiles --
    path("", include("home.urls")),
    path("profile/", include("profiles.urls")),

    # -- product catalog --
    path("", product_views.product_list, name="product_list"),
    path("product/<int:product_id>/", product_views.product_detail, name="product_detail"),

    # -- hurleys shop & detail --
    path("hurleys/", product_views.hurleys_shop, name="hurleys_shop"),
    path("hurleys/<int:hurley_id>/", product_views.hurley_detail, name="hurley_detail"),

    # -- accessories shop --
    path("accessories/", product_views.accessories_shop, name="accessories_shop"),
    path("grip/<int:grip_id>/", product_views.grip_detail, name="grip_detail"),
    path("sliotar/<int:sliotar_id>/", product_views.sliotar_detail, name="sliotar_detail"),
    path("helmet/<int:helmet_id>/", product_views.helmet_detail, name="helmet_detail"),

    # -- bag, checkout, etc --
    path("bag/", include("bag.urls")),
    path("checkout/", include("checkout.urls")),
    path("privacy-policy/", include("core.urls")),
    path("faq/", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

