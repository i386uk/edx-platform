"""Middleware classes for third_party_auth."""

from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from requests import HTTPError
from social_django.middleware import SocialAuthExceptionMiddleware

from student.helpers import get_next_url_for_login_page

from . import pipeline


class ExceptionMiddleware(SocialAuthExceptionMiddleware):
    """Custom middleware that handles conditional redirection."""

    def get_redirect_uri(self, request, exception):
        # Fall back to django settings's SOCIAL_AUTH_LOGIN_ERROR_URL.
        redirect_uri = super(ExceptionMiddleware, self).get_redirect_uri(request, exception)

        # Safe because it's already been validated by
        # pipeline.parse_query_params. If that pipeline step ever moves later
        # in the pipeline stack, we'd need to validate this value because it
        # would be an injection point for attacker data.
        auth_entry = request.session.get(pipeline.AUTH_ENTRY_KEY)

        # Check if we have an auth entry key we can use instead
        if auth_entry and auth_entry in pipeline.AUTH_DISPATCH_URLS:
            redirect_uri = pipeline.AUTH_DISPATCH_URLS[auth_entry]

        return redirect_uri

    def process_exception(self, request, exception):
        """Handles specific exception raised by Python Social Auth eg HTTPError."""
        if isinstance(exception, HTTPError):
            messages.error(request, _('Unable to connect with the external provider, please try again'),
                           extra_tags='social-auth')

            redirect_url = get_next_url_for_login_page(request)
            return redirect('/login?next=' + redirect_url)
        else:
            super(ExceptionMiddleware, self).process_exception(request, exception)
