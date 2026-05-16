import os
import re

# We will look for <a> tags containing 'threads.com' and replace their SVG with <span class="threads-icon"></span>
# We'll use a regex that captures the <a> tag and its content, then replaces the SVG inside.

def update_file(filepath):
    if not filepath.endswith('.html'):
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for Threads link with an SVG inside
    # This captures the link and we'll process the content inside
    pattern = r'(<a\s+[^>]*href="[^"]*threads\.com[^"]*"[^>]*>)(.*?)(</a>)'
    
    def replace_svg(match):
        prefix = match.group(1)
        inner = match.group(2)
        suffix = match.group(3)
        
        # Replace the SVG block with the span
        # SVG might have different sizes, but the CSS utility handles it
        new_inner = re.sub(r'<svg.*?</svg>', '<span class="threads-icon"></span>', inner, flags=re.DOTALL)
        
        # Special case for the contact card which has a label
        if 'Threads' in inner and 'contact-label' not in inner:
             # If it's a simple link like in footer, we might want to keep the text if any
             pass
        
        # In the footer, we have <a ...>Threads</a>
        # If it's just text, we might want to ADD the icon if it's missing, or just keep it as is.
        # But the user said "load it", so they probably want the icon.
        if 'Threads' in inner and '<span class="threads-icon">' not in new_inner and '<svg' not in inner:
             new_inner = '<span class="threads-icon"></span>' + inner

        return prefix + new_inner + suffix

    new_content = re.sub(pattern, replace_svg, content, flags=re.DOTALL)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

for f in os.listdir('.'):
    if f.endswith('.html'):
        if update_file(f):
            print(f"Updated {f}")
