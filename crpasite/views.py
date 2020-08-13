from django.shortcuts import render, redirect, reverse
from .forms import ContactForm
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from products.models import Product
from django.contrib import messages

def home_page(request):
    context = {
        "latests": Product.objects.filter(active=True).order_by("-created_at")[0:6],
        "products": Product.objects.filter(active=True).order_by("created_at")[0:6],
        "featured": Product.objects.filter(active=True, featured=True)[0:6]
    }
    return render(request, "home.html", context)

def termandconds_page(request):
    return render(request, "termandconds.html", {})