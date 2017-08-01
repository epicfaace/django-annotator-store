from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import resolve_url
from django.template import RequestContext
from django.template.loader import get_template
from django.utils.decorators import available_attrs
from django.utils.six.moves.urllib.parse import urlparse



def absolutize_url(local_url):
    '''Convert a local url to an absolute url, with scheme and server name,
    based on the current configured :class:`~django.contrib.sites.models.Site`.

    :param local_url: local url to be absolutized, e.g. something generated by
        :meth:`~django.core.urlresolvers.reverse`
    '''
    if local_url.startswith('https'):
        return local_url

    # add scheme and server (i.e., the http://example.com) based
    # on the django Sites infrastructure.
    root = Site.objects.get_current().domain
    # but also add the http:// if necessary, since most sites docs
    # suggest using just the domain name
    if not root.startswith('https'):
        root = 'https://' + root

    # make sure there is no double slash between site url and local url
    if local_url.startswith('/'):
        root = root.rstrip('/')

    return root + local_url



def user_passes_test_ajax_403(test_func, login_url=None,
                              redirect_field_name=REDIRECT_FIELD_NAME):
    '''Variation on :meth:`django.contrib.auth.decorators.user_passes_test`.
    If the user is already logged in but has insufficient privileges,
    returns a 403 Forbidden response because redirecting to log in is not
    useful.  If request is ajax user is not authenticated, returns a 401
    because redirecting an ajax request to login is also not useful.

    Partially adapted from/inspired by :mod:`eulcommon` implementation.
    http://eulcommon.readthedocs.io/en/0.17.0/djangoextras.html#module-eulcommon.djangoextras.auth
    '''

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            # if test passes, return view normally
            if test_func(request.user):
                return view_func(request, *args, **kwargs)

            # if user is authenticated, default django behavior of
            # redirecting to login page is not useful
            if request.user.is_authenticated():
                raise PermissionDenied

            # if user is not authenticated, check for ajax request
            # (redirect to login also not useful for ajax)
            if request.is_ajax():
                # send 403 Forbidden response
                resp = HttpResponse('Not Authorized')
                resp.status_code = 401
                return resp

            # otherwise redirect normally
            # (default user_passes_test logic from django)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def permission_required(perm, login_url=None):
    '''Version of :meth:`django.contrib.auth.decorators.permission_required`
    that uses :meth:`user_passes_test_with_ajax_403` for better
    http response codes and ajax handling.'''
    return user_passes_test_ajax_403(lambda u: u.has_perm(perm), login_url=login_url)
