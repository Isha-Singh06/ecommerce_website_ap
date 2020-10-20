from django import forms

class checkout_form(forms.Form):
    house_address = forms.CharField(required=False)
    town = forms.CharField(required=False)
    country = forms.CharField(required=False)
    zip = forms.CharField(required=False)
    save_as_Default = forms.BooleanField(required=False)
    use_default_address = forms.BooleanField(required=False)


    
