(() => {
  'use strict';
  const lab = document.getElementById('sdf-lab');
  if (lab) {
    const n = 24, range = 4;
    const mask = new Float64Array(n * n), field = new Float64Array(n * n);
    // Positive inside an analytic annulus. Both textures use the same lattice.
    const distance = (x, y) => 1.45 - Math.abs(Math.hypot(x - 12, y - 12) - 7.3);
    for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) {
      const i = y * n + x;
      field[i] = Math.max(-range, Math.min(range, distance(x + .5, y + .5)));
      let coverage = 0;
      for (let sy = 0; sy < 4; sy++) for (let sx = 0; sx < 4; sx++)
        coverage += distance(x + (sx + .5) / 4, y + (sy + .5) / 4) >= 0 ? 1 / 16 : 0;
      mask[i] = coverage;
    }
    const at = (a, x, y) => a[Math.max(0, Math.min(n - 1, y)) * n + Math.max(0, Math.min(n - 1, x))];
    function bilinear(a, x, y) {
      const ix = Math.floor(x), iy = Math.floor(y), tx = x - ix, ty = y - iy;
      return (at(a, ix, iy) * (1 - tx) + at(a, ix + 1, iy) * tx) * (1 - ty)
        + (at(a, ix, iy + 1) * (1 - tx) + at(a, ix + 1, iy + 1) * tx) * ty;
    }
    const smooth = (lo, hi, x) => {
      const t = Math.max(0, Math.min(1, (x - lo) / (hi - lo)));
      return t * t * (3 - 2 * t);
    };
    const size = document.getElementById('lab-size'), outline = document.getElementById('lab-outline');
    const canvases = ['lab-nearest', 'lab-linear', 'lab-sdf'].map(id => document.getElementById(id));
    function draw() {
      const pixels = Number(size.value), border = Number(outline.value), margin = (280 - pixels) / 2;
      const width = .75 * n / pixels;
      for (let mode = 0; mode < canvases.length; mode++) {
        const ctx = canvases[mode].getContext('2d'), image = ctx.createImageData(280, 280);
        for (let py = 0; py < 280; py++) for (let px = 0; px < 280; px++) {
          const i = (py * 280 + px) * 4;
          let alpha = 0, ink = [21, 67, 75];
          if (px >= margin && py >= margin && px < margin + pixels && py < margin + pixels) {
            const x = (px + .5 - margin) * n / pixels - .5, y = (py + .5 - margin) * n / pixels - .5;
            if (mode === 0) alpha = at(mask, Math.round(x), Math.round(y));
            else if (mode === 1) alpha = bilinear(mask, x, y);
            else {
              const d = bilinear(field, x, y);
              const face = smooth(-width, width, d), whole = smooth(-width, width, d + border);
              alpha = whole;
              if (whole > 0) {
                const mix = face / whole, edge = [214, 139, 50];
                ink = ink.map((v, k) => v * mix + edge[k] * (1 - mix));
              }
            }
          }
          for (let k = 0; k < 3; k++) image.data[i + k] = Math.round(250 * (1 - alpha) + ink[k] * alpha);
          image.data[i + 3] = 255;
        }
        ctx.putImageData(image, 0, 0);
      }
      document.getElementById('lab-size-value').textContent = pixels + ' px';
      document.getElementById('lab-outline-value').textContent = border.toFixed(1) + ' 单位';
      document.getElementById('lab-status').textContent = '源采样网格 24 × 24；显示 ' + pixels + ' × ' + pixels
        + ' 像素；SDF 描边向外扩展 ' + border.toFixed(1) + ' 个源网格单位。前两幅图不增加描边。';
    }
    size.addEventListener('input', draw); outline.addEventListener('input', draw); draw();
  }

  const questions = [...document.querySelectorAll('details.faq-question')];
  const filter = document.getElementById('faq-filter'), status = document.getElementById('faq-filter-status');
  if (filter) {
    filter.addEventListener('input', () => {
      const query = filter.value.trim().toLowerCase(), terms = query.split(/\s+/).filter(Boolean);
      let matches = 0;
      for (const item of questions) {
        const text = item.textContent.toLowerCase();
        item.hidden = !terms.every(term => text.includes(term));
        if (!item.hidden) { matches++; if (query) item.open = true; }
      }
      status.textContent = query ? '找到 ' + matches + ' / ' + questions.length + ' 个问题'
        : '共 ' + questions.length + ' 个问题；可按问题或答案中的关键词筛选。';
    });
    document.getElementById('faq-expand').addEventListener('click', () => questions.filter(x => !x.hidden).forEach(x => x.open = true));
    document.getElementById('faq-collapse').addEventListener('click', () => questions.filter(x => !x.hidden).forEach(x => x.open = false));
    status.textContent = '共 ' + questions.length + ' 个问题；可按问题或答案中的关键词筛选。';
  }
  const revealHash = () => {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = id ? document.getElementById(id) : null;
    if (target?.matches('details')) target.open = true;
  };
  addEventListener('hashchange', revealHash); revealHash();
  let printState;
  addEventListener('beforeprint', () => {
    printState = [...document.querySelectorAll('article details')].map(x => [x, x.open, x.hidden]);
    printState.forEach(([x]) => { x.open = true; x.hidden = false; });
  });
  addEventListener('afterprint', () => printState?.forEach(([x, open, hidden]) => { x.open = open; x.hidden = hidden; }));
})();
