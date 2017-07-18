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
