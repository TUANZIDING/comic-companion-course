/* 教学示例，非原始制作记录。仅本地存储主题与勾选进度。 */
(() => {
  'use strict';
  const root = document.documentElement;
  const safeRead = key => { try { return localStorage.getItem(key); } catch { return null; } };
  const safeWrite = (key, value) => { try { localStorage.setItem(key, value); } catch { /* Private browsing still works without persistence. */ } };
  const themeButton = document.querySelector('[data-theme-toggle]');
  const preferred = safeRead('comic-course-theme-v1');
  root.dataset.theme = preferred === 'dark' || preferred === 'light' ? preferred : (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  function themeLabel() { if (themeButton) { themeButton.textContent = root.dataset.theme === 'dark' ? '切换浅色' : '切换深色'; themeButton.setAttribute('aria-pressed', String(root.dataset.theme === 'dark')); } }
  themeLabel();
  themeButton?.addEventListener('click', () => { root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark'; safeWrite('comic-course-theme-v1', root.dataset.theme); themeLabel(); });
  const status = document.querySelector('[data-status]');
  let statusTimer;
  function announce(message) { if (!status) return; status.textContent = message; clearTimeout(statusTimer); statusTimer = setTimeout(() => { status.textContent = ''; }, 4000); }
  function fallbackCopy(text) {
    const area = document.createElement('textarea'); area.value = text; area.setAttribute('aria-label', '复制提示词'); area.style.position = 'fixed'; area.style.left = '-10000px';
    document.body.append(area); area.focus(); area.select(); area.setSelectionRange(0, text.length);
    let success = false; try { success = document.execCommand('copy'); } finally { area.remove(); }
    return success;
  }
  document.querySelectorAll('[data-copy]').forEach(button => {
    button.addEventListener('click', async () => {
      const source = document.getElementById(button.dataset.copy); if (!source) { announce('未找到提示词'); return; }
      const text = source.textContent; let copied = false;
      try { if (navigator.clipboard?.writeText && window.isSecureContext) { await navigator.clipboard.writeText(text); copied = true; } } catch { /* Safari permissions or insecure context: use selection-based copy. */ }
      if (!copied) copied = fallbackCopy(text);
      if (copied) { button.textContent = '已复制'; announce('已复制提示词'); setTimeout(() => { button.textContent = '复制提示词'; }, 4000); }
      else { button.textContent = '请选中文字复制'; announce('浏览器限制复制，请选中提示词后复制'); }
      button.focus();
    });
  });
  let completed = [];
  try { const saved = JSON.parse(safeRead('comic-course-progress-v1') || '[]'); if (Array.isArray(saved)) completed = [...new Set(saved.filter(x => Number.isInteger(x) && x >= 0 && x < 12))]; } catch { /* Corrupt local data does not stop navigation. */ }
  function progress() {
    document.querySelectorAll('[data-progress-text]').forEach(node => { node.textContent = `${completed.length} / 12 课已勾选`; });
    document.querySelectorAll('[data-progress-fill]').forEach(node => { node.style.width = `${completed.length / 12 * 100}%`; });
    document.querySelectorAll('[data-progress-bar]').forEach(node => node.setAttribute('aria-valuenow', String(completed.length)));
  }
  const complete = document.querySelector('[data-complete]');
  if (complete) {
    const lesson = Number(complete.dataset.complete); complete.checked = completed.includes(lesson);
    complete.addEventListener('change', () => { completed = complete.checked ? [...new Set([...completed, lesson])] : completed.filter(x => x !== lesson); safeWrite('comic-course-progress-v1', JSON.stringify(completed)); progress(); announce(complete.checked ? '本课已勾选完成' : '已取消本课完成标记'); });
  }
  document.querySelector('[data-reset-progress]')?.addEventListener('click', () => { completed = []; safeWrite('comic-course-progress-v1', '[]'); if (complete) complete.checked = false; progress(); announce('本机学习进度已重置'); });
  progress();
  const dialog = document.querySelector('[data-gallery-dialog]');
  const galleryImage = dialog?.querySelector('img'); const caption = dialog?.querySelector('[data-dialog-caption]'); let returnFocus;
  document.querySelectorAll('[data-enlarge]').forEach(button => button.addEventListener('click', () => {
    if (!dialog || !galleryImage) return; const image = button.querySelector('img'); if (!image) return;
    galleryImage.src = image.src; galleryImage.alt = image.alt; if (caption) caption.textContent = button.dataset.caption || image.alt; returnFocus = button; dialog.showModal(); dialog.querySelector('[data-close-dialog]')?.focus();
  }));
  dialog?.addEventListener('keydown', event => {
    if (event.key !== 'Tab') return;
    const controls = [...dialog.querySelectorAll('button, a[href], input, select, textarea, [tabindex]:not([tabindex="-1"])')].filter(node => !node.disabled && node.getClientRects().length);
    const first = controls[0], last = controls[controls.length - 1];
    if (!first) { event.preventDefault(); return; }
    if ((event.shiftKey && document.activeElement === first) || (!event.shiftKey && document.activeElement === last) || !dialog.contains(document.activeElement)) {
      event.preventDefault(); (event.shiftKey ? last : first).focus();
    }
  });
  dialog?.querySelector('[data-close-dialog]')?.addEventListener('click', () => dialog.close());
  dialog?.addEventListener('click', event => { const box = dialog.getBoundingClientRect(); if (event.target === dialog && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) dialog.close(); });
  dialog?.addEventListener('close', () => { if (galleryImage) galleryImage.removeAttribute('src'); returnFocus?.focus(); });
})();
