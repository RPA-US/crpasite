from django import forms
from .models import CategoryTerm, KnowledgeSource, InputFormatSupported, Report, Comment

class ProposalCategoryTermForm(forms.ModelForm):
    class Meta:
        model = CategoryTerm
        exclude = ('user',)
        fields = (
            "term",
            "description",
            "is_tax_categ",
            "active",
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
            "active": forms.CheckboxInput(
                attrs={"class": "primary-checkbox", "checked": ""}
            ),
            "formats_supported": forms.CheckboxSelectMultiple(),
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
        self.user = kwargs.pop('user')
        super(ProposalCategoryTermForm, self).__init__(*args, **kwargs)

    def clean_term(self):
        term = self.cleaned_data['term']
        if CategoryTerm.objects.filter(user=self.user, term=term).exists():
            raise forms.ValidationError("You have already written a proposal with same term.")
        return term

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
        fields = ("decision", "result", "explanation", "user")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("user", "category_term", "title", "text")