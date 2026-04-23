import os
import glob
import re

files = glob.glob('Teacher/*.html') + glob.glob('Student/*.html')

# New CSS block
new_css = """
    .menu-toggle {
      display: none;
      flex-direction: column;
      gap: 5px;
      background: none;
      border: none;
      cursor: pointer;
      padding: 8px;
      z-index: 40;
    }
    .menu-toggle span {
      display: block;
      width: 22px;
      height: 2px;
      background: var(--text-dark);
      border-radius: 2px;
      transition: 0.3s;
    }

    @media (max-width: 1000px) {
      .menu-toggle {
        display: flex;
      }
      .nav-links {
        display: flex;
        position: fixed;
        top: 64px;
        right: 0;
        width: 280px;
        height: calc(100vh - 64px);
        background: #ffffff;
        flex-direction: column;
        padding: 16px 24px;
        box-shadow: -10px 0 20px rgba(0,0,0,0.05);
        border-left: 1px solid rgba(0,0,0,0.08);
        gap: 0;
        z-index: 100;
        transform: translateX(100%);
        transition: transform 0.3s ease;
      }
      .nav-links.open {
        transform: translateX(0);
      }
      .nav-link {
        width: 100%;
        padding: 16px 0;
        border-bottom: 1px solid var(--divider);
        height: auto;
      }
      .nav-link.active {
        border-bottom-color: var(--blue);
      }
      .nav-link.switch {
        margin-left: 0;
        width: 100%;
        justify-content: flex-start;
        padding-right: 0;
        margin-top: auto;
        padding-bottom: 32px;
      }
      .menu-toggle.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
      .menu-toggle.open span:nth-child(2) { opacity: 0; }
      .menu-toggle.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
    }
"""

# New button HTML
new_button_html = """
      <button class="menu-toggle" aria-label="Toggle menu" onclick="this.classList.toggle('open'); document.querySelector('.nav-links').classList.toggle('open')">
        <span></span>
        <span></span>
        <span></span>
      </button>"""

# Pattern to find and remove old 600px nav-links hiding
old_600px_pattern = re.compile(r'\s*@media \(max-width: 600px\) \{\s*\.nav-links \{\s*display: none;\s*\}\s*\}', re.DOTALL)

for file_path in files:
    with open(file_path, 'r') as f:
        content = f.read()
    
    # 1. Remove old 600px and 1000px CSS blocks I added
    content = old_600px_pattern.sub('', content)
    # Remove previous .menu-toggle and @media (max-width: 1000px) block if it exists
    # We'll just replace everything from .menu-toggle up to the end of the 1000px media query
    content = re.sub(r'\s*\.menu-toggle \{.*?@media \(max-width: 1000px\) \{.*?\}\s*\}', '', content, flags=re.DOTALL)
    
    # 2. Add the refined CSS before </style>
    if '</style>' in content:
        content = content.replace('</style>', new_css + '\n  </style>')
    
    # 3. Update the button if it exists, or add it
    if '<button class="menu-toggle"' in content:
        content = re.sub(r'<button class="menu-toggle".*?</button>', new_button_html, content, flags=re.DOTALL)
    else:
        brand_pattern = re.compile(r'(<a[^>]*brand[^>]*>.*?</a>)', re.DOTALL)
        if brand_pattern.search(content):
            content = brand_pattern.sub(r'\1' + new_button_html, content)
        else:
            content = content.replace('<img class="brand"', new_button_html + '\n      <img class="brand"')

    with open(file_path, 'w') as f:
        f.write(content)
    print(f"Updated {file_path}")
