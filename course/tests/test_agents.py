import re
from pathlib import Path

from django.test import TestCase
from django.urls import reverse


class AgentsStripTests(TestCase):
    def test_home_has_decorative_agents(self):
        html = self.client.get(reverse("home")).content.decode()
        self.assertIn('class="agents" aria-hidden="true"', html)
        self.assertEqual(html.count('class="agent '), 3)

    def test_skip_link_and_main_target(self):
        html = self.client.get(reverse("home")).content.decode()
        self.assertIn('class="skip-link" href="#main"', html)
        self.assertIn('id="main"', html)
        self.assertIn('aria-current="page"', html)

    def test_favicon_linked(self):
        html = self.client.get(reverse("home")).content.decode()
        self.assertIn("course/favicon.svg", html)

    def test_agents_strip_not_fixed(self):
        css = Path(__file__).resolve().parents[1] / "static" / "course" / "style.css"
        bodies = re.findall(r"\.agents\s*\{([^}]*)\}", css.read_text(encoding="utf-8"))
        self.assertTrue(bodies)
        for body in bodies:
            self.assertNotRegex(body, r"position\s*:\s*fixed")

    def test_css_respects_reduced_motion(self):
        css = Path(__file__).resolve().parents[1] / "static" / "course" / "style.css"
        self.assertIn("prefers-reduced-motion", css.read_text(encoding="utf-8"))
