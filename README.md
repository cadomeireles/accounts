# accounts app
A Django app for user accounts.

## Usage

1. Clone this repo into your project.
2. Add the app to `INSTALLED_APPS` list.
3. Set `AUTH_USER_MODEL` on your settings to `accounts.User`.
4. Run the migrations.
5. Include the `accounts.urls` to your main URLconf with namespace `accounts`.
6. Add `accounts.backends.ConfirmationTokenAuthenticationBackend` to `AUTHENTICATION_BACKENDS`.
7. Configure your project to be able to send email.

## Running tests
1. Install [pytest-django](https://pytest-django.readthedocs.io):

`pip install pytest-django`

2. Execute tests:

`pytest`
