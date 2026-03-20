import os
import re

BASE_DIR = r"e:/фото для ии/photosetai_antigravity"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
CSS_DIR = os.path.join(ASSETS_DIR, "css")
JS_DIR = os.path.join(ASSETS_DIR, "js")

os.makedirs(CSS_DIR, exist_ok=True)
os.makedirs(JS_DIR, exist_ok=True)

# 1. READ INDEX.HTML FOR CSS
with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
    index_html = f.read()

css_match = re.search(r"<style>(.*?)</style>", index_html, flags=re.DOTALL)
index_css = css_match.group(1).strip() if css_match else ""

CATEGORY_SPECIFIC_CSS = """
/* ── CATEGORY PAGE SPECIFIC CSS ── */
.nav-back { display:inline-flex; align-items:center; gap:8px; font-size:0.82rem; letter-spacing:0.06em; color:var(--muted); text-decoration:none; transition:color 0.2s; }
.nav-back:hover { color:var(--accent); }
.nav-back:hover svg { transform:translateX(-3px); }
.nav-back svg { transition:transform 0.2s; }
.cat-header { padding:130px 40px 48px; max-width:1120px; margin:0 auto; position:relative; z-index:1; }
.cat-breadcrumb { font-size:0.72rem; letter-spacing:0.14em; text-transform:uppercase; color:var(--muted); margin-bottom:16px; }
.cat-breadcrumb a { color:var(--muted); text-decoration:none; }
.cat-breadcrumb a:hover { color:var(--accent); }
.cat-header-row { display:flex; align-items:flex-end; justify-content:space-between; flex-wrap:wrap; gap:20px; margin-bottom:16px; }
.cat-title { font-family:'Cormorant Garamond',serif; font-size:clamp(2.4rem,5vw,4.2rem); font-weight:300; line-height:1.1; letter-spacing:-0.01em; }
.cat-title em { font-style:italic; color:var(--accent); }
.cat-desc { font-size:0.95rem; color:var(--muted); line-height:1.7; max-width:480px; }
.cat-count { display:inline-flex; align-items:center; gap:8px; margin-top:16px; font-size:0.75rem; letter-spacing:0.1em; text-transform:uppercase; color:var(--muted); }
.cat-count::before { content:''; display:block; width:24px; height:1px; background:var(--muted); }
.cat-grid { columns:3; column-gap:14px; padding:0 40px 100px; max-width:1120px; margin:0 auto; position:relative; z-index:1; }
.photo-item { break-inside:avoid; border-radius:16px; overflow:hidden; position:relative; cursor:pointer; margin-bottom:14px; background:var(--glass-bg); border:1px solid var(--glass-border); box-shadow:var(--glass-shadow); transition:transform 0.36s cubic-bezier(0.22,1,0.36,1),box-shadow 0.36s; display:block; width:100%; text-align:left; padding:0; }
.photo-item:hover { transform:translateY(-6px); box-shadow:0 24px 64px rgba(0,0,0,0.15); }
.photo-item img { width:100%; height:auto; display:block; transition:transform 0.5s cubic-bezier(0.22,1,0.36,1); }
.photo-item:hover img { transform:scale(1.03); }
.photo-item .overlay { position:absolute; inset:0; background:linear-gradient(to top,rgba(0,0,0,0.3) 0%,transparent 55%); opacity:0; transition:opacity 0.3s; z-index:1; }
.photo-item:hover .overlay { opacity:1; }
.photo-item .zoom { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%) scale(0.7); width:46px; height:46px; border-radius:50%; background:rgba(255,255,255,0.9); display:flex; align-items:center; justify-content:center; opacity:0; z-index:2; transition:opacity 0.25s,transform 0.25s cubic-bezier(0.22,1,0.36,1); }
.photo-item:hover .zoom { opacity:1; transform:translate(-50%,-50%) scale(1); }
.photo-placeholder { width:100%; aspect-ratio:2/3; background:linear-gradient(145deg,#f0ede8,#e2ddd6); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:12px; color:var(--muted); }
.photo-placeholder svg { opacity:0.2; }
.photo-placeholder p { font-size:0.7rem; letter-spacing:0.1em; text-transform:uppercase; opacity:0.4; }
.lightbox { position:fixed; inset:0; z-index:1000; background:rgba(12,11,10,0.92); backdrop-filter:blur(24px); display:flex; align-items:center; justify-content:center; opacity:0; pointer-events:none; transition:opacity 0.3s cubic-bezier(0.22,1,0.36,1); }
.lightbox.open { opacity:1; pointer-events:all; }
.lb-inner { position:relative; max-width:min(520px,90vw); width:100%; transform:scale(0.9) translateY(20px); transition:transform 0.35s cubic-bezier(0.22,1,0.36,1); }
.lightbox.open .lb-inner { transform:scale(1) translateY(0); }
.lb-img { border-radius:20px; overflow:hidden; box-shadow:0 40px 100px rgba(0,0,0,0.5); max-height:85vh; display:flex; align-items:center; justify-content:center; }
.lb-img img { width:100%; height:auto; max-height:85vh; object-fit:contain; display:block; }
.lb-close { position:absolute; top:-16px; right:-16px; width:40px; height:40px; border-radius:50%; background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.2); display:flex; align-items:center; justify-content:center; cursor:pointer; color:#fff; z-index:10; transition:background 0.2s; padding:0; }
.lb-close:hover { background:rgba(255,255,255,0.22); }
.lb-nav { position:absolute; top:50%; transform:translateY(-50%); width:44px; height:44px; border-radius:50%; background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.18); display:flex; align-items:center; justify-content:center; cursor:pointer; color:#fff; transition:background 0.2s; padding:0; }
.lb-nav:hover { background:rgba(255,255,255,0.2); }
.lb-prev { left:-60px; } .lb-next { right:-60px; }
.lb-dots { display:flex; gap:8px; justify-content:center; margin-top:16px; }
.lb-dot { width:6px; height:6px; border-radius:50%; background:rgba(255,255,255,0.25); cursor:pointer; transition:background 0.2s,transform 0.2s; border:none; padding:0; }
.lb-dot.active { background:#fff; transform:scale(1.3); }
"""

CSS_RESETS = """
/* ── RESETS FOR SEMANTIC TAGS ── */
button { border: none; background: transparent; font-family: inherit; padding: 0; outline: none; cursor: pointer; }
.photo-item { text-align: left; }
.gender-tab { appearance: none; -webkit-appearance: none; outline: none; }
.nav-mobile-btn { appearance: none; -webkit-appearance: none; outline: none; padding: 4px; cursor: pointer; }
"""

CATEGORY_MEDIA_QUERIES = """
@media(max-width:900px){
  .cat-header{padding:110px 20px 40px;}
  .cat-grid{columns:2;column-gap:10px;padding:0 20px 80px;}
  .lb-prev{left:-44px;}.lb-next{right:-44px;}
}
@media(max-width:600px){
  .cat-header{padding:90px 16px 32px;}
  .cat-grid{columns:2;column-gap:8px;padding:0 16px 60px;}
  .cat-header-row{flex-direction:column;align-items:flex-start;gap:16px;}
  .lb-prev,.lb-next{display:none;}
  .lb-inner{max-width:94vw;}
  .gender-tab{padding:8px 16px;font-size:0.75rem;}
}
@media(max-width:420px){
  .cat-grid{columns:1;}
}
@media(prefers-color-scheme:dark){
  .photo-placeholder{background:linear-gradient(145deg,#1e1c1a,#171614);}
}
"""

final_css = index_css + "\n" + CSS_RESETS + "\n" + CATEGORY_SPECIFIC_CSS + "\n" + CATEGORY_MEDIA_QUERIES

with open(os.path.join(CSS_DIR, "style.css"), "w", encoding="utf-8") as f:
    f.write(final_css)

MAIN_JS_CONTENT = """
/* ── MAIN JS ── */

function toggleMenu() {
  const m = document.getElementById('mobileMenu');
  if (!m) return;
  const open = m.style.display === 'flex';
  m.style.display = open ? 'none' : 'flex';
}

window.appSwitchGender = function(gender) {
  if (typeof window.currentGender !== 'undefined' && document.getElementById('catGrid')) {
    if (gender === window.currentGender) return;
    window.currentGender = gender;
    document.querySelectorAll('.gender-tab').forEach(t => {
      if(t.dataset.gender === gender) t.classList.add('active');
      else t.classList.remove('active');
    });
    appMoveGenderSlider(gender);
    const grid = document.getElementById('catGrid');
    if(!grid) return;
    grid.style.transition='opacity 0.2s'; grid.style.opacity='0';
    setTimeout(() => { if(typeof window.buildGrid === 'function') window.buildGrid(gender); grid.style.opacity='1'; }, 200);
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
  if (typeof window.currentGender !== 'undefined') {
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
  if (typeof window.DATA === 'undefined') return;
  const data = window.DATA[gender];
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
"""

with open(os.path.join(JS_DIR, "main.js"), "w", encoding="utf-8") as f:
    f.write(MAIN_JS_CONTENT)

def process_html_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # REMOVE CSS <style> completely
    content = re.sub(r"<style>[\s\S]*?</style>", r'<link rel="stylesheet" href="assets/css/style.css">', content)

    # Convert ALL <div class="gender-tab..."> to <button type="button" class="gender-tab...">
    content = re.sub(
        r'<div\s+class="gender-tab([^"]*)"([^>]*)>(.*?)</div>',
        r'<button type="button" class="gender-tab\1"\2>\3</button>',
        content
    )

    # Add <main> wrappers
    if "index.html" in filepath:
        if "<main>" not in content:
            content = content.replace('<!-- HERO -->', '<main>\n<!-- HERO -->')
            content = content.replace('<!-- FOOTER -->', '</main>\n<!-- FOOTER -->')
        
        # Replace nav-mobile-btn div
        content = re.sub(
            r'<div class="nav-mobile-btn"([^>]*)>(.*?)</div>',
            r'<button type="button" class="nav-mobile-btn"\1>\2</button>',
            content,
            flags=re.DOTALL
        )

        # Replace JS block with script tag
        content = re.sub(r"<script>[\s\S]*?</script>", r'<script src="assets/js/main.js"></script>', content)

    else:
        # Category Pages
        if "<header class=\"cat-header\">" in content and "<main>" not in content:
            content = content.replace('<header class="cat-header">', '<main>\n<header class="cat-header">')
            content = content.replace('<footer>', '</main>\n<footer>')

        # Since category grid starts empty and is built dynamically by `buildGrid`, we don't need to replace <div...photo-item> inside HTML here; it's handled in main.js.

        # Refactor JS
        script_match = re.search(r"<script>([\s\S]*?)</script>", content)
        if script_match and "assets/js/main.js" not in content:
            script_code = script_match.group(1)
            
            data_match = re.search(r"const DATA = \{[\s\S]*?\};\s*", script_code)
            title_match = re.search(r"const TITLE = .*?;\s*", script_code)
            gender_match = re.search(r"let currentGender = .*?;\s*", script_code)

            data_str = data_match.group(0) if data_match else "const DATA = {};\n"
            title_str = title_match.group(0) if title_match else "const TITLE = '';\n"
            
            # Extract default gender
            if gender_match:
                gender_val = gender_match.group(0).split('=')[1].replace(';','').strip()
            else:
                gender_val = "'female'"

            new_script = f"""<script>
{data_str}{title_str}
window.TITLE = TITLE;
window.DATA = DATA;
window.currentGender = {gender_val};
</script>
<script src="assets/js/main.js"></script>"""
            
            content = content[:script_match.start()] + new_script + content[script_match.end():]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

for fn in os.listdir(BASE_DIR):
    if fn.endswith(".html"):
        process_html_file(os.path.join(BASE_DIR, fn))

print("DONE refactoring.")
