import pytest
from django.core import mail

from ..models import EmailConfirmation


@pytest.mark.django_db
class TestEmailConfirmation:

    def test_send_email_confirmation(self, client, signup_data):
        """
        An email with token to confirmation must be sent
        """

        # Make the request
        client.post('/accounts/signup/', signup_data)

        # Ensure the email confirmation was created and sent
        assert EmailConfirmation.objects.exists()
        assert len(mail.outbox) == 1

        email = mail.outbox[0]
        email_confirmation = EmailConfirmation.objects.first()

        # Ensure the token was generated
        assert email_confirmation.token

        # Check email infos
        assert email_confirmation.user.email in email.to
        assert email_confirmation.token in email.body

    def test_confirm_email(self, client, signup_data):
        """
        An valid token must activate the associated user
        """

        # Make the request
        client.post('/accounts/signup/', signup_data)

        # Get token
        email_confirmation = EmailConfirmation.objects.first()
        token = email_confirmation.token

        # Access confirmation URL
        client.get('/accounts/signup/confirm/' + token)

        # Refresh object
        email_confirmation = EmailConfirmation.objects.first()

        # User must be actived now
        assert email_confirmation.user.is_active

        # Confirmation muts be confirmed now
        assert email_confirmation.is_confirmed

    def test_email_confirmation_usage(self, client, signup_data):
        """
        A confirmation email can't be used twice or more
        """

        # Make the request
        client.post('/accounts/signup/', signup_data)

        # Get token
        email_confirmation = EmailConfirmation.objects.first()
        token = email_confirmation.token

        # Access confirmation URL
        client.get('/accounts/signup/confirm/' + token)

        # Access confirmation URL again
        resp = client.get('/accounts/signup/confirm/' + token)

        # The link must be inactivated
        resp.status_code == 404
