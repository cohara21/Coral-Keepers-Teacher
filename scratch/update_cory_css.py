import os, re

count = 0
for root, dirs, files in os.walk("."):
    if "node_modules" in root or ".git" in root or "scratch" in root: continue
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            original_content = content

            # Remove background from .floating-ai and .cory-trigger
            # Some files use #fff, some might use #ffffff. Let's just remove specific properties
            content = re.sub(r'border:\s*3px solid #[0-9a-fA-F]+;', 'border: none;', content)
            content = re.sub(r'background:\s*#fff(?:fff)?;', 'background: transparent;', content)
            
            # Since some box-shadows might be attached to .floating-ai, we can remove it.
            # The box-shadow is usually: box-shadow: 0 4px 4px rgba(0, 0, 0, 0.11);
            content = re.sub(r'box-shadow:\s*0 4px 4px rgba\(0,\s*0,\s*0,\s*0\.11\);', 'box-shadow: none;', content)

            # Change img width and height
            content = re.sub(r'width:\s*32\.287px;', 'width: 100%;', content)
            content = re.sub(r'height:\s*48\.156px;', 'height: 100%;', content)
            
            # We also might have a hover state background: #f4faff;
            content = re.sub(r'background:\s*#f4faff;', 'background: transparent;', content)

            if content != original_content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                count += 1
                print(f"Updated {path}")

print(f"Total updated: {count}")
