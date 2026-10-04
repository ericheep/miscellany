"""Render a work's Markdown body, with embeds for media.

A line containing only one of these becomes an embedded player:

    https://www.youtube.com/watch?v=dQw4w9WgXcQ    (also youtu.be/..., /shorts/...)
    https://vimeo.com/123456789                    (also unlisted vimeo.com/123/abc)
    https://soundcloud.com/artist/track            (tracks or sets)
    {image: some-image-title}                      an Image uploaded in the admin
    {image: some-image-title | A caption}          ...with a caption (inline Markdown allowed)
    {image: some-image-title right 40% | Caption}  ...placed and sized (see IMAGE OPTIONS below)
    {audio: some-audio-title}                      an Audio clip uploaded in the admin
    {audio: some-audio-title | A caption}          ...with a caption

    {images: one, two, three | Caption}            several images side by side at equal height
    https://vimeo.com/123456789 right 50%          videos take the same placement/width options
    {clear}                                        start the next text below any wrapped image

A link inside a sentence stays an ordinary link.

IMAGE OPTIONS, written after the image name, in any order:
    left / right    float the image so the following text wraps around it
    center          center it, no wrapping
    full            stretch it to the full column width
    40%             width relative to the text column (height keeps the aspect ratio)
    300px or 300    fixed width in pixels (never wider than the column)
Floated images without a width default to 40%, videos to 50%. On phones nothing wraps.
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
CLEAR = re.compile(r'^\{clear\}[ \t]*$', re.MULTILINE)
PLACEMENTS = {'left', 'right', 'center', 'full'}
WIDTH = re.compile(r'^(\d{1,4})(px|%)?$')
DEFAULT_FLOAT_WIDTH = '40%'
DEFAULT_VIDEO_FLOAT_WIDTH = '50%'
BARE_URL = re.compile(r'^[ \t]*<?(https?://[^\s>]+)>?((?:[ \t]+\S+)*)[ \t]*$', re.MULTILINE)
IMAGE_ROW = re.compile(r'^\{images:\s*([^|}]+?)\s*(?:\|\s*(.*?)\s*)?\}[ \t]*$', re.MULTILINE)

YOUTUBE = re.compile(
    r'^https?://(?:www\.|m\.)?(?:youtube\.com/(?:watch\?(?:.*&)?v=|shorts/|embed/|live/)|youtu\.be/)'
    r'([\w-]{11})')
VIMEO = re.compile(r'^https?://(?:www\.|player\.)?vimeo\.com/(?:video/)?(\d+)(?:/([0-9a-f]+))?')
SOUNDCLOUD = re.compile(r'^https?://(?:www\.|m\.)?soundcloud\.com/[^/\s]+/[^\s]+')


def _missing(kind, value):
    return f'<p class="missing">Missing {kind}: {escape(value)}</p>'


def _video(src, attrs='class="body-video"'):
    return (f'<div {attrs}><iframe src="{src}" '
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


def _parse_option(word, placement, width):
    """Return (placement, width) with `word` applied, or None if it isn't an option."""
    word = word.lower()
    m = WIDTH.match(word)
    if word in PLACEMENTS and placement is None:
        return word, width
    if m and width is None:
        number, unit = int(m.group(1)), m.group(2) or 'px'
        if unit == '%':
            number = max(1, min(number, 100))
        return placement, f'{number}{unit}'
    return None


def _image_options(value):
    """Split 'kiln photo right 40%' into ('kiln photo', 'right', '40%').

    Options are read from the end, so image titles containing spaces still work.
    """
    words = value.split()
    placement = width = None
    while len(words) > 1:
        parsed = _parse_option(words[-1], placement, width)
        if parsed is None:
            break
        placement, width = parsed
        words.pop()
    return ' '.join(words), placement, width


def _options_only(text):
    """Parse a string made only of options; None if anything else is in it."""
    placement = width = None
    for word in text.split():
        parsed = _parse_option(word, placement, width)
        if parsed is None:
            return None
        placement, width = parsed
    return placement, width


def _placement_attrs(base, placement, width, default_float_width):
    """Class and style attributes for a placed, sized block."""
    if placement in ('left', 'right') and not width:
        width = default_float_width
    if placement == 'full':
        width = '100%'
    classes = [base]
    if placement:
        classes.append(f'align-{placement}')
    if width:
        classes.append('sized')
    style = f' style="width: {width}"' if width else ''
    return f'class="{" ".join(classes)}"{style}'


def _image(value, caption):
    img = Image.objects.filter(title=value).first()
    placement = width = None
    if not img:
        name, placement, width = _image_options(value)
        img = Image.objects.filter(title=name).first()
        if not img:
            return _missing('image', name)

    attrs = _placement_attrs('body-image', placement, width, DEFAULT_FLOAT_WIDTH)
    alt = _plain(caption) if caption else escape(img.title)
    return (f'<figure {attrs}>'
            f'<a href="{img.image.url}" target="_blank" rel="noopener">'
            f'<img src="{img.image.url}" alt="{alt}" loading="lazy"></a>'
            f'{_caption(caption) if caption else ""}</figure>')


def _image_row(names, caption):
    """Several images side by side, equal height, widths in proportion to their shapes."""
    items = []
    for name in [n.strip() for n in names.split(',') if n.strip()]:
        img = Image.objects.filter(title=name).first()
        if not img:
            items.append(f'<div class="row-item">{_missing("image", name)}</div>')
            continue
        try:
            ratio = img.image.width / img.image.height
        except Exception:  # unreadable file: fall back to square
            ratio = 1
        items.append(
            f'<div class="row-item" style="flex: {ratio:.4f} 1 0">'
            f'<a href="{img.image.url}" target="_blank" rel="noopener">'
            f'<img src="{img.image.url}" alt="{escape(img.title)}" loading="lazy"></a></div>')
    return (f'<figure class="body-image-row"><div class="row-items">{"".join(items)}</div>'
            f'{_caption(caption) if caption else ""}</figure>')


def _shortcode(kind, value, caption):
    if kind == 'image':
        return _image(value, caption)

    clip = Audio.objects.filter(title=value).first()
    if not clip or not clip.audio:
        return _missing('audio', value)
    return (f'<figure class="body-audio">'
            f'<audio controls preload="none" src="{clip.audio.url}"></audio>'
            f'{_caption(caption) if caption else ""}</figure>')


def _url_embed(url, placement=None, width=None):
    """Return embed HTML for a supported link, or None to leave it as text."""
    attrs = lambda base: _placement_attrs(base, placement, width, DEFAULT_VIDEO_FLOAT_WIDTH)

    m = YOUTUBE.match(url)
    if m:
        return _video(f'https://www.youtube-nocookie.com/embed/{m.group(1)}', attrs('body-video'))

    m = VIMEO.match(url)
    if m:
        src = f'https://player.vimeo.com/video/{m.group(1)}'
        if m.group(2):  # unlisted videos carry a privacy hash
            src += f'?h={m.group(2)}'
        return _video(src, attrs('body-video'))

    if SOUNDCLOUD.match(url):
        src = f'https://w.soundcloud.com/player/?url={quote(url, safe="")}&visual=false'
        return (f'<div {attrs("body-soundcloud")}><iframe src="{escape(src)}" '
                f'allow="autoplay" loading="lazy"></iframe></div>')

    return None


def _bare_url(m):
    options = _options_only(m.group(2) or '')
    if options is None:  # other words on the line: leave it as text
        return m.group(0)
    html = _url_embed(m.group(1), *options)
    return _block(html) if html else m.group(0)


def _block(html):
    return '\n\n' + html + '\n\n'


@register.filter
def render_body(text):
    # Only the site owner writes this through the admin, so raw HTML is allowed.
    # Browsers submit textareas with \r\n line endings; normalize so the
    # line-based patterns below match.
    text = (text or '').replace('\r\n', '\n').replace('\r', '\n')
    text = CLEAR.sub(lambda m: _block('<div class="body-clear"></div>'), text)
    text = SHORTCODE.sub(lambda m: _block(_shortcode(m.group(1), m.group(2), m.group(3))), text)
    text = IMAGE_ROW.sub(lambda m: _block(_image_row(m.group(1), m.group(2))), text)
    text = BARE_URL.sub(_bare_url, text)
    return mark_safe(markdown.markdown(text, extensions=['extra']))
