from django.core.urlresolvers import reverse_lazy as r
from django.views.generic import CreateView

from .forms import SignupForm


class SignupView(CreateView):
    """
    View to save a new user
    """
    form_class = SignupForm
    success_url = r('accounts:signup')
    template_name = 'accounts/signup.html'
