from django import forms

from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "address_line_1",
            "address_line_2",
            "city",
            "country",
            "state",
            "postal_code",
        ]
        widget = {
            "address_line_1": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "placeholder": "Address line 1",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'Address line 1'",
                }
            ),
            "address_line_2": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "placeholder": "Address line 2",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'Address line 2'",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "placeholder": "City",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'City'",
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "placeholder": "Country",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'Country'",
                }
            ),
            "state": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "placeholder": "State",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'State'",
                }
            ),
            "postal_code": forms.TextInput(
                attrs={
                    "class": "single-input",
                    "placeholder": "Postal code",
                    "onfocus": "this.placeholder = ''",
                    "onblur": "this.placeholder = 'Postal code'",
                }
            ),
        }
