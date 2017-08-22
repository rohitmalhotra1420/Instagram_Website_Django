from django import forms
from models import UserModel,SessionToken,PostModel


class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields=['email','username','name','password']

 #forms.py
class LoginForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password']