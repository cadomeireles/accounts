import hashlib
import uuid
from random import random

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.urlresolvers import reverse as r
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .email import send_email
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model
    """

    # Fields
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    name = models.CharField(
        _('name'),
        max_length=120,
    )
    email = models.EmailField(
        _('email'),
        unique=True,
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )

    # Override manager
    objects = UserManager()

    # Auth settings
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Return name
        """
        return self.name

    def get_short_name(self):
        """
        Split name and return first result
        """
        return self.name.split()[0]


class EmailConfirmation(models.Model):
    """
    Confirmation for user email
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='email_confirmations',
    )
    token = models.CharField(max_length=40)
    is_confirmed = models.BooleanField(default=False)

    def send(self):
        """
        Send email with link to confirm email
        """
        link = r('accounts:confirm_email', kwargs={'token': self.token})
        send_email(
            _('Email confirmation'),
            [self.user.email],
            'accounts/emails/email_confirmation.html',
            {'link': link},
        )

    def save(self, *args, **kwargs):
        """
        Save EmailConfirmation and generate token
        """
        created = not self.pk

        # Call default save method
        super().save(*args, **kwargs)

        # Generate token on create
        if created:
            token = str(random()) + self.user.email
            self.token = hashlib.sha1(token.encode()).hexdigest()
            self.save()
