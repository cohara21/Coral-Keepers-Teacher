import os
import glob
import re

files = glob.glob('Teacher/*.html') + glob.glob('Student/*.html')

nav_hide_pattern = re.compile(r'(\s+\.nav-links \{\s+display: none;\s+\})')
new_media_query = """
    @media (max-width: 768px) {
      .nav-links {
        display: none;
      }
    }
"""

for file_path in files:
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Remove old nav-links hiding
    new_content = nav_hide_pattern.sub('', content)
    
    # If the new media query isn't already there, add it right before </style>
    if '@media (max-width: 768px)' not in new_content and '</style>' in new_content:
        new_content = new_content.replace('</style>', new_media_query + '  </style>')
        
    with open(file_path, 'w') as f:
        f.write(new_content)
    print(f"Updated {file_path}")
