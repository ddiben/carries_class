from django import forms

class LoginForm(forms.Form):
    password_field = forms.CharField(widget=forms.TextInput(
        attrs={'class' : 'login-input'}), label="", max_length=100)

class LoginAgainForm(forms.Form):
    password_field = forms.CharField(widget=forms.TextInput(
        attrs={'class' : 'login-input', 'placeholder' : 'incorrect key'}), label="", max_length=100)