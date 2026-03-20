import os
import re
import csv

# Setup
html_files = [f for f in os.listdir('.') if f.startswith('category-') and f.endswith('.html')]
output_csv = 'photos_data.csv'

data_rows = []
seen_urls = set()

# Improved Regex patterns
male_block_re = re.compile(r'male:\s*\{(.*?)\}', re.DOTALL)
female_block_re = re.compile(r'female:\s*\{(.*?)\}', re.DOTALL)
desc_re = re.compile(r'desc:\s*"(.*?)"', re.DOTALL)
photos_re = re.compile(r'photos:\s*\[(.*?)\]', re.DOTALL)
title_pattern = re.compile(r'const TITLE = "(.*?)";', re.DOTALL)

def clean_url(url):
    return url.strip().strip('"').strip("'").strip()

for filename in html_files:
    category_key = filename.replace('category-', '').replace('-male', '').replace('.html', '')
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # TITLE
        title_match = title_pattern.search(content)
        title = title_match.group(1).encode('utf-8').decode('unicode_escape') if title_match else ""
        
        # Parse blocks
        for gender, block_re in [('male', male_block_re), ('female', female_block_re)]:
            block_match = block_re.search(content)
            if block_match:
                block_content = block_match.group(1)
                
                # DESC
                desc_match = desc_re.search(block_content)
                desc = desc_match.group(1).encode('utf-8').decode('unicode_escape') if desc_match else ""
                
                # PHOTOS
                photos_match = photos_re.search(block_content)
                if photos_match:
                    raw_photos = photos_match.group(1)
                    urls = [clean_url(u) for u in raw_photos.split(',') if u.strip()]
                    for url in urls:
                        # De-duplicate by (gender, category, url)
                        uid = f"{gender}-{category_key}-{url}"
                        if uid not in seen_urls:
                            data_rows.append([gender, category_key, title, desc, url])
                            seen_urls.add(uid)

# Write to CSV
with open(output_csv, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Gender', 'Category', 'Title', 'Description', 'PhotoURL'])
    writer.writerows(data_rows)

print(f"Successfully extracted {len(data_rows)} unique photo entries to {output_csv}")
