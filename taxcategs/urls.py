from django.urls import path
from .views import CategoriesListView, CategoryDetailView
from django.contrib.auth.views import LogoutView

app_name = "taxcategs"

urlpatterns = [
    path('navigate/', CategoriesListView.as_view(), name="list"),
    path('proposal/', CategoryDetailView.as_view(), name="register"),
    path('review/', LogoutView.as_view(), name="review"),
]