from django.urls import path
from .views import ProductListView, ProductDetailView, CreateProductView, upload

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("new/", CreateProductView.as_view(), name="create"),
    path("upload/", upload, name="upload"),
    path("detail/<slug:slug>/", ProductDetailView.as_view(), name="detail"),
]
