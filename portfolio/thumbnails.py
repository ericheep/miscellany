"""Small, pre-cropped thumbnails for the works grid.

For a main image like media/images/kiln.jpg this writes, next to it:

    images/kiln.thumb-480.webp
    images/kiln.thumb-960.webp    (for high-resolution screens)

Each is cropped to the grid's 4:3 shape around the center, so no bytes are
spent on parts the grid would hide. No database fields are involved: the
template looks for these files and falls back to the original if missing.
"""
import os

from PIL import Image as PILImage, ImageOps

WIDTHS = (480, 960)
ASPECT = (4, 3)
QUALITY = 80


def thumb_path(image_path, width):
    return f'{os.path.splitext(image_path)[0]}.thumb-{width}.webp'


def thumb_url(field_file, width):
    """URL of a thumbnail if it exists and is up to date, else None."""
    try:
        path = thumb_path(field_file.path, width)
        if os.path.getmtime(path) >= os.path.getmtime(field_file.path):
            return f'{os.path.splitext(field_file.url)[0]}.thumb-{width}.webp'
    except (OSError, ValueError):
        pass
    return None


def thumbs_current(image_path):
    try:
        source = os.path.getmtime(image_path)
        return all(os.path.getmtime(thumb_path(image_path, w)) >= source for w in WIDTHS)
    except OSError:
        return False


def make_thumbnails(image_path):
    """Write all thumbnail sizes for one image. Returns the paths written."""
    written = []
    with PILImage.open(image_path) as src:
        src.seek(0)  # first frame of an animated image
        img = ImageOps.exif_transpose(src)  # turn phone photos upright
        img = img.convert('RGBA' if 'A' in img.getbands() else 'RGB')

        for width in WIDTHS:
            height = round(width * ASPECT[1] / ASPECT[0])
            # never enlarge: a small original makes a smaller thumbnail
            scale = min(1.0, img.width / width, img.height / height)
            size = (max(1, round(width * scale)), max(1, round(height * scale)))
            thumb = ImageOps.fit(img, size, method=PILImage.LANCZOS, centering=(0.5, 0.5))

            out = thumb_path(image_path, width)
            tmp = out + '.tmp'
            thumb.save(tmp, 'WEBP', quality=QUALITY, method=6)
            os.replace(tmp, out)
            written.append(out)
    return written
