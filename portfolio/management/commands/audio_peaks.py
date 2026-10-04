"""Create waveform files for audio uploaded before waveforms existed.

    python manage.py audio_peaks          # only files missing a waveform
    python manage.py audio_peaks --all    # redo every file
"""
import os

from django.core.management.base import BaseCommand

from portfolio.models import Audio
from portfolio.peaks import peaks_path, write_peaks


class Command(BaseCommand):
    help = 'Generate waveform (.peaks.json) files for uploaded audio.'

    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true', help='Regenerate existing waveforms too.')

    def handle(self, *args, **options):
        done = skipped = failed = 0
        for clip in Audio.objects.exclude(audio=''):
            path = clip.audio.path
            if not os.path.exists(path):
                self.stderr.write(f'missing file: {path}')
                failed += 1
                continue
            if not options['all'] and os.path.exists(peaks_path(path)):
                skipped += 1
                continue
            try:
                write_peaks(path)
                done += 1
                self.stdout.write(f'ok: {clip}')
            except Exception as e:  # keep going on a bad file
                failed += 1
                self.stderr.write(f'failed: {clip}: {e}')
        self.stdout.write(f'{done} created, {skipped} already had one, {failed} failed')
