from django import forms
from .models import Product
from taxcategs import models as tax_categ

class ProductForm(forms.Form):
    title = forms.CharField(
        label="Title",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Title"}
        ),
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Description"}
        ),
    )
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Price"})
    )
    image = forms.ImageField(
        label = "Image",
        widget = forms.FileInput(attrs={"class": "form-control", "placeholder": "Image"})
    )
    featured = forms.BooleanField(
        label="Featured",
        widget=forms.CheckboxInput(
            attrs={"class": "primary-checkbox", "checked": "checked"}
        ),
    )
    active = forms.BooleanField(
        label="Active",
        widget=forms.CheckboxInput(
            attrs={"class": "primary-checkbox", "checked": "checked"}
        ),
    )
    # categories = forms.ModelMultipleChoiceField(queryset=tax_categ.CategoryTerm.objects.all().filter(active=True, is_tax_categ=True))
    categories = forms.ModelMultipleChoiceField(queryset=tax_categ.TaxCateg.objects.all(), widget = forms.SelectMultiple(attrs={"class": "form-control"}))

    def clean(self):
        data = self.cleaned_data
        title = data.get("title")
        qs = Product.objects.filter(title=title)
        if qs.exists():
            raise forms.ValidationError("Title is taken")
        return data
