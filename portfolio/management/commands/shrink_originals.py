"""One-time cleanup of images uploaded before uploads were processed.

For every image file (the Images library and each work's main image) this:
  - turns phone photos upright (applies the EXIF rotation),
  - removes metadata, including GPS location,
  - shrinks anything larger than 2000px on its longest side.

Files keep their names and formats, so nothing in the database changes.
It edits files in place: run your backup script first.

    python manage.py shrink_originals --dry-run   # list what would change, touch nothing
    python manage.py shrink_originals             # do it
"""
import os

from django.core.management.base import BaseCommand
from PIL import Image as PILImage, ImageOps

from portfolio.models import Image, Work

MAX_SIDE = 2000
JPEG_QUALITY = 85
FORMATS = {'JPEG', 'PNG', 'WEBP'}


def needs_work(img):
    exif = img.getexif()
    return max(img.size) > MAX_SIDE or len(exif) > 0


def process(path):
    """Rewrite one file in place. Returns (old_bytes, new_bytes)."""
    old = os.path.getsize(path)
    with PILImage.open(path) as src:
        fmt = src.format
        icc = src.info.get('icc_profile')  # keep color accuracy
        img = ImageOps.exif_transpose(src)
        img.thumbnail((MAX_SIDE, MAX_SIDE), PILImage.LANCZOS)

        options = {'icc_profile': icc} if icc else {}
        if fmt == 'JPEG':
            img = img.convert('RGB')
            options.update(quality=JPEG_QUALITY, optimize=True, progressive=True)
        elif fmt == 'PNG':
            options.update(optimize=True)
        elif fmt == 'WEBP':
            options.update(quality=JPEG_QUALITY, method=6)

        tmp = path + '.tmp'
        img.save(tmp, fmt, **options)  # no exif= argument, so metadata is dropped
    os.replace(tmp, path)
    return old, os.path.getsize(path)


class Command(BaseCommand):
    help = 'Rotate, strip metadata (including GPS) and shrink old uploaded images, in place.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Only list what would change.')

    def handle(self, *args, **options):
        paths = set()
        for img in Image.objects.exclude(image=''):
            paths.add(img.image.path)
        for work in Work.objects.exclude(mainImage=''):
            paths.add(work.mainImage.path)

        changed = skipped = failed = 0
        before = after = 0
        for path in sorted(paths):
            name = os.path.basename(path)
            if not os.path.exists(path):
                self.stderr.write(f'missing: {path}')
                failed += 1
                continue
            try:
                with PILImage.open(path) as img:
                    if img.format not in FORMATS or getattr(img, 'is_animated', False):
                        skipped += 1
                        continue
                    if not needs_work(img):
                        skipped += 1
                        continue
                    info = f'{img.size[0]}x{img.size[1]}, {"has" if len(img.getexif()) else "no"} metadata'
                if options['dry_run']:
                    self.stdout.write(f'would fix: {name} ({info}, {os.path.getsize(path) // 1024} KB)')
                    changed += 1
                    continue
                old, new = process(path)
                before += old
                after += new
                changed += 1
                self.stdout.write(f'fixed: {name} ({info}): {old // 1024} KB -> {new // 1024} KB')
            except Exception as e:
                failed += 1
                self.stderr.write(f'failed: {name}: {e}')

        verb = 'would fix' if options['dry_run'] else 'fixed'
        summary = f'{changed} {verb}, {skipped} already fine or skipped, {failed} failed'
        if not options['dry_run'] and changed:
            summary += f'; {before // (1024 * 1024)} MB -> {after // (1024 * 1024)} MB'
            summary += '\nNow run: python manage.py make_thumbnails'
        self.stdout.write(summary)
