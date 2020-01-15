# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django.forms import ModelForm
# from account.models import Account


# class SignUpForm(UserCreationForm):
#     username = forms.CharField(max_length=30, required=True, help_text='username')
#     email = forms.CharField(max_length=60, required=True, help_text='email')
#     password = forms.CharField(max_length=30, required=True, help_text='Password')
#     password_confirm = forms.CharField(max_length=30, required=True, help_text='Password_confirm')
#
#     def clean_username(self):
#         data = self.cleaned_data['username']
#         duplicate_users = User.objects.filter(username=data)
#         if duplicate_users.exists():
#             raise forms.ValidationError("this username has already taken!")
#         return data
#
#     def clean_password2(self):
#         data = self.cleaned_data['password']
#         check = self.cleaned_data['password_confirm']
#         if data != check:
#             raise forms.ValidationError("not equal passwords")
#         return data
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password', 'password_confirm',)


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password1', 'email', 'password2')
#
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Account
#         fields = ('birth_date', 'location', 'bio')

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=100, help_text='Last Name')
    # last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
