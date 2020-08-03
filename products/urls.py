from django.urls import path
from .views import ProductListView, ProductDetailView, register_product

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("new/", register_product, name="create"),
    path("detail/<slug:slug>/", ProductDetailView.as_view(), name="detail"),
]
