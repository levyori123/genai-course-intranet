from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from course.models import Announcement, CourseInfo, Lecture


class Command(BaseCommand):
    help = "Create demo content so the site has something to show."

    def handle(self, *args, **options):
        CourseInfo.objects.get_or_create(
            defaults=dict(
                title="Generative AI",
                semester="Fall 2026",
                description="An introduction to large language models, "
                "diffusion models and their applications.",
                schedule_text="Thursdays 14:00–16:00 · Mount Scopus",
            )
        )
        today = timezone.localdate()
        for n, title in enumerate(
            ["Introduction to Generative AI", "Transformers and LLMs", "Prompting"], 1
        ):
            Lecture.objects.get_or_create(
                number=n,
                defaults=dict(
                    title=title,
                    date=today + timedelta(days=7 * (n - 1) + 3),
                    description=f"Topics for lecture {n}.",
                ),
            )
        Announcement.objects.get_or_create(
            title="Welcome to the course",
            defaults=dict(
                body="Welcome! Materials will appear here as the semester goes on.",
                pinned=True,
            ),
        )
        self.stdout.write(self.style.SUCCESS("Demo data ready."))
