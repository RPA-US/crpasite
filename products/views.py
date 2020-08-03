from django.views.generic import ListView, DetailView
from .models import Product
from carts.models import Cart
from .forms import ProductForm
from django.shortcuts import render

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data()
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
        return context

    template_name = "products/detail.html"



def register_product(request):
    form = ProductForm(request.POST or None)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
    
    if form.is_valid():
        data = form.cleaned_data
        # Checking: user must be a Provider
        if request.user.role == 2:
            slug = data.get("slug")
            title = data.get("title")
            description = data.get("description")
            price = data.get("price")
            image = data.get("image")
            is_featured = data.get("is_featured")
            is_active = data.get("is_active")
            categories = form.data.get("categories")
            new_prod = Product.create_product(
                title,
                slug,
                description,
                price,
                image,
                is_featured,
                is_active,
                categories,
            )
        else:
            new_prod = None
        if new_prod is not None:
            messages.success(request, "Created Product.")
            return reverse("products:detail", kwargs={"slug": self.slug})

        messages.warning(request, "Create Error !")

    context = {"form": form}

    return render(request, "products/create.html", context)