/* ── MAIN JS ── */
const SHEETS_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ48SSesrIXD0_IXpb5M_hGhrxa4QTSzbggIzoCulVMD02SeU_NzA7lcLy4tHrnEjURTqDQs7u4gL1b/pub?gid=0&single=true&output=csv";
window.DYNAMIC_DATA = null;

// Simple CSV Parser for Google Sheets output
function parseCSV(text) {
  const lines = text.split(/\r?\n/).filter(l => l.trim() !== "");
  const result = { male: {}, female: {} };
  
  // Skip header
  for (let i = 1; i < lines.length; i++) {
    // Basic regex to handle commas inside quotes
    const matches = lines[i].match(/(".*?"|[^",\s]+)(?=\s*,|\s*$)/g);
    if (!matches || matches.length < 5) continue;
    
    const [gender, category, title, desc, url] = matches.map(s => s.replace(/^"|"$/g, '').trim());
    
    if (!result[gender][category]) {
      result[gender][category] = { title, desc, photos: [] };
    }
    result[gender][category].photos.push(url);
  }
  return result;
}

async function fetchPhotosData() {
  const grid = document.getElementById('catGrid');
  if (grid && !window.DYNAMIC_DATA) {
    grid.innerHTML = '<div class="skeleton-item"></div>'.repeat(6);
  }
  try {
    const response = await fetch(SHEETS_CSV_URL);
    const text = await response.text();
    window.DYNAMIC_DATA = parseCSV(text);
    
    // If we're on a category page, re-build the grid with fresh data
    if (typeof window.currentGender !== 'undefined' && typeof window.buildGrid === 'function') {
      window.buildGrid(window.currentGender);
    }
  } catch (err) {
    console.error("Failed to fetch sheets data:", err);
  }
}

function toggleMenu() {
  const m = document.getElementById('mobileMenu');
  if (!m) return;
  const open = m.style.display === 'flex';
  m.style.display = open ? 'none' : 'flex';
}

window.appSwitchGender = function(gender) {
  if (typeof window.currentGender !== 'undefined' && document.getElementById('catGrid')) {
    if (gender === window.currentGender) return;
    
    let path = window.location.pathname;
    let file = path.split('/').pop();
    if (!file || file === '') file = 'index.html';
    
    if (gender === 'male') {
      if (!file.includes('-male.html')) {
        file = file.replace('.html', '-male.html');
      }
    } else {
      if (file.includes('-male.html')) {
        file = file.replace('-male.html', '.html');
      }
    }
    
    const grid = document.getElementById('catGrid');
    if(grid) {
      grid.style.transition='opacity 0.2s'; 
      grid.style.opacity='0';
    }
    
    setTimeout(() => {
      window.location.href = file + window.location.search + window.location.hash;
    }, 200);
  } else {
    document.querySelectorAll('.gender-tab').forEach(t => t.classList.remove('active'));
    let target = document.querySelector(`.gender-tab[data-gender="${gender}"]`);
    if(target) target.classList.add('active');

    const female = document.getElementById('female-panel');
    const male   = document.getElementById('male-panel');
    if (female && male) {
      if (gender === 'female') {
        female.style.display = 'contents';
        male.style.display   = 'none';
      } else {
        female.style.display = 'none';
        male.style.display   = 'contents';
      }
    }
    appMoveGenderSlider(gender);
  }
}

window.appMoveGenderSlider = function(gender) {
  const toggle = document.getElementById('genderToggle');
  const tab    = document.querySelector(`.gender-tab[data-gender="${gender}"]`);
  const slider = document.getElementById('genderSlider');
  if (!toggle || !tab || !slider) return;
  const tr = toggle.getBoundingClientRect();
  const br = tab.getBoundingClientRect();
  slider.style.left  = (br.left - tr.left) + 'px';
  slider.style.width = br.width + 'px';
}

window.addEventListener('load', () => {
  fetchPhotosData(); // Start fetch immediately
  if (typeof window.currentGender !== 'undefined') {
    if (document.getElementById('catGrid')) {
      document.querySelectorAll('.gender-tab').forEach(t => t.classList.remove('active'));
      const target = document.querySelector(`.gender-tab[data-gender="${window.currentGender}"]`);
      if (target) target.classList.add('active');
      if (typeof window.buildGrid === 'function') window.buildGrid(window.currentGender);
    }
    appMoveGenderSlider(window.currentGender);
  } else {
    appMoveGenderSlider('female');
  }
});

window.addEventListener('resize', () => {
  const active = document.querySelector('.gender-tab.active');
  if (active) appMoveGenderSlider(active.dataset.gender);
});

window.switchGender = window.appSwitchGender;
window.moveSlider = window.appMoveGenderSlider;

function initScratch(wrap) {
  const canvas = wrap.querySelector('.scratch-canvas');
  const reveal = wrap.querySelector('.scratch-reveal');
  const doneMsg = wrap.closest('.scratch-zone').querySelector('.scratch-done-msg');
  if(!canvas || !reveal) return;
  const revealH = reveal.offsetHeight || 80;
  canvas.width  = wrap.offsetWidth;
  canvas.height = revealH + (reveal.offsetTop || 0) + 28;

  const ctx = canvas.getContext('2d');
  const grad = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
  grad.addColorStop(0,   '#C8C0B8');
  grad.addColorStop(0.3, '#E2DAD2');
  grad.addColorStop(0.6, '#B8B0A8');
  grad.addColorStop(1,   '#D0C8C0');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = 'rgba(255,255,255,0.15)';
  ctx.lineWidth = 1;
  for (let i = -canvas.height; i < canvas.width + canvas.height; i += 8) {
    ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i + canvas.height, canvas.height); ctx.stroke();
  }

  ctx.fillStyle = 'rgba(80,70,60,0.55)';
  ctx.font = '500 13px DM Sans, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('Сотрите монеткой или пальцем', canvas.width / 2, canvas.height / 2 - 8);
  ctx.fillStyle = 'rgba(80,70,60,0.3)';
  ctx.beginPath();
  ctx.arc(canvas.width / 2, canvas.height / 2 + 20, 13, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = 'rgba(255,255,255,0.5)';
  ctx.font = 'bold 11px DM Sans, sans-serif';
  ctx.fillText('₽', canvas.width / 2, canvas.height / 2 + 25);

  ctx.globalCompositeOperation = 'destination-out';

  let painting = false;
  let revealed = false;

  function getPos(e) {
    const r = canvas.getBoundingClientRect();
    const src = e.touches ? e.touches[0] : e;
    return { x: src.clientX - r.left, y: src.clientY - r.top };
  }

  function scratch(x, y) {
    ctx.beginPath();
    ctx.arc(x, y, 28, 0, Math.PI * 2);
    ctx.fill();
  }

  function fullClear() {
    revealed = true;
    let alpha = 1;
    const fade = setInterval(() => {
      alpha -= 0.07;
      if (alpha <= 0) {
        clearInterval(fade);
        canvas.style.display = 'none';
        if (doneMsg) doneMsg.classList.add('visible');
        return;
      }
      ctx.globalCompositeOperation = 'destination-out';
      ctx.globalAlpha = 0.15;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }, 16);
  }

  function checkReveal() {
    if (revealed) return;
    const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
    let cleared = 0, total = 0;
    for (let i = 3; i < data.length; i += 32) { if (data[i] === 0) cleared++; total++; }
    if (cleared / total > (window.matchMedia('(hover: hover)').matches ? 0.20 : 0.40)) fullClear();
  }

  canvas.addEventListener('mousedown', (e) => { painting = true; const p = getPos(e); scratch(p.x, p.y); });
  canvas.addEventListener('mousemove', (e) => { if (!painting) return; const p = getPos(e); scratch(p.x, p.y); checkReveal(); });
  canvas.addEventListener('mouseup',   () => { painting = false; checkReveal(); });
  canvas.addEventListener('mouseleave',() => { painting = false; });
  canvas.addEventListener('touchstart', (e) => { e.preventDefault(); painting = true; const p = getPos(e); scratch(p.x, p.y); }, { passive: false });
  canvas.addEventListener('touchmove',  (e) => { e.preventDefault(); if (!painting) return; const p = getPos(e); scratch(p.x, p.y); checkReveal(); }, { passive: false });
  canvas.addEventListener('touchend',   () => { painting = false; checkReveal(); });
}

window.copyCode = function(btn, code) {
  navigator.clipboard.writeText(code).then(() => {
    btn.textContent = '✓ Скопировано!';
    btn.classList.add('copied');
    setTimeout(() => { btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 13 13" fill="none"><rect x="4" y="4" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="1.3"/><path d="M1 9V2a1 1 0 011-1h7" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg> Скопировать`; btn.classList.remove('copied'); }, 2000);
  });
}

window.addEventListener('load', () => {
  document.querySelectorAll('.scratch-canvas-wrap').forEach(w => initScratch(w));
});

window.addEventListener('load', () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.opacity = '1';
        e.target.style.transform = 'translateY(0)';
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.08 });

  document.querySelectorAll('.case-card, .step, .photo-card, .contact-card, .about-card').forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(22px)';
    el.style.transition = `opacity 0.6s cubic-bezier(0.22,1,0.36,1) ${i * 0.05}s, transform 0.6s cubic-bezier(0.22,1,0.36,1) ${i * 0.05}s`;
    observer.observe(el);
  });
});

window.lbOpen = function(idx,e) { 
  if(e)e.stopPropagation(); 
  if(typeof window.imgs === 'undefined') return;
  if(idx>=window.imgs.length)return; 
  window.cur=idx; 
  window.renderLb(); 
  document.getElementById('lightbox').classList.add('open'); 
  document.body.style.overflow='hidden'; 
}
window.lbClose = function() { 
  document.getElementById('lightbox').classList.remove('open'); 
  document.body.style.overflow=''; 
}
window.lbBgClose = function(e) { 
  if(e.target===document.getElementById('lightbox')) window.lbClose(); 
}
window.lbNav = function(dir) {
  const inner=document.querySelector('.lb-inner');
  if(!inner) return;
  const out=dir===1?'-60px':'60px', inn=dir===1?'60px':'-60px';
  inner.style.transition='opacity 0.16s,transform 0.16s'; 
  inner.style.opacity='0'; 
  inner.style.transform=`scale(0.95) translateX(${out})`;
  setTimeout(() => {
    window.cur=(window.cur+dir+window.imgs.length)%window.imgs.length; 
    window.renderLb();
    inner.style.transition='none'; 
    inner.style.transform=`scale(0.95) translateX(${inn})`; 
    inner.style.opacity='0';
    requestAnimationFrame(() => requestAnimationFrame(() => {
      inner.style.transition='opacity 0.2s,transform 0.22s cubic-bezier(0.22,1,0.36,1)';
      inner.style.opacity='1'; inner.style.transform='scale(1) translateX(0)';
    }));
  }, 160);
}
window.renderLb = function() {
  const imgs = window.imgs;
  const cur = window.cur;
  if(!imgs) return;
  const lbImg = document.getElementById('lbImg');
  if(lbImg) lbImg.innerHTML = imgs[cur]?`<img src="${imgs[cur]}" alt="">`:'<div style="width:100%;height:300px;background:#1e1c1a"></div>';
  const dots=document.getElementById('lbDots'); 
  if(dots) {
    dots.innerHTML='';
    imgs.forEach((_,i) => { 
      const d=document.createElement('button'); 
      d.className='lb-dot'+(i===cur?' active':'');
      d.setAttribute('type', 'button');
      d.setAttribute('aria-label', `Slide ${i+1}`);
      d.onclick=ev=>{ev.stopPropagation();window.cur=i;window.renderLb();}; 
      dots.appendChild(d); 
    });
  }
}

document.addEventListener('keydown', e => {
  const lb = document.getElementById('lightbox');
  if(!lb || !lb.classList.contains('open')) return;
  if(e.key==='Escape') window.lbClose(); 
  if(e.key==='ArrowLeft') window.lbNav(-1); 
  if(e.key==='ArrowRight') window.lbNav(1);
});

window.addEventListener('load', () => {
  const lb = document.getElementById('lightbox'); 
  if(!lb) return;
  let sx=0,sy=0,drag=false;
  const inn=()=>document.querySelector('.lb-inner');
  lb.addEventListener('touchstart',e=>{
    if(!lb.classList.contains('open'))return;
    sx=e.touches[0].clientX;sy=e.touches[0].clientY;drag=true;
    if(inn()) inn().style.transition='none';
  },{passive:true});
  
  lb.addEventListener('touchmove',e=>{
    if(!drag||!lb.classList.contains('open'))return;
    const dx=e.touches[0].clientX-sx,dy=e.touches[0].clientY-sy;
    if(Math.abs(dx)>Math.abs(dy)){
      const c=Math.max(-120,Math.min(120,dx));
      if(inn()){
        inn().style.transform=`translateX(${c}px) scale(${1-Math.abs(c)/120*0.04})`;
        inn().style.opacity=`${1-Math.abs(c)/120*0.3}`;
      }
    }
  },{passive:true});
  
  lb.addEventListener('touchend',e=>{
    if(!drag||!lb.classList.contains('open'))return;
    drag=false;
    const dx=e.changedTouches[0].clientX-sx,dy=e.changedTouches[0].clientY-sy;
    if(Math.abs(dx)>Math.abs(dy)&&Math.abs(dx)>50){
      window.lbNav(dx<0?1:-1);
    }else{
      if(inn()){
        inn().style.transition='opacity 0.2s,transform 0.2s';
        inn().style.transform='translateX(0) scale(1)';
        inn().style.opacity='1';
      }
    }
  },{passive:true});
});

window.buildGrid = function(gender) {
  let data;
  if (window.DYNAMIC_DATA && window.DYNAMIC_DATA[gender] && window.DYNAMIC_DATA[gender][window.currentCategory]) {
    data = window.DYNAMIC_DATA[gender][window.currentCategory];
    window.TITLE = data.title; // Update TITLE globally from Sheet
  } else if (typeof window.DATA !== 'undefined' && window.DATA[gender]) {
    data = window.DATA[gender];
  }

  if (!data) return;
  const grid = document.getElementById('catGrid');
  if(!grid) return;
  const PHOTO_COUNT = data.photos.length > 0 ? data.photos.length : 3;
  let html = '';
  for (let i = 0; i < Math.max(3, PHOTO_COUNT); i++) {
    if (i < data.photos.length) {
      html += `<button type="button" class="photo-item" onclick="lbOpen(${i},event)">
        <img src="${data.photos[i]}" alt="Фотография стиля">
        <div class="overlay"></div>
        <div class="zoom"><svg width="14" height="14" viewBox="0 0 14 14" fill="none"><circle cx="6" cy="6" r="3.5" stroke="currentColor" stroke-width="1.4"/><path d="M9.5 9.5l3 3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg></div>
      </button>`;
    } else {
      html += `<div class="photo-item">
        <div class="photo-placeholder">
          <svg width="40" height="40" viewBox="0 0 40 40" fill="none"><rect x="4" y="8" width="32" height="24" rx="4" stroke="currentColor" stroke-width="1.5"/><circle cx="20" cy="20" r="5" stroke="currentColor" stroke-width="1.5"/></svg>
          <p>Фото скоро</p>
        </div>
      </div>`;
    }
  }
  grid.innerHTML = html;
  window.imgs = Array.from(grid.querySelectorAll('img[src]')).map(i => i.src).filter(src => !src.includes('data:'));
  document.getElementById('catDesc').textContent = data.desc;
  document.getElementById('photoCount').textContent = window.imgs.length + ' фотографий';
  document.getElementById('breadcrumb').innerHTML =
    `<a href="index.html">Главная</a> / Категории / ${(gender==='male'?'Мужские':'Женские')} / ${window.TITLE}`;
  
  const obs = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.style.opacity='1'; e.target.style.transform='translateY(0)'; obs.unobserve(e.target); }
  }), {threshold:0.05});
  grid.querySelectorAll('.photo-item').forEach((el,i) => {
    el.style.opacity='0'; el.style.transform='translateY(18px)';
    el.style.transition=`opacity 0.5s cubic-bezier(0.22,1,0.36,1) ${i*0.07}s,transform 0.5s cubic-bezier(0.22,1,0.36,1) ${i*0.07}s`;
    obs.observe(el);
  });
}
