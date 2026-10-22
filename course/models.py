from django.db import models
from django.utils import timezone


class CourseInfo(models.Model):
    """Singleton: the course header shown across the site."""

    title = models.CharField(max_length=200, default="Generative AI")
    semester = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    schedule_text = models.CharField(
        "Lecture time & place", max_length=200, blank=True
    )
    moodle_url = models.URLField(blank=True)
    zoom_url = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = "course info"

    def __str__(self):
        return self.title

    @classmethod
    def get(cls):
        return cls.objects.first() or cls()


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(help_text="Markdown supported.")
    published_at = models.DateTimeField(default=timezone.now)
    pinned = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-pinned", "-published_at"]

    def __str__(self):
        return self.title


class Lecture(models.Model):
    number = models.PositiveIntegerField(unique=True)
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text="Markdown supported.")
    recording_url = models.URLField(blank=True)

    class Meta:
        ordering = ["date", "number"]

    def __str__(self):
        return f"Lecture {self.number}: {self.title}"
