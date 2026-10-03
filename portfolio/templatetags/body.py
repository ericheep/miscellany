"""Render a work's Markdown body, with one-line shortcodes for media.

    {image: some-image-title}   an Image uploaded in the admin, by title
    {audio: some-audio-title}   an Audio clip uploaded in the admin, by title
    {vimeo: 123456789}          a Vimeo video, by ID
    {youtube: dQw4w9WgXcQ}      a YouTube video, by ID

Each shortcode must sit on its own line.
"""
import re

import markdown
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from portfolio.models import Audio, Image

register = template.Library()

SHORTCODE = re.compile(r'^\{(image|audio|vimeo|youtube):\s*(.+?)\s*\}[ \t]*$', re.MULTILINE)


def _missing(kind, value):
    return f'<p class="missing">Missing {kind}: {escape(value)}</p>'


def _embed(kind, value):
    if kind == 'image':
        img = Image.objects.filter(title=value).first()
        if not img:
            return _missing('image', value)
        return (f'<figure class="body-image"><a href="{img.image.url}" target="_blank" rel="noopener">'
                f'<img src="{img.image.url}" alt="{escape(img.title)}" loading="lazy"></a></figure>')

    if kind == 'audio':
        clip = Audio.objects.filter(title=value).first()
        if not clip or not clip.audio:
            return _missing('audio', value)
        caption = f'<figcaption>{escape(clip.title)}</figcaption>' if clip.title else ''
        return (f'<figure class="body-audio">{caption}'
                f'<audio controls preload="none" src="{clip.audio.url}"></audio></figure>')

    if kind == 'vimeo':
        return (f'<div class="body-video"><iframe src="https://player.vimeo.com/video/{escape(value)}" '
                f'allow="fullscreen; picture-in-picture" allowfullscreen></iframe></div>')

    if kind == 'youtube':
        return (f'<div class="body-video"><iframe src="https://www.youtube-nocookie.com/embed/{escape(value)}" '
                f'allow="fullscreen; picture-in-picture" allowfullscreen></iframe></div>')


@register.filter
def render_body(text):
    # Only the site owner writes this through the admin, so raw HTML is allowed.
    text = SHORTCODE.sub(lambda m: '\n\n' + _embed(m.group(1), m.group(2)) + '\n\n', text or '')
    return mark_safe(markdown.markdown(text, extensions=['extra']))
