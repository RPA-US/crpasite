from django import forms
from .models import (
    CategoryTerm,
    KnowledgeSource,
    InputFormatSupported,
    Report,
    Comment,
    TaxCateg,
)


class ProposalCategoryTermForm(forms.ModelForm):
    class Meta:
        model = CategoryTerm
        exclude = (
            "user",
            "active",
            "is_tax_categ",
            "substitute_tax_categ",
            "decision",
        )
        fields = (
            "term",
            "description",
            "tax_categ",
            "knowledge_source",
            "image",
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
            "image": forms.FileInput(
                attrs={"class": "form-control", "placeholder": "Image"}
            ),
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
        if self.taxcategdecision == "2":
            self.base_fields["tax_categ"].label = "Parent category"
        else:
            self.base_fields["tax_categ"].label = "Taxonomic category"
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
            "image",
            "is_tax_categ",
            "substitute_tax_categ",
            "knowledge_source",
            "tax_categ",
        )
        fields = (
            "term",
            "description",
            "formats_supported",
            "categoryChars",
            "decision",
        )

        widgets = {
            "term": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "placeholder": "Term",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'Term'",
                    "readonly": "",
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
            "decision": forms.Select(attrs={"class": "cat_decision",}),
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
        if not CategoryTerm.objects.filter(term=term).exists():
            raise forms.ValidationError(
                "Reviewer cannot edit the term of the category proposal."
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

    def clean_decision(self):
        d = self.cleaned_data["decision"]
        if not d:
            raise forms.ValidationError(
                "Reviewer cannot review a proposal without taking a decision."
            )
        return d


class InputFormatSupportedForm(forms.ModelForm):
    class Meta:
        model = InputFormatSupported
        exclude = ("slug",)
        fields = ("name", "parent")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "placeholder": "Name",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'Name'",
                }
            ),
        }



class KnowledgeSourceForm(forms.ModelForm):
    class Meta:
        model = KnowledgeSource
        exclude = (
            "creator",
            "active",
        )
        fields = (
            "name",
            "url",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "placeholder": "Name",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'Name'",
                }
            ),
            "url": forms.URLInput(
                attrs={
                    "class": "single-input",
                    "placeholder": "URL",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'URL'",
                }
            ),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = (
            "result",
            "explanation",
        )
        exclude = (
            "review_user",
            "categ_term",
        )
        widgets = {
            "explanation": forms.Textarea(
                attrs={
                    "class": "single-input",
                    "placeholder": "Explanation of the decision taken and its result",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'Explanation of the decision taken and its result'",
                    "rows": "5",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ("user", "category_term")
        fields = ("title", "text",)
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "placeholder": "Title of the comment",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'Title of the comment'",
                }
            ),
            "text": forms.Textarea(
                attrs={
                    "class": "single-input",
                    "placeholder": "Comment...",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'Comment...'",
                    "rows": "5",
                }
            ),
        }
