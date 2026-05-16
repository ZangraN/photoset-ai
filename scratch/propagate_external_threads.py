import os
import re

NAV_HTML = """  <nav>
    <div class="nav-logo">Photoset<span>AI</span></div>
    <div class="nav-links">
      <a href="index.html#portfolio">Работы</a>
      <a href="index.html#usecases">Применение</a>
      <a href="index.html#pricing">Цены</a>
      <a href="index.html#promos">Акции</a>
      <a href="index.html#certificates">Сертификаты</a>
      <a href="verify.html">Проверка</a>
      <a href="index.html#about">Обо мне</a>
      <a href="index.html#contact">Контакты</a>
    </div>
    <button type="button" class="nav-mobile-btn" id="menuBtn" onclick="toggleMenu()" aria-label="Меню">
      <span></span><span></span><span></span>
    </button>
  </nav>

  <!-- Mobile Drawer -->
  <div class="drawer-overlay" id="drawerOverlay" onclick="toggleMenu()"></div>
  <div class="burger-drawer" id="burgerDrawer">
    <div class="drawer-links">
      <a href="index.html#portfolio" onclick="toggleMenu()">Работы</a>
      <a href="index.html#usecases" onclick="toggleMenu()">Применение</a>
      <a href="index.html#pricing" onclick="toggleMenu()">Цены</a>
      <a href="index.html#promos" onclick="toggleMenu()">Акции</a>
      <a href="index.html#certificates" onclick="toggleMenu()">Сертификаты</a>
      <a href="verify.html" onclick="toggleMenu()">Проверка</a>
      <a href="index.html#about" onclick="toggleMenu()">Обо мне</a>
      <a href="index.html#contact" onclick="toggleMenu()">Контакты</a>
    </div>
    <div class="drawer-footer">
      <div class="section-tag">Мы в соцсетях</div>
      <div class="drawer-socials">
        <a href="https://www.instagram.com/photo.set_ai/" target="_blank" class="social-icon" aria-label="Instagram">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
        </a>
        <a href="https://www.threads.com/@photo.set_ai?igshid=NTc4MTIwNjQ2YQ==" target="_blank" class="social-icon" aria-label="Threads">
          <span class="threads-icon"></span>
        </a>
        <a href="https://t.me/Mescallito" target="_blank" class="social-icon" aria-label="Telegram">
          <svg width="20" height="18" viewBox="0 0 26 22" fill="none"><path d="M1.5 10.5L24 1.5L17 20.5L11 13.5L1.5 10.5Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" /><path d="M11 13.5L15.5 9.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" /></svg>
        </a>
      </div>
    </div>
  </div>"""

FOOTER_HTML = """  <!-- FOOTER -->
  <footer>
    <div class="footer-content">
      <div class="footer-socials">
        <a href="https://www.instagram.com/photo.set_ai/" target="_blank" aria-label="Instagram">Instagram</a>
        <a href="https://www.threads.com/@photo.set_ai?igshid=NTc4MTIwNjQ2YQ==" target="_blank" aria-label="Threads">
          <span class="threads-icon"></span>Threads
        </a>
        <a href="https://t.me/Mescallito" target="_blank" aria-label="Telegram">Telegram</a>
      </div>
      <div>© 2026 PhotosetAI · Павел &nbsp;·&nbsp; Все права защищены</div>
    </div>
  </footer>"""

def update_file(filepath):
    if not filepath.endswith('.html'):
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace Nav
    # We look for <nav>...</nav> or similar
    new_content = re.sub(r'<nav>.*?</nav>(.*?<!-- Mobile Drawer -->.*?</div>.*?</div>)?', NAV_HTML, content, flags=re.DOTALL)
    
    # If index.html, we also have the mobile dropdown to remove
    if filepath == 'index.html':
        new_content = re.sub(r'<!-- Mobile dropdown -->.*?</div>', '', new_content, flags=re.DOTALL)
        
        # Also update Threads contact card in index.html
        threads_card_pattern = r'(<a\s+[^>]*threads\.com[^>]*class="contact-card"[^>]*>)(.*?)(</a>)'
        def replace_threads_card(match):
            prefix = match.group(1)
            inner = match.group(2)
            suffix = match.group(3)
            # Replace inline SVG with span
            new_inner = re.sub(r'<svg.*?</svg>', '<span class="threads-icon"></span>', inner, flags=re.DOTALL)
            return prefix + new_inner + suffix
        new_content = re.sub(threads_card_pattern, replace_threads_card, new_content, flags=re.DOTALL)

    # Replace Footer
    new_content = re.sub(r'<footer>.*?</footer>', FOOTER_HTML, new_content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

for f in os.listdir('.'):
    if f.endswith('.html'):
        print(f"Updating {f}...")
        update_file(f)
