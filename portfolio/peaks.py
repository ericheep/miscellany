"""Waveform data for the audio player.

For each audio file, writes a small JSON file next to it in the media folder,
e.g. audio/field-recording.mp3 -> audio/field-recording.peaks.json, holding
per-slice minimum, maximum and RMS sample values on a -1..1 scale, the way a
DAW draws a waveform. The player fetches it to draw the waveform.
Requires ffmpeg on the server (sudo apt install ffmpeg).
"""
import json
import math
import operator
import os
import subprocess
from array import array

BINS = 800          # horizontal resolution of the waveform
SAMPLE_RATE = 8000  # enough detail for the drawing, small enough to process quickly
FULL_SCALE = 32768.0


def peaks_path(audio_path):
    return os.path.splitext(audio_path)[0] + '.peaks.json'


def compute_peaks(audio_path, bins=BINS):
    """Return {'min': [...], 'max': [...], 'rms': [...]} with values in -1..1."""
    result = subprocess.run(
        ['ffmpeg', '-v', 'error', '-i', audio_path,
         '-ac', '1', '-ar', str(SAMPLE_RATE), '-f', 's16le', '-'],
        capture_output=True, check=True, timeout=300,
    )
    samples = array('h')
    samples.frombytes(result.stdout[: len(result.stdout) // 2 * 2])

    mins, maxs, rmss = [], [], []
    if samples:
        size = max(1, len(samples) // bins)
        for i in range(bins):
            chunk = samples[i * size:(i + 1) * size]
            if not chunk:
                mins.append(0.0); maxs.append(0.0); rmss.append(0.0)
                continue
            mins.append(round(min(chunk) / FULL_SCALE, 3))
            maxs.append(round(max(chunk) / FULL_SCALE, 3))
            rmss.append(round(math.sqrt(sum(map(operator.mul, chunk, chunk)) / len(chunk)) / FULL_SCALE, 3))
    return {'version': 2, 'min': mins, 'max': maxs, 'rms': rmss}


def write_peaks(audio_path):
    """Compute and save the peaks file. Returns its path."""
    data = compute_peaks(audio_path)  # compute first, so a failure leaves no empty file
    out = peaks_path(audio_path)
    tmp = out + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(data, f, separators=(',', ':'))
    os.replace(tmp, out)
    return out


def has_peaks(audio_path):
    """True if a usable peaks file exists for this audio file."""
    try:
        with open(peaks_path(audio_path)) as f:
            data = json.load(f)
        return bool(data.get('max')) if isinstance(data, dict) else bool(data)
    except (OSError, ValueError):
        return False
