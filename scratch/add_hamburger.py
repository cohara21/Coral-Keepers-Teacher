import os
import glob
import re

files = glob.glob('Teacher/*.html') + glob.glob('Student/*.html')

# CSS to inject
css_to_add = """
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
        display: none;
        position: fixed;
        top: 64px;
        right: 0;
        width: 260px;
        background: #ffffff;
        flex-direction: column;
        padding: 16px 24px;
        box-shadow: -10px 0 20px rgba(0,0,0,0.05);
        border-left: 1px solid rgba(0,0,0,0.08);
        height: auto;
        gap: 0;
        z-index: 100;
      }
      .nav-links.open {
        display: flex;
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
      }
    }
"""

# HTML button to inject after the brand link
button_html = """
      <button class="menu-toggle" aria-label="Toggle menu" onclick="document.querySelector('.nav-links').classList.toggle('open')">
        <span></span>
        <span></span>
        <span></span>
      </button>"""

for file_path in files:
    with open(file_path, 'r') as f:
        content = f.read()
    
    # 1. Add CSS before </style>
    if '</style>' in content and '.menu-toggle' not in content:
        content = content.replace('</style>', css_to_add + '\n  </style>')
    
    # 2. Add button into top-nav-inner after the brand link / img
    # Look for the brand img wrapper and insert after it
    if '<button class="menu-toggle"' not in content:
        # Match the end of the </a> tag that wraps the brand img
        brand_pattern = re.compile(r'(<a[^>]*brand[^>]*>.*?</a>)', re.DOTALL)
        if brand_pattern.search(content):
            content = brand_pattern.sub(r'\1' + button_html, content)
        else:
            # Fallback: find the brand img and insert after its parent link if possible
            content = content.replace('<img class="brand"', button_html + '\n      <img class="brand"')

    with open(file_path, 'w') as f:
        f.write(content)
    print(f"Updated {file_path}")
