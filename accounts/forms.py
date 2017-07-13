from django import forms
from django.utils.translation import ugettext_lazy as _

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

    def clean(self):
        """
        Validate passwords
        """
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError(_('The passwords don\'t match.'))
