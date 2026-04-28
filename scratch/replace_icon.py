import os, re

count = 0
for root, dirs, files in os.walk("."):
    if "node_modules" in root or ".git" in root or "scratch" in root: continue
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Find the floating-ai or cory-trigger button and replace its img src
            new_content = re.sub(
                r'(<button[^>]*class=["\'][^>]*?(?:floating-ai|cory-trigger)[^>]*?["\'][^>]*>\s*<img[^>]*src=)["\'][^"\']*?["\']',
                r'\1"../assets/corychaticon.svg"',
                content,
                flags=re.IGNORECASE | re.DOTALL
            )
            
            if content != new_content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                count += 1
                print(f"Updated {path}")

print(f"Total updated: {count}")
