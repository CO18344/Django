from django import forms
from django.forms.widgets import PasswordInput
from customauth.models import MyUser

class UsersSignupForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=PasswordInput)

    def is_already_present(self):
        return MyUser.objects.filter(email=self.cleaned_data['email']).exists()

class UsersLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=PasswordInput)
