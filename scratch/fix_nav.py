import os
import re

files = [
    "Teacher/announcements.html",
    "Teacher/learn.html",
    "Teacher/calendar.html",
    "Teacher/course-details.html",
    "Teacher/post-reading.html", # Added as it was in the IA list
    "Student/is-coral-animal.html",
    "Student/announcements.html",
    "Student/messages.html",
    "Student/learn.html",
    "Student/calendar.html",
    "Student/profile.html"
]

nav_hide_pattern = re.compile(r'(\s+\.nav-links \{\s+display: none;\s+\})')
style_close_pattern = re.compile(r'(\s+<\/style>)')

new_media_query = """
    @media (max-width: 600px) {
      .nav-links {
        display: none;
      }
    }
"""

for file_path in files:
    if os.path.exists(file_path):
        print(f"Processing {file_path}...")
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Remove old nav-links hiding from the middle of the file
        new_content = nav_hide_pattern.sub('', content)
        
        # Add the new media query before the closing style tag
        if '</style>' in new_content:
            new_content = new_content.replace('</style>', new_media_query + '  </style>')
            
        with open(file_path, 'w') as f:
            f.write(new_content)
    else:
        print(f"File {file_path} not found.")
