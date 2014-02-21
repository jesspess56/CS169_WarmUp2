from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=138)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=138, required=False)
