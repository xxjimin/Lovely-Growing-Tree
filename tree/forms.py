# tree/forms.py
from django import forms
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=4)
    password = forms.CharField(widget=forms.PasswordInput)
