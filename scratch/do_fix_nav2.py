import os
import glob
import re

files = glob.glob('Teacher/*.html') + glob.glob('Student/*.html')

for file_path in files:
    with open(file_path, 'r') as f:
        content = f.read()
    
    new_content = content.replace('@media (max-width: 768px)', '@media (max-width: 600px)')
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    print(f"Updated {file_path}")
