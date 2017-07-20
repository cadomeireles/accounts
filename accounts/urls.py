from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(
        r'^signup/confirm/(?P<token>\w{40})',
        views.ConfirmEmailView.as_view(),
        name='confirm_email',
    ),
]
