import os
import re

files_to_fix = [
    r"D:\Proyectos personales\personal branding\living_book_astro\src\content\ebook\03-what-a-production-line-teaches-about-architecture.mdx",
    r"D:\Proyectos personales\personal branding\living_book_astro\src\pages\es\ebook\03-what-a-production-line-teaches-about-architecture\index.astro"
]

replacements = [
    (r'style="fill:#0057D9;stroke:#0057D9;stroke-width:1.5"', 'fill="#0057D9" stroke="#0057D9" stroke-width="1.5"'),
    (r'style="fill:#FFFFFF;stroke:#C9D0D8;stroke-width:1.5"', 'fill="#FFFFFF" stroke="#C9D0D8" stroke-width="1.5"'),
    (r'style="font-family:Archivo,sans-serif;font-weight:700;fill:#ffffff"', 'font-family="Archivo,sans-serif" font-weight="700" fill="#ffffff"'),
    (r'style="font-family:Archivo,sans-serif;font-weight:700;fill:#111418"', 'font-family="Archivo,sans-serif" font-weight="700" fill="#111418"'),
    (r'style="font-family:Archivo,sans-serif;font-weight:500;fill:rgba(255,255,255,.85)"', 'font-family="Archivo,sans-serif" font-weight="500" fill="rgba(255,255,255,.85)"'),
    (r'style="font-family:Archivo,sans-serif;font-weight:500;fill:#5C6673"', 'font-family="Archivo,sans-serif" font-weight="500" fill="#5C6673"'),
    (r'style="stroke:#2E7CFF;stroke-width:1.5;fill:none"', 'stroke="#2E7CFF" stroke-width="1.5" fill="none"'),
    (r'style="stroke:#C9D0D8;stroke-width:1.5;fill:none"', 'stroke="#C9D0D8" stroke-width="1.5" fill="none"'),
]

for file_path in files_to_fix:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Replaced all style attributes with SVG presentation attributes.")
