from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode

SESSION_FLAG = "site_access"
EXEMPT_PREFIXES = ("/enter/", "/admin/")


class SitePasswordMiddleware:
    """Gate every page behind the shared SITE_PASSWORD.

    Exempt: the /enter/ form, Django admin (has its own login), static files,
    and logged-in staff. Everyone else without the session flag is redirected
    to /enter/?next=<path>.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self._is_allowed(request):
            url = reverse("enter")
            if request.get_full_path() != "/":
                url += "?" + urlencode({"next": request.get_full_path()})
            return redirect(url)
        return self.get_response(request)

    @staticmethod
    def _is_allowed(request):
        path = request.path_info
        static_url = "/" + settings.STATIC_URL.lstrip("/")
        if path.startswith(EXEMPT_PREFIXES) or path.startswith(static_url):
            return True
        user = getattr(request, "user", None)
        if user is not None and user.is_authenticated and user.is_staff:
            return True
        return bool(request.session.get(SESSION_FLAG))
