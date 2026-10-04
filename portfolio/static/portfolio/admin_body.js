// Drag-and-drop / paste uploads and a Preview button for the Work "Body" field.
(function () {
  'use strict';

  function csrfToken() {
    const el = document.querySelector('input[name=csrfmiddlewaretoken]');
    return el ? el.value : '';
  }

  // Insert text on its own line at the cursor.
  function insertLine(ta, text) {
    const v = ta.value;
    let before = v.slice(0, ta.selectionStart);
    let after = v.slice(ta.selectionEnd);
    if (before && !before.endsWith('\n')) before += '\n';
    let insert = text + '\n';
    if (after && !after.startsWith('\n')) insert += '\n';
    ta.value = before + insert + after;
    const pos = before.length + insert.length;
    ta.setSelectionRange(pos, pos);
    ta.focus();
  }

  function replaceText(ta, from, to) {
    const start = ta.selectionStart;
    const end = ta.selectionEnd;
    const at = ta.value.indexOf(from);
    if (at === -1) { insertLine(ta, to); return; }
    ta.value = ta.value.slice(0, at) + to + ta.value.slice(at + from.length);
    const shift = to.length - from.length;
    const fix = (p) => (p > at ? p + shift : p);
    ta.setSelectionRange(fix(start), fix(end));
  }

  function setup(ta) {
    let pending = 0;

    async function upload(file) {
      const id = Math.random().toString(36).slice(2, 7);
      const placeholder = `{uploading ${file.name} ${id}…}`;
      insertLine(ta, placeholder);
      pending += 1;

      const fd = new FormData();
      fd.append('file', file);
      let result;
      try {
        const r = await fetch(ta.dataset.uploadUrl, {
          method: 'POST',
          body: fd,
          headers: { 'X-CSRFToken': csrfToken() },
          credentials: 'same-origin',
        });
        const data = await r.json().catch(() => ({ error: `server returned ${r.status}` }));
        result = r.ok ? data.shortcode : `{upload failed: ${file.name}: ${data.error}}`;
      } catch (e) {
        result = `{upload failed: ${file.name}: network error}`;
      }
      replaceText(ta, placeholder, result);
      pending -= 1;
    }

    function uploadAll(files) {
      Array.from(files).forEach(upload);
    }

    ta.addEventListener('dragover', (e) => {
      if (e.dataTransfer && Array.from(e.dataTransfer.types).includes('Files')) {
        e.preventDefault();
        ta.classList.add('body-dragging');
      }
    });
    ta.addEventListener('dragleave', () => ta.classList.remove('body-dragging'));
    ta.addEventListener('drop', (e) => {
      ta.classList.remove('body-dragging');
      if (!e.dataTransfer || !e.dataTransfer.files.length) return;
      e.preventDefault();
      ta.focus();
      uploadAll(e.dataTransfer.files);
    });
    ta.addEventListener('paste', (e) => {
      const files = e.clipboardData && e.clipboardData.files;
      if (files && files.length) {
        e.preventDefault();
        uploadAll(files);
      }
    });

    const form = ta.closest('form');
    if (form) {
      form.addEventListener('submit', (e) => {
        if (pending > 0) {
          e.preventDefault();
          window.alert('Still uploading. Save again in a moment.');
        }
      });
    }

    // Preview button + hint under the textarea
    const bar = document.createElement('div');
    bar.className = 'body-toolbar';

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'button';
    btn.textContent = 'Preview';
    btn.addEventListener('click', () => {
      const f = document.createElement('form');
      f.method = 'post';
      f.action = ta.dataset.previewUrl;
      f.target = '_blank';
      const add = (name, value) => {
        const i = document.createElement('input');
        i.type = 'hidden';
        i.name = name;
        i.value = value;
        f.appendChild(i);
      };
      add('csrfmiddlewaretoken', csrfToken());
      add('body', ta.value);
      const title = document.getElementById('id_title');
      if (title) add('title', title.value);
      const created = document.getElementById('id_created_date');
      if (created) add('created_date', created.value);
      document.body.appendChild(f);
      f.submit();
      f.remove();
    });

    const hint = document.createElement('span');
    hint.className = 'body-hint';
    hint.textContent = 'Drag or paste images and audio into the box. Options: {image: name right 40% | Caption} (left, right, center, full; 40% or 300px). {clear} ends a wrap.';

    bar.append(btn, hint);

    // The admin lays a field's contents out in a row, so stack the toolbar
    // above the textarea inside a wrapper of our own.
    const wrap = document.createElement('div');
    wrap.className = 'body-editor-wrap';
    ta.parentNode.insertBefore(wrap, ta);
    wrap.append(bar, ta);
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('textarea[data-upload-url]').forEach(setup);
  });
})();
