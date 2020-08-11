from django.db import models
from accounts.models import User as UserModel
from categories.models import CategoryBase
from enum import Enum
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
import os
import random

# Create your models here.
class TaxCateg(CategoryBase):
    """
    The category term that stands as the representative of the others.
    """

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Taxonomic category"
        verbose_name_plural = "Taxonomic categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("taxcategs:taxcategory_detail", kwargs={"pk": self.pk})
    
    def clean(self):
        categ_terms = CategoryTerm.objects.filter(
            tax_categ=self, is_tax_categ=True, active=True
        )
        if len(categ_terms) != 1:
            raise ValidationError(
                "A taxonomic category always has to have at least one associated category term"
            )
        if not (categ_terms[0].term == self.name):
            raise ValidationError(
                "A taxonomic category must always have the same name as its category term"
            )


class KnowledgeSource(models.Model):
    """
    Knowledge source where the information that users relies on when writing a proposal, comes from.
    """

    name = models.CharField(max_length=50)
    url = models.URLField(max_length=200, blank=True)
    creator = models.ForeignKey(
        UserModel, verbose_name="Creator", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Knowledge Source"
        verbose_name_plural = "Knowledge Sources"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("taxcategs:categoryterm_create")


class InputFormatSupported(CategoryBase):
    """
    Input format supported by RPA components that are included in a category.
    """

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Input Format Supported"
        verbose_name_plural = "Input Formats Supported"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("taxcategs:categoryterm_create")  # , kwargs={"pk": self.pk})

DECISION_CHOICES = (
        ("1", "Accepted"),
        ("2", "Refused"),
        ("3", "Accepted with changes"),
    )

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    new_filename = random.randint(1, 123123123123)
    final_name = f"{new_filename}{ext}"
    return f"categories/{final_name}"

class CategoryTerm(models.Model):
    """
    Equivalent categories associated with the same taxonomic category. 
    """

    term = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_tax_categ = models.BooleanField(default=False)
    substitute_tax_categ = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    tax_categ = models.ForeignKey(
        TaxCateg, on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={'active': True},
    )
    knowledge_source = models.ForeignKey(KnowledgeSource, on_delete=models.CASCADE)
    formats_supported = models.ManyToManyField(InputFormatSupported, blank=True)
    user = models.ForeignKey(
        UserModel, verbose_name="Creator", on_delete=models.CASCADE
    )
    categoryChars = ArrayField(models.CharField(max_length=200))
    decision = models.CharField(max_length=5, choices=DECISION_CHOICES, blank=True)
    image = models.ImageField(upload_to=upload_image_path, blank=True)

    class Meta:
        verbose_name = "Category Term"
        verbose_name_plural = "Category Terms"

    @property
    def image_url(self):
        """
        Return self.photo.url if self.image is not None, 
        'url' exist and has a value, else, return None.
        """
        if self.image:
            return getattr(self.image, 'url', None)
        return None

    def create(self, validated_data):
        CategoryTerm.term_unique(self, validated_data.get("term"))
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        validated_data.update({"user": self.request.user})
        items = validated_data.pop("formats_supported", None)
        action = CategoryTerm.objects.create(**validated_data)
        if items is not None:
            # items = [InputFormatSupported.objects.create(**item) for item in items]
            # '*' is the "splat" operator: It takes a list as input, and expands it into actual positional arguments in the function call.
            action.formats_supported.add(*items)
        return action

    def term_unique(self, term):
        if CategoryTerm.objects.filter(term=term).exists():
            raise ValidationError('The term of the category term already exists')

    def __str__(self):
        return self.term

    def get_absolute_url(self):
        return reverse("taxcategs:categoryterm_detail", args=[self.pk])

    def clean(self):
        if(self.is_tax_categ and (not self.active)):
             raise ValidationError(
                "For a category to be taxonomical, it always has to be active"
            )
        if len(self.categoryChars) < 1:
            raise ValidationError(
                "A category term cannot have less than one category characteristic"
            )


# If you are using Django >= 1.9 with Postgres you can make use of ArrayField advantages

# A field for storing lists of data. Most field types can be used, you simply pass
# another field instance as the base_field. You may also specify a size. ArrayField
# can be nested to store multi-dimensional arrays.

# https://stackoverflow.com/questions/1110153/what-is-the-most-efficient-way-to-store-a-list-in-the-django-models


# class CategoryChar(models.Model):
#     """
#     Characteristics of a component belonging to one of the taxonomic categories.
#     """
#     rule = models.TextField()
#     active = models.BooleanField(default=False) #¿?
#     category_term = models.ForeignKey(CategoryTerm, verbose_name="Category Term", on_delete=models.CASCADE)
#     creator = models.ForeignKey(UserModel, verbose_name="Creator", on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = "Category characteristic"
#         verbose_name_plural = "Category characteristics"

#     def __str__(self):
#         return self.name


RESULT_CHOICES = (
        ("1", "New category term"),
        ("2", "Taxonomic category proposal save as new category term"),
        ("3", "New taxonomic category"),
        ("4", "Taxonomic category replaced"),
    )

class Report(models.Model):
    """
    Report of the decision taken after reviewing the proposal.
    """
    result = models.CharField(max_length=5, choices=RESULT_CHOICES, blank=True)
    categ_term = models.ForeignKey(
        CategoryTerm, verbose_name="Proposal reviewed", on_delete=models.CASCADE
    )
    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    review_user = models.ForeignKey(
        UserModel, verbose_name="Reviewer", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Decision"
        verbose_name_plural = "Decisions"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("taxcategs:categoryterm_create")

class Comment(models.Model):
    user = models.ForeignKey(UserModel, verbose_name="Author", on_delete=models.CASCADE)
    category_term = models.ForeignKey(CategoryTerm, on_delete=models.CASCADE, limit_choices_to={'active': True})
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("taxcategs:comment_list")
