"""Create grid thumbnails for every work's main image.

    python manage.py make_thumbnails          # only missing or out-of-date ones
    python manage.py make_thumbnails --all    # redo every one
"""
import os

from django.core.management.base import BaseCommand

from portfolio.models import Work
from portfolio.thumbnails import make_thumbnails, thumbs_current


class Command(BaseCommand):
    help = "Generate 4:3 WebP thumbnails for each work's main image."

    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true', help='Regenerate existing thumbnails too.')

    def handle(self, *args, **options):
        made = skipped = failed = 0
        saved_bytes = 0
        for work in Work.objects.exclude(mainImage=''):
            path = work.mainImage.path
            if not os.path.exists(path):
                self.stderr.write(f'missing file for {work}: {path}')
                failed += 1
                continue
            if not options['all'] and thumbs_current(path):
                skipped += 1
                continue
            try:
                written = make_thumbnails(path)
                small = os.path.getsize(written[0])
                saved_bytes += os.path.getsize(path) - small
                made += 1
                self.stdout.write(f'ok: {work}  ({os.path.getsize(path) // 1024} KB -> {small // 1024} KB)')
            except Exception as e:
                failed += 1
                self.stderr.write(f'failed: {work}: {e}')
        self.stdout.write(f'{made} made, {skipped} already current, {failed} failed; '
                          f'about {saved_bytes // (1024 * 1024)} MB less on the front page')
