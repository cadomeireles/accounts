import pytest
from django.core import mail

from ..models import User, EmailConfirmation


@pytest.mark.django_db
class TestUserSignup:

    @pytest.mark.parametrize('uses_data, successful, status_code', [
        (True, True, 302),
        (False, False, 200),
    ])
    def test_signup(
        self, client, uses_data, successful, status_code, signup_data,
    ):
        """
        POST with correct data on /accounts/signup/ must save a new user
        """
        data = signup_data if uses_data else {}

        # Make the request
        resp = client.post('/accounts/signup/', data)

        # Check database state
        assert User.objects.exists() == successful

        # Check status code
        assert resp.status_code == status_code

    @pytest.mark.parametrize('right_passwords, successful, status_code', [
        (True, True, 302),
        (False, False, 200),
    ])
    def test_password_confirmation(
        self, client, signup_data, right_passwords, successful, status_code
    ):
        """
        The passwords must match to finish signup
        """
        if not right_passwords:
            signup_data['password_confirm'] = 'wrong_password'

        # Make the request
        resp = client.post('/accounts/signup/', signup_data)

        # Check database state
        assert User.objects.exists() == successful

        # Check status code
        assert resp.status_code == status_code

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
