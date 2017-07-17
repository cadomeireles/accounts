from django.core import mail

from ..email import send_email


class TestSendEmailTemplate:

    def test_email_sending(self):
        """
        Check if email is sent correctly
        """
        subject = 'Sending test'
        message = 'Email sending test.'
        to = ['recipient@email.com']

        # Send email
        send_email(
            subject,
            to,
            'accounts/emails/basic_template.html',
            {'message': message},
        )

        # Check email
        email = mail.outbox[0]
        assert email.subject == subject
        assert email.to == to
        assert message in email.body
