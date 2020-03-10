import logging
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from colorful.widgets import ColorFieldWidget
from django import forms
from django.forms import ModelForm
from .models import WebProjects
from djng.forms import fields, NgFormValidationMixin
from djng.styling.bootstrap3.forms import Bootstrap3Form


class AIRPAPIRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput({'class': 'form-control'}))
    username = forms.CharField(required=True, max_length=30, widget=forms.TextInput({'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput({'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput({'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name'
        )


    def save(self, commit=True):
        user = super(AIRPAPIRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = False

        if commit:
            user.save()
        return user


class ProjectForm(ModelForm):
    class Meta:
        model = WebProjects
        fields = ['web_tx_name','web_tx_description','web_cl_colour','web_cd_user']
        widgets = {'web_tx_name': forms.TextInput(),
                   'web_tx_description': forms.Textarea({'rows': 4}),
                   'web_cl_colour': forms.CharField(widget=ColorFieldWidget),
                   'web_cd_user': forms.HiddenInput}


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']


################################# Formularios para mostrar ejemplos de uso Servinform ##########################

MODEL_CHOICES= [('hupikonobu','Modelo general')]

class AirpaTextAlignmentFormText(NgFormValidationMixin, Bootstrap3Form,forms.Form):
    use_required_attribute = False

    # email = forms.EmailField(required=True, widget=forms.TextInput({'class': 'form-control'}))
    airpa_text_model = fields.ChoiceField(required=True, label="Modelo Usado", choices=MODEL_CHOICES, initial='hupikonobu',
                                          error_messages={'invalid': 'Introduzca un modelo válido'},
                                          )
    search_text=fields.CharField(required=True, label="Texto Buscado", error_messages={'invalid': 'Introduzca el texto a búscar'})
    text = fields.CharField(required=True, label="Texto",error_messages={'invalid': 'Introduzca un texto'})



class AirpaTextAlignmentFormList(NgFormValidationMixin, Bootstrap3Form,forms.Form):
    use_required_attribute = False

    # email = forms.EmailField(required=True, widget=forms.TextInput({'class': 'form-control'}))
    airpa_text_model_list = fields.ChoiceField(required=True,label="Modelo Usado", choices=MODEL_CHOICES,
                                          error_messages={'invalid': 'Introduzca un modelo válido'},
                                          )
    search_text_list=fields.CharField(required=True,  label="Texto Buscado", error_messages={'invalid': 'Introduzca el texto a búscar'})


class AirpaTextAlignmentFormCompleteList(AirpaTextAlignmentFormList):

    list = fields.CharField(required=True, label="Lista de Textos", error_messages={'invalid': 'Introduzca alguna etiqueta'})


class AirpaReaderForm(forms.Form):

    # email = forms.EmailField(required=True, widget=forms.TextInput({'class': 'form-control'}))
    airpa_reader_file = forms.FileField(label="Introducir fichero",required=True)


class SpacyForm(NgFormValidationMixin, Bootstrap3Form,forms.Form):
    use_required_attribute = False

    spacy_text=fields.CharField(required=True, label="Texto", error_messages={'invalid': 'Introduzca el texto donde buscar'})