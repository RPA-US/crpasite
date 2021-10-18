from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_page, termandconds_page
from taxcategs.views import taxonomy_view


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        # path("", home_page, name="home_url"),
        path("", taxonomy_view, name="categoryterm_list"),
        path("termandconds", termandconds_page, name="termandconds_url"),
        path("accounts/", include("accounts.urls")),
        path("products/", include("products.urls"), name="products"),
        path("addresses/", include("addresses.urls")),
        path("cart/", include("carts.urls")),
        path("search/", include("search.urls")),
        path("categories/", include("taxcategs.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

