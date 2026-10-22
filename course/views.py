from django.shortcuts import render
from django.utils import timezone

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
