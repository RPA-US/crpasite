from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import TaxCateg

# Create your views here.
class CategoriesListView(ListView):
    queryset = TaxCateg.objects.all()
    template_name = "categories/list.html"


class CategoryDetailView(DetailView):
    model = TaxCateg
    template_name = "categories/detail.html"