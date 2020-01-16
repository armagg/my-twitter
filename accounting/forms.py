from django import forms
from django.contrib.auth.models import User

from accounting.models import Account


class UserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ()
