// Replace the browser's default audio controls with a small player that
// matches the site, all on one row: a dashed play button, the track name,
// a waveform you click to seek (or a dotted track without one) and the time.
(function () {
  'use strict';

  const players = [];

  // false: true levels, like a DAW (quiet recordings look small).
  // true: scale each waveform so its loudest peak fills the height.
  const NORMALIZE = false;

  function fmt(seconds) {
    if (!isFinite(seconds)) return '--:--';
    const s = Math.floor(seconds);
    return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
  }

  function sourceUrl(audio) {
    const src = audio.getAttribute('src') || (audio.querySelector('source') || {}).src || '';
    return src.split('#')[0].split('?')[0];
  }

  function fileName(url) {
    try {
      return decodeURIComponent(url.split('/').pop()).replace(/\.[^.]+$/, '');
    } catch (e) {
      return '';
    }
  }

  function el(tag, className) {
    const node = document.createElement(tag);
    node.className = className;
    return node;
  }

  function enhance(audio) {
    audio.controls = false;
    audio.hidden = true;
    audio.preload = 'metadata'; // fetch just enough to show the length

    const url = sourceUrl(audio);
    const player = el('div', 'player');

    // Track name, unless the old layout already shows a title
    const oldBlock = audio.closest('.audio');
    const name = el('div', 'player-name');
    if (!(oldBlock && oldBlock.querySelector('.audio-title'))) {
      name.textContent = fileName(url);
      name.title = name.textContent;
    }

    // Seek area: the waveform, or the dotted track when there's no waveform file
    const seek = el('div', 'player-seek');
    seek.tabIndex = 0;
    seek.setAttribute('role', 'slider');
    seek.setAttribute('aria-label', name.textContent ? `Seek ${name.textContent}` : 'Seek');
    seek.setAttribute('aria-valuemin', '0');

    const wave = el('canvas', 'player-wave');

    const toggle = el('button', 'player-toggle');
    toggle.type = 'button';
    toggle.textContent = 'play';

    const track = el('div', 'player-track');
    const fill = el('div', 'player-fill');
    track.appendChild(fill);
    seek.append(wave, track);

    const time = el('span', 'player-time');
    time.textContent = '0:00 / --:--';

    player.append(toggle, name, seek, time);
    audio.insertAdjacentElement('afterend', player);
    players.push(audio);

    let peaks = null;

    function progress() {
      const d = audio.duration;
      return isFinite(d) && d > 0 ? audio.currentTime / d : 0;
    }

    function drawWave() {
      if (!peaks) return;
      const ratio = window.devicePixelRatio || 1;
      const w = wave.clientWidth;
      const h = wave.clientHeight;
      if (!w || !h) return;
      wave.width = Math.round(w * ratio);
      wave.height = Math.round(h * ratio);
      const ctx = wave.getContext('2d');
      ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
      ctx.clearRect(0, 0, w, h);

      // Draw like a DAW: for each pixel column, the min..max peak envelope
      // around a center line, with the RMS (average level) darker inside it.
      const n = peaks.max.length;
      const loudest = Math.max(...peaks.max, ...peaks.min.map((v) => -v)) || 1;
      const mid = (h / 2) * (NORMALIZE ? 1 / loudest : 1);
      const center = h / 2;
      const px = 1 / ratio;                  // one device pixel
      const cols = Math.round(w * ratio);
      const played = progress() * w;

      for (let c = 0; c < cols; c++) {
        const x = c * px;
        const a = Math.floor((c / cols) * n);
        const b = Math.max(a + 1, Math.floor(((c + 1) / cols) * n));
        let lo = 0, hi = 0, rms = 0;
        for (let i = a; i < b && i < n; i++) {
          if (peaks.min[i] < lo) lo = peaks.min[i];
          if (peaks.max[i] > hi) hi = peaks.max[i];
          if (peaks.rms[i] > rms) rms = peaks.rms[i];
        }
        const isPlayed = x < played;
        // peak envelope
        ctx.fillStyle = isPlayed ? '#666' : '#ccc';
        const top = center - hi * mid;
        ctx.fillRect(x, top, px, Math.max(px, (center - lo * mid) - top));
        // RMS core
        ctx.fillStyle = isPlayed ? '#000' : '#999';
        ctx.fillRect(x, center - rms * mid, px, Math.max(px, rms * mid * 2));
      }

      // center line and playhead
      ctx.fillStyle = '#999';
      ctx.fillRect(0, center - px / 2, w, px);
      if (played > 0) {
        ctx.fillStyle = '#000';
        ctx.fillRect(Math.min(played, w - 1), 0, 1, h);
      }
    }

    function update() {
      const d = audio.duration;
      fill.style.width = `${progress() * 100}%`;
      time.textContent = `${fmt(audio.currentTime)} / ${fmt(d)}`;
      seek.setAttribute('aria-valuemax', isFinite(d) ? Math.floor(d) : 0);
      seek.setAttribute('aria-valuenow', Math.floor(audio.currentTime));
      seek.setAttribute('aria-valuetext', time.textContent);
      drawWave();
    }

    function seekTo(seconds) {
      if (!isFinite(audio.duration)) return;
      audio.currentTime = Math.max(0, Math.min(audio.duration, seconds));
      update();
    }

    function seekFromClick(e, target) {
      const rect = target.getBoundingClientRect();
      seekTo(((e.clientX - rect.left) / rect.width) * audio.duration);
    }

    toggle.addEventListener('click', () => {
      if (audio.paused) {
        players.forEach((other) => { if (other !== audio) other.pause(); });
        audio.play();
      } else {
        audio.pause();
      }
    });

    seek.addEventListener('click', (e) => seekFromClick(e, seek));

    seek.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') { seekTo(audio.currentTime + 5); e.preventDefault(); }
      if (e.key === 'ArrowLeft') { seekTo(audio.currentTime - 5); e.preventDefault(); }
      if (e.key === ' ' || e.key === 'Enter') { toggle.click(); e.preventDefault(); }
    });

    audio.addEventListener('play', () => { toggle.textContent = 'pause'; player.classList.add('playing'); });
    audio.addEventListener('pause', () => { toggle.textContent = 'play'; player.classList.remove('playing'); });
    audio.addEventListener('ended', () => { audio.currentTime = 0; update(); });
    ['loadedmetadata', 'durationchange', 'timeupdate'].forEach((ev) => audio.addEventListener(ev, update));
    audio.addEventListener('error', () => { time.textContent = 'unavailable'; toggle.disabled = true; });
    window.addEventListener('resize', drawWave);

    // Waveform data lives next to the audio file: foo.mp3 -> foo.peaks.json
    if (url) {
      fetch(url.replace(/\.[^./]+$/, '.peaks.json'))
        .then((r) => (r.ok ? r.json() : null))
        .then((data) => {
          if (Array.isArray(data) && data.length) {
            // older single-list format: treat each value as a symmetric level
            data = { min: data.map((v) => -v), max: data, rms: data.map((v) => v * 0.7) };
          }
          if (data && Array.isArray(data.max) && data.max.length) {
            peaks = data;
            player.classList.add('has-wave');
            drawWave();
          }
        })
        .catch(() => {});
    }

    update();
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('#page audio').forEach(enhance);
  });
})();
