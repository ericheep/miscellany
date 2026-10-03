"""Turn files dropped into the admin's Body box into Image / Audio records.

Images are resized and re-saved, which drops EXIF metadata (including GPS
location). Titles are slugs of the filename, made unique with a number.
"""
import os
from io import BytesIO

from django.core.files.base import ContentFile
from django.utils.text import slugify
from PIL import Image as PILImage, ImageOps, UnidentifiedImageError

from .models import Audio, Image

try:  # iPhone HEIC photos, if pillow-heif is installed
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

MAX_IMAGE_SIDE = 2000
JPEG_QUALITY = 85
AUDIO_EXTENSIONS = {'.mp3', '.m4a', '.aac', '.wav', '.ogg', '.oga', '.flac'}


class UploadError(Exception):
    pass


def unique_title(model, filename):
    base = slugify(os.path.splitext(filename)[0])[:180] or 'file'
    title, n = base, 2
    while model.objects.filter(title=title).exists():
        title = f'{base}-{n}'
        n += 1
    return title


def process_image(uploaded):
    """Return (bytes, extension) for a resized copy with metadata removed."""
    try:
        img = PILImage.open(uploaded)
        img.load()
    except (UnidentifiedImageError, OSError):
        raise UploadError('not a readable image')

    if getattr(img, 'is_animated', False):
        # Re-encoding would lose the animation; keep the original file.
        uploaded.seek(0)
        return uploaded.read(), os.path.splitext(uploaded.name)[1].lower() or '.gif'

    img = ImageOps.exif_transpose(img)  # apply phone rotation before EXIF is dropped
    img.thumbnail((MAX_IMAGE_SIDE, MAX_IMAGE_SIDE))

    buf = BytesIO()
    has_alpha = img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info)
    if has_alpha:
        img.save(buf, 'PNG', optimize=True)
        ext = '.png'
    else:
        img.convert('RGB').save(buf, 'JPEG', quality=JPEG_QUALITY, optimize=True, progressive=True)
        ext = '.jpg'
    return buf.getvalue(), ext


def save_upload(uploaded):
    """Store an uploaded file and return the shortcode to insert in the body."""
    ext = os.path.splitext(uploaded.name)[1].lower()
    content_type = getattr(uploaded, 'content_type', '') or ''

    if ext in AUDIO_EXTENSIONS or content_type.startswith('audio/'):
        title = unique_title(Audio, uploaded.name)
        clip = Audio(title=title)
        clip.audio.save(f'{title}{ext}', uploaded, save=True)
        return f'{{audio: {title}}}'

    data, out_ext = process_image(uploaded)
    title = unique_title(Image, uploaded.name)
    img = Image(title=title)
    img.image.save(f'{title}{out_ext}', ContentFile(data), save=True)
    return f'{{image: {title}}}'
