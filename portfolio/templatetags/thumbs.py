"""{% thumbnail work.mainImage work.title forloop.counter %} -> a sized, responsive <img>.

The first few cards (the first row) load right away; the rest as you scroll.
"""
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from portfolio.thumbnails import WIDTHS, thumb_url

register = template.Library()

# How wide a card is on screen: one column on phones, roughly 260-400px otherwise
SIZES = '(max-width: 600px) calc(100vw - 60px), 400px'
EAGER_COUNT = 4  # cards loaded immediately


@register.simple_tag
def thumbnail(field_file, alt='', position=99):
    if not field_file:
        return ''
    urls = {w: thumb_url(field_file, w) for w in WIDTHS}
    alt = escape(alt)
    eager = int(position or 99) <= EAGER_COUNT
    loading = 'eager" fetchpriority="high' if eager else 'lazy'

    if all(urls.values()):
        srcset = ', '.join(f'{urls[w]} {w}w' for w in WIDTHS)
        return mark_safe(
            f'<img src="{urls[WIDTHS[0]]}" srcset="{srcset}" sizes="{SIZES}" '
            f'width="{WIDTHS[0]}" height="{WIDTHS[0] * 3 // 4}" alt="{alt}" '
            f'loading="{loading}" decoding="async">')

    # no thumbnails yet: fall back to the original
    return mark_safe(f'<img src="{field_file.url}" alt="{alt}" loading="{loading}" decoding="async">')
