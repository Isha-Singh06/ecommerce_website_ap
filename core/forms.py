from django import forms

class checkout_form(forms.Form):
    house_address = forms.CharField()
    town = forms.CharField()
    country = forms.CharField()
    zip = forms.CharField()
    save_as_Default = forms.BooleanField(required=False)
