from django import forms

from .models import User


class SignupForm(forms.ModelForm):
    """
    Form for user signup
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ('name', 'email', 'password')
        model = User
