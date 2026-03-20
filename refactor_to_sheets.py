import os
import re

# List of all category files
html_files = [f for f in os.listdir('.') if f.startswith('category-') and f.endswith('.html')]

# Regex for the script block containing DATA and TITLE
# We want to replace it with a smaller block defining category and gender
script_pattern = re.compile(r'<script>\s*const DATA = \{.*?\};\s*const TITLE = ".*?";\s*window\.TITLE = TITLE;\s*window\.DATA = DATA;\s*window\.currentGender = "(.*?)";\s*</script>', re.DOTALL)

def refactor_file(filename):
    # Determine category key from filename
    category_key = filename.replace('category-', '').replace('-male', '').replace('.html', '')
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract gender from existing script or filename
    gender = 'male' if '-male.html' in filename else 'female'
    
    # New script block
    new_script = f"""<script>
    window.currentGender = "{gender}";
    window.currentCategory = "{category_key}";
  </script>"""
    
    # Replace the old block
    # We use a more flexible regex if the one above is too strict
    flexible_pattern = re.compile(r'<script>\s*const DATA = \{.*?\};.*?window\.currentGender = ".*?";\s*</script>', re.DOTALL)
    
    new_content = flexible_pattern.sub(new_script, content)
    
    if new_content != content:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

count = 0
for f in html_files:
    if refactor_file(f):
        count += 1
        print(f"Refactored {f}")

print(f"Total files refactored: {count}")
