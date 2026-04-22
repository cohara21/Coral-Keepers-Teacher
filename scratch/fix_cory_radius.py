import os
import re

directories = ["Teacher", "Student"]
target_classes = [".floating-ai", ".cory-trigger", ".cory-avatar"]

# This regex matches the class followed by a block of CSS, 
# capturing the portion before and after the border-radius property.
# It handles both single-line and multi-line blocks.
def fix_border_radius(content):
    for cls in target_classes:
        # Find the block for this class
        # Look for the class name followed by optional space, then { and then 
        # any characters that aren't } until we find border-radius
        pattern = re.compile(r'(' + re.escape(cls) + r'\s*\{[^\}]*)(border-radius:\s*[^;]+;)', re.DOTALL)
        content = pattern.sub(r'\1border-radius: 50%;', content)
    return content

for directory in directories:
    if not os.path.exists(directory):
        continue
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            file_path = os.path.join(directory, filename)
            print(f"Processing {file_path}...")
            with open(file_path, 'r') as f:
                content = f.read()
            
            new_content = fix_border_radius(content)
            
            if new_content != content:
                with open(file_path, 'w') as f:
                    f.write(new_content)
                print(f"  Updated {file_path}")
            else:
                print(f"  No change needed for {file_path}")
