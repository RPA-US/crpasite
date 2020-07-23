from django.shortcuts import render
from django.views.generic import ListView, DetailView

# Create your views here.

class CategoriesListView(ListView):
    queryset = Category.objects.all()
    template_name = "categories/list.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(CategoryListView, self).get_context_data()
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    template_name = "Categorys/detail.html"
from django.views.generic import ListView, DetailView
from .models import Category
from products.models import Product


class CategoryListView(ListView):
    queryset = Category.objects.all()
    template_name = "Categorys/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryListView, self).get_context_data()
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
        return context


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
        return context

    template_name = "categories/detail.html"
