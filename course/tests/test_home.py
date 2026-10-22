from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from course.models import Announcement, CourseInfo, Lecture
from course.templatetags.markdown_extras import markdown


class HomePageTests(TestCase):
    def setUp(self):
        session = self.client.session
        session["site_access"] = True
        session.save()

    def test_empty_site_renders(self):
        r = self.client.get(reverse("home"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "No announcements yet.")
        self.assertContains(r, "No upcoming lectures")

    def test_shows_course_title(self):
        CourseInfo.objects.create(title="Gen AI 101", semester="Fall 2026")
        self.assertContains(self.client.get(reverse("home")), "Gen AI 101")

    def test_next_lecture_skips_past(self):
        today = timezone.localdate()
        Lecture.objects.create(number=1, date=today - timedelta(days=7), title="Past")
        Lecture.objects.create(number=2, date=today + timedelta(days=2), title="Soon")
        Lecture.objects.create(number=3, date=today + timedelta(days=9), title="Later")
        r = self.client.get(reverse("home"))
        self.assertContains(r, "Soon")
        self.assertNotContains(r, "Past")
        self.assertNotContains(r, "Later")

    def test_unpublished_announcement_hidden_and_pinned_first(self):
        Announcement.objects.create(title="Normal", body="x")
        Announcement.objects.create(title="Pinned", body="x", pinned=True)
        Announcement.objects.create(title="Secret", body="x", is_published=False)
        r = self.client.get(reverse("home"))
        self.assertNotContains(r, "Secret")
        body = r.content.decode()
        self.assertLess(body.index("Pinned"), body.index("Normal"))

    def test_markdown_strips_scripts(self):
        out = markdown("hi <script>alert(1)</script> **bold**")
        self.assertNotIn("<script", out)
        self.assertIn("<strong>bold</strong>", out)
