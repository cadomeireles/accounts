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

    def form_valid(self, form):
        """
        Save user and send email confirmation
        """
        # Save user
        user = form.save()

        # Create and send email confirmation
        email_confirmation = user.email_confirmations.create()
        email_confirmation.send()

        return super().form_valid(form)
