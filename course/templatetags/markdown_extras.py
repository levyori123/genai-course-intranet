import markdown as md
import nh3
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def markdown(text):
    """Render Markdown, then sanitize so staff content can't inject scripts."""
    return mark_safe(nh3.clean(md.markdown(text or "", extensions=["extra"])))
