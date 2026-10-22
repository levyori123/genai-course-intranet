from pathlib import Path

from django.test import TestCase
from django.urls import reverse


class AgentsStripTests(TestCase):
    def setUp(self):
        session = self.client.session
        session["site_access"] = True
        session.save()

    def test_home_has_decorative_agents(self):
        html = self.client.get(reverse("home")).content.decode()
        self.assertIn('class="agents" aria-hidden="true"', html)
        self.assertEqual(html.count('class="agent '), 3)

    def test_css_respects_reduced_motion(self):
        css = Path(__file__).resolve().parents[1] / "static" / "course" / "style.css"
        self.assertIn("prefers-reduced-motion", css.read_text(encoding="utf-8"))
