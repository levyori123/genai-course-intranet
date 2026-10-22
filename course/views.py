import hmac

from django.conf import settings
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone

from .middleware import SESSION_FLAG
from .models import Announcement, CourseInfo, Lecture


def home(request):
    today = timezone.localdate()
    announcements = Announcement.objects.filter(is_published=True)[:5]
    next_lecture = Lecture.objects.filter(date__gte=today).first()
    return render(
        request,
        "course/home.html",
        {
            "course": CourseInfo.get(),
            "announcements": announcements,
            "next_lecture": next_lecture,
        },
    )


def _safe_next(request, candidate):
    if candidate and url_has_allowed_host_and_scheme(
        candidate, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return candidate
    return "/"


@never_cache
@csrf_protect
def enter(request):
    next_url = _safe_next(request, request.POST.get("next") or request.GET.get("next"))
    if request.session.get(SESSION_FLAG):
        return redirect(next_url)
    error = None
    expected = getattr(settings, "SITE_PASSWORD", "")
    if request.method == "POST":
        given = request.POST.get("password", "")
        if expected and hmac.compare_digest(given.encode(), expected.encode()):
            request.session.cycle_key()
            request.session[SESSION_FLAG] = True
            return redirect(next_url)
        error = "That password isn't right." if expected else "Site access isn't configured yet."
    return render(
        request,
        "course/enter.html",
        {"course": CourseInfo.get(), "error": error, "next": next_url},
        status=401 if error else 200,
    )
