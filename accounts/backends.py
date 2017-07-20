from django.shortcuts import get_object_or_404

from .models import EmailConfirmation, User


class ConfirmationTokenAuthenticationBackend:
    """
    Authenticate users against their EmailConfirmation token.
    """

    def authenticate(self, token):
        """
        If the given token is valid (not used yet),
        active and return the user
        """
        email_confirmation = get_object_or_404(
            EmailConfirmation,
            token=token,
            is_confirmed=False)

        # Update confirmation object
        email_confirmation.is_confirmed = True
        email_confirmation.save()

        # Update user associated
        email_confirmation.user.is_active = True
        email_confirmation.user.save()

        return email_confirmation.user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass
