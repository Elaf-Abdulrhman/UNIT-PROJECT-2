from django import template
from urllib.parse import urlparse, parse_qs

register = template.Library()

@register.filter
def youtube_embed(url):
    """Convert a standard YouTube URL into an embed URL."""
    try:
        query = parse_qs(urlparse(url).query)
        video_id = query.get("v")[0]
        return f"https://www.youtube.com/embed/{video_id}"
    except Exception:
        return ""