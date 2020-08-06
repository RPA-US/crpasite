from django import forms
from .models import CategoryTerm, KnowledgeSource, InputFormatSupported, Report, Comment


class ProposalCategoryTermForm(forms.ModelForm):
    class Meta:
        model = CategoryTerm
        exclude = (
            "user",
            "active",
            "is_tax_categ",
            "substitute_tax_categ",
            "decision"
        )
        fields = (
            "term",
            "description",
            "tax_categ",
            "knowledge_source",
            "formats_supported",
            "categoryChars",
        )

        widgets = {
            "term": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "placeholder": "Term",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'Term'",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "single-input",
                    "placeholder": "Description",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'Description'",
                    "rows": "5",
                }
            ),
            "tax_categ": forms.Select(attrs={"class": "form-control default-select"}),
            "formats_supported": forms.SelectMultiple(
                attrs={
                    "class": "multipleselector",
                    "data-placeholder": "Click to select an option...",
                    "multiple": "multiple",
                }
            ),
            "categoryChars": forms.Textarea(
                attrs={
                    "class": "single-input",
                    "placeholder": "Category characteristics (separated by commas)",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'Category characteristics (separated by commas)'",
                    "rows": "5",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.taxcategdecision = kwargs.pop("taxcategdecision")
        super(ProposalCategoryTermForm, self).__init__(*args, **kwargs)

    def clean_term(self):
        term = self.cleaned_data["term"]
        if CategoryTerm.objects.filter(term=term).exists():
            raise forms.ValidationError(
                "There is already a proposal with the same term."
            )
        return term

    def clean_formats_supported(self):
        ifp = self.cleaned_data["formats_supported"]
        if len(ifp) < 1:
            raise forms.ValidationError(
                "A category term cannot have less than one associated input format supported"
            )
        return ifp

    def clean_categoryChars(self):
        categChars = self.cleaned_data["categoryChars"]
        if len(categChars) < 1:
            raise ValidationError(
                "A category term cannot have less than one category characteristic"
            )
        return categChars

class ProposalReviewForm(forms.ModelForm):
    class Meta:
        model = CategoryTerm
        exclude = (
            "user",
            "active",
            "is_tax_categ",
            "substitute_tax_categ"
        )
        fields = (
            "term",
            "description",
            "tax_categ",
            "knowledge_source",
            "formats_supported",
            "categoryChars",
            "decision"
        )

        widgets = {
            "term": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "placeholder": "Term",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'Term'",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "single-input",
                    "placeholder": "Description",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'Description'",
                    "rows": "5",
                }
            ),
            "tax_categ": forms.Select(attrs={"class": "form-control default-select"}),
            "formats_supported": forms.SelectMultiple(
                attrs={
                    "class": "multipleselector",
                    "data-placeholder": "Click to select an option...",
                    "multiple": "multiple",
                }
            ),
            "categoryChars": forms.Textarea(
                attrs={
                    "class": "single-input",
                    "placeholder": "Category characteristics (separated by commas)",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'Category characteristics (separated by commas)'",
                    "rows": "5",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ProposalReviewForm, self).__init__(*args, **kwargs)

    def clean_term(self):
        term = self.cleaned_data["term"]
        if CategoryTerm.objects.filter(term=term).exists():
            raise forms.ValidationError(
                "There is already a proposal with the same term."
            )
        return term

    def clean_formats_supported(self):
        ifp = self.cleaned_data["formats_supported"]
        if len(ifp) < 1:
            raise forms.ValidationError(
                "A category term cannot have less than one associated input format supported"
            )
        return ifp

    def clean_categoryChars(self):
        categChars = self.cleaned_data["categoryChars"]
        if len(categChars) < 1:
            raise ValidationError(
                "A category term cannot have less than one category characteristic"
            )
        return categChars

class InputFormatSupportedForm(forms.ModelForm):
    class Meta:
        model = InputFormatSupported
        fields = ("name", "slug", "parent")


class KnowledgeSourceForm(forms.ModelForm):
    class Meta:
        model = KnowledgeSource
        fields = ("name", "url", "creator", "active")


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ("result", "explanation", "review_user")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("user", "category_term", "title", "text")
