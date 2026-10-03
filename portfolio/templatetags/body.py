"""Render a work's Markdown body, with embeds for media.

A line containing only one of these becomes an embedded player:

    https://www.youtube.com/watch?v=dQw4w9WgXcQ    (also youtu.be/..., /shorts/...)
    https://vimeo.com/123456789                    (also unlisted vimeo.com/123/abc)
    https://soundcloud.com/artist/track            (tracks or sets)
    {image: some-image-title}                      an Image uploaded in the admin
    {image: some-image-title | A caption}          ...with a caption (inline Markdown allowed)
    {audio: some-audio-title}                      an Audio clip uploaded in the admin
    {audio: some-audio-title | A caption}          ...with a caption

A link inside a sentence stays an ordinary link.
"""
import re
from html import unescape
from urllib.parse import quote

import markdown
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from portfolio.models import Audio, Image

register = template.Library()

SHORTCODE = re.compile(
    r'^\{(image|audio):\s*([^|}]+?)\s*(?:\|\s*(.*?)\s*)?\}[ \t]*$', re.MULTILINE)
BARE_URL = re.compile(r'^[ \t]*<?(https?://\S+?)>?[ \t]*$', re.MULTILINE)

YOUTUBE = re.compile(
    r'^https?://(?:www\.|m\.)?(?:youtube\.com/(?:watch\?(?:.*&)?v=|shorts/|embed/|live/)|youtu\.be/)'
    r'([\w-]{11})')
VIMEO = re.compile(r'^https?://(?:www\.|player\.)?vimeo\.com/(?:video/)?(\d+)(?:/([0-9a-f]+))?')
SOUNDCLOUD = re.compile(r'^https?://(?:www\.|m\.)?soundcloud\.com/[^/\s]+/[^\s]+')


def _missing(kind, value):
    return f'<p class="missing">Missing {kind}: {escape(value)}</p>'


def _video(src):
    return (f'<div class="body-video"><iframe src="{src}" '
            f'allow="fullscreen; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>')


def _caption_html(text):
    """Render a caption as inline Markdown (links, emphasis) without a <p> wrapper."""
    html = markdown.markdown(text)
    if html.startswith('<p>') and html.endswith('</p>'):
        html = html[3:-4]
    return html


def _caption(text):
    return f'<figcaption>{_caption_html(text)}</figcaption>'


def _plain(text):
    """Caption as plain text, for an image's alt attribute."""
    return escape(unescape(re.sub(r'<[^>]+>', '', _caption_html(text))))


def _shortcode(kind, value, caption):
    if kind == 'image':
        img = Image.objects.filter(title=value).first()
        if not img:
            return _missing('image', value)
        alt = _plain(caption) if caption else escape(img.title)
        return (f'<figure class="body-image"><a href="{img.image.url}" target="_blank" rel="noopener">'
                f'<img src="{img.image.url}" alt="{alt}" loading="lazy"></a>'
                f'{_caption(caption) if caption else ""}</figure>')

    clip = Audio.objects.filter(title=value).first()
    if not clip or not clip.audio:
        return _missing('audio', value)
    return (f'<figure class="body-audio">'
            f'<audio controls preload="none" src="{clip.audio.url}"></audio>'
            f'{_caption(caption) if caption else ""}</figure>')


def _url_embed(url):
    """Return embed HTML for a supported link, or None to leave it as text."""
    m = YOUTUBE.match(url)
    if m:
        return _video(f'https://www.youtube-nocookie.com/embed/{m.group(1)}')

    m = VIMEO.match(url)
    if m:
        src = f'https://player.vimeo.com/video/{m.group(1)}'
        if m.group(2):  # unlisted videos carry a privacy hash
            src += f'?h={m.group(2)}'
        return _video(src)

    if SOUNDCLOUD.match(url):
        src = f'https://w.soundcloud.com/player/?url={quote(url, safe="")}&visual=false'
        return (f'<div class="body-soundcloud"><iframe src="{escape(src)}" '
                f'allow="autoplay" loading="lazy"></iframe></div>')

    return None


def _block(html):
    return '\n\n' + html + '\n\n'


@register.filter
def render_body(text):
    # Only the site owner writes this through the admin, so raw HTML is allowed.
    text = text or ''
    text = SHORTCODE.sub(lambda m: _block(_shortcode(m.group(1), m.group(2), m.group(3))), text)
    text = BARE_URL.sub(
        lambda m: _block(html) if (html := _url_embed(m.group(1))) else m.group(0), text)
    return mark_safe(markdown.markdown(text, extensions=['extra']))
