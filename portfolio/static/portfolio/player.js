// Replace the browser's default audio controls with a small player that
// matches the site: a dashed play button, a dotted track and the time.
(function () {
  'use strict';

  const players = [];

  function fmt(seconds) {
    if (!isFinite(seconds)) return '--:--';
    const s = Math.floor(seconds);
    return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
  }

  function enhance(audio) {
    audio.controls = false;
    audio.hidden = true;
    audio.preload = 'metadata'; // fetch just enough to show the length

    const player = document.createElement('div');
    player.className = 'player';

    const toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'player-toggle';
    toggle.textContent = 'play';

    const track = document.createElement('div');
    track.className = 'player-track';
    track.tabIndex = 0;
    track.setAttribute('role', 'slider');
    track.setAttribute('aria-label', 'Seek');
    track.setAttribute('aria-valuemin', '0');

    const fill = document.createElement('div');
    fill.className = 'player-fill';
    track.appendChild(fill);

    const time = document.createElement('span');
    time.className = 'player-time';
    time.textContent = '0:00 / --:--';

    player.append(toggle, track, time);
    audio.insertAdjacentElement('afterend', player);
    players.push(audio);

    function update() {
      const d = audio.duration;
      const pct = isFinite(d) && d > 0 ? (audio.currentTime / d) * 100 : 0;
      fill.style.width = `${pct}%`;
      time.textContent = `${fmt(audio.currentTime)} / ${fmt(d)}`;
      track.setAttribute('aria-valuemax', isFinite(d) ? Math.floor(d) : 0);
      track.setAttribute('aria-valuenow', Math.floor(audio.currentTime));
      track.setAttribute('aria-valuetext', time.textContent);
    }

    function seekTo(seconds) {
      if (!isFinite(audio.duration)) return;
      audio.currentTime = Math.max(0, Math.min(audio.duration, seconds));
      update();
    }

    toggle.addEventListener('click', () => {
      if (audio.paused) {
        players.forEach((other) => { if (other !== audio) other.pause(); });
        audio.play();
      } else {
        audio.pause();
      }
    });

    track.addEventListener('click', (e) => {
      const rect = track.getBoundingClientRect();
      seekTo(((e.clientX - rect.left) / rect.width) * audio.duration);
    });

    track.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') { seekTo(audio.currentTime + 5); e.preventDefault(); }
      if (e.key === 'ArrowLeft') { seekTo(audio.currentTime - 5); e.preventDefault(); }
      if (e.key === ' ' || e.key === 'Enter') { toggle.click(); e.preventDefault(); }
    });

    audio.addEventListener('play', () => { toggle.textContent = 'pause'; player.classList.add('playing'); });
    audio.addEventListener('pause', () => { toggle.textContent = 'play'; player.classList.remove('playing'); });
    audio.addEventListener('ended', () => { audio.currentTime = 0; update(); });
    ['loadedmetadata', 'durationchange', 'timeupdate'].forEach((ev) => audio.addEventListener(ev, update));
    audio.addEventListener('error', () => { time.textContent = 'unavailable'; toggle.disabled = true; });

    update();
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('#page audio').forEach(enhance);
  });
})();
