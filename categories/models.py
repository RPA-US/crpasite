from django.db import models
from ..accounts import models as UserModel
from categories.models import CategoryBase
from enum import Enum

# Create your models here.

class TaxCateg(CategoryBase):
    """
    The category term that stands as the representative of the others.
    """
    
    class Meta:
        verbose_name = "Taxonomic category"
        verbose_name_plural = 'Taxonomic categories'

    def __str__(self):
        return self.name

    def clean(self):
        categ_terms = CategoryTerm.objects.filter(tax_categ=self, is_tax_categ=True, active=True)
        if(not(len(categ_terms)==1)):
            raise ValidationError('A taxonomic category always has to have at least one associated category term')

class CategoryTerm(models.Model):
    """
    Equivalent categories associated with the same taxonomic category. 
    """
    term = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_tax_categ = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    tax_categ = models.ForeignKey(TaxCateg, on_delete=models.CASCADE)
    knowledge_source = models.ForeignKey(KnowledgeSource, on_delete=models.CASCADE)
    formats_supported = models.ManyToManyField(InputFormatSupported)
    # knowledgeSource
    # list of category terms
    # list of category chars
    # list of input format supported

    class Meta:
        verbose_name = "Category Term"
        verbose_name_plural = "Category Terms"
        
    def __str__(self):
        return self.term
    
    def clean(self):
        categ_chars = CategoryChar.objects.filter(category_term=self, active=True)
        if(len(categ_chars)<1):
            raise ValidationError('A category term cannot have less than one category characteristic')
        if(len(self.formats_supported)<1):
            raise ValidationError('A category term cannot have less than one associated input format supported')


class KnowledgeSource(models.Model):
    """
    Knowledge source where the information that users relies on when writing a proposal, comes from.
    """
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=200, blank=True)
    creator = models.OneToOneField(UserModel.User, verbose_name=_("Creator"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Knowledge Source"
        verbose_name_plural = "Knowledge Sources"

    def __str__(self):
        return self.name


class CategoryChar(models.Model):
    """
    Characteristics of a component belonging to one of the taxonomic categories.
    """
    rule = models.TextField()
    active = models.BooleanField(default=False) #¿?
    category_term = models.ForeignKey(Category, verbose_name=_("Category Term"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Category characteristic")
        verbose_name_plural = _("Category characteristics")

    def __str__(self):
        return self.name

class InputFormatSupported(CategoryBase):
    """
    Input format supported by RPA components that are included in a category.
    """
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = _("Input Format Supported")
        verbose_name_plural = _("Input Formats Supported")

    def __str__(self):
        return self.name

class Report(models.Model):
    """
    Report of the decision taken after reviewing the proposal.
    """
    decision = models.CharField(
      max_length=30,
      choices=[(tag, tag.value) for tag in DecisionChoice]  # Choices is a list of Tuple
    )
    result = models.CharField(
      max_length=60,
      choices=[(tag, tag.value) for tag in ResultChoice]  # Choices is a list of Tuple
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reviewer = models.ForeignKey(UserModel.User)

    class Meta:
        verbose_name = 'Decision'
        verbose_name_plural = 'Decisions'
    
    def __str__(self):
        return self.name

class DecisionChoice(Enum):
    OK = "Accepted"
    KO = "Refused"
    KK = "Accepted with changes"

class ResultChoice(Enum):
    NC = "New category term"
    NT = "New taxonomic category"
    CT = "Taxonomic category proposal save as new category term"
    TE = "Taxonomic category edited"

class Comment(models.Model):
    author = models.ForeignKey(UserModel.User)
    category_term = models.ForeignKey(CategoryTerm)
    title = models.CharField(max_length=50)
    text = models.TextField()
    
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.name
