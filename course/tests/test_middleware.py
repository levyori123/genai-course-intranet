from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from course.middleware import SESSION_FLAG


@override_settings(SITE_PASSWORD="open-sesame")
class SitePasswordTests(TestCase):
    def test_redirects_anonymous(self):
        r = self.client.get(reverse("home"))
        self.assertRedirects(r, reverse("enter"), fetch_redirect_response=False)

    def test_redirect_keeps_next(self):
        r = self.client.get("/some/page/?x=1")
        self.assertEqual(r.status_code, 302)
        self.assertIn("next=%2Fsome%2Fpage%2F%3Fx%3D1", r["Location"])

    def test_enter_page_is_reachable(self):
        self.assertEqual(self.client.get(reverse("enter")).status_code, 200)

    def test_wrong_password_rejected(self):
        r = self.client.post(reverse("enter"), {"password": "nope"})
        self.assertEqual(r.status_code, 401)
        self.assertNotIn(SESSION_FLAG, self.client.session)

    def test_right_password_grants_access(self):
        r = self.client.post(reverse("enter"), {"password": "open-sesame"})
        self.assertRedirects(r, "/", fetch_redirect_response=False)
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)

    def test_open_redirect_blocked(self):
        r = self.client.post(
            reverse("enter"), {"password": "open-sesame", "next": "https://evil.example/"}
        )
        self.assertEqual(r["Location"], "/")

    def test_local_next_honoured(self):
        r = self.client.post(reverse("enter"), {"password": "open-sesame", "next": "/x/"})
        self.assertEqual(r["Location"], "/x/")

    def test_admin_and_static_exempt(self):
        self.assertEqual(self.client.get("/admin/login/").status_code, 200)
        r = self.client.get("/static/course/style.css")
        self.assertNotEqual(r.get("Location", ""), reverse("enter"))

    def test_staff_bypass(self):
        staff = get_user_model().objects.create_user("t", password="pw", is_staff=True)
        self.client.force_login(staff)
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)

    def test_csrf_enforced(self):
        from django.test import Client
        c = Client(enforce_csrf_checks=True)
        self.assertEqual(c.post(reverse("enter"), {"password": "open-sesame"}).status_code, 403)


@override_settings(SITE_PASSWORD="")
class UnconfiguredPasswordTests(TestCase):
    def test_fails_closed(self):
        r = self.client.post(reverse("enter"), {"password": ""})
        self.assertEqual(r.status_code, 401)
        self.assertEqual(self.client.get(reverse("home")).status_code, 302)
